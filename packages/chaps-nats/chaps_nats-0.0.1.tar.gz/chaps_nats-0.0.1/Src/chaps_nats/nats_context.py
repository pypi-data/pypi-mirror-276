"""
NatsContext class

NatsContext is a wrapper around a NATS connection and a JetStream context.
The NatsContext should be used as a context manager, to ensure that the connection to the NATS server is properly open/closed.

@author: Pierre Dellenbach
"""

import nats
import nats.aio
import nats.aio.subscription
import nats.aio.transport
import nats.js
import nats.js.api
import nats.js.errors
import nats.errors

import nats.js.object_store
from typing import List, Union, Dict, Optional
import asyncio
import rich
import time
import json

from enum import Enum, IntEnum
from pydantic import BaseModel, Field
from abc import ABC, abstractmethod



class NatsContext:
    """
    A class for managing a NATS context.

    A NATS context is a connection to the NATS server, and a JetStream context for managing object stores.
    In this library, one object store is created for each job. The NatsContext keeps track of all object stores created.

    Usage:

    >>> async with NatsContext(app_id="test", urls=["nats://localhost:4222"]) as nats_context:
    >>>     object_stores = await nats_context.list_object_stores()
    >>>     print(object_stores)

    """

    def __init__(self, app_id: str, urls: List[str]):
        self.app_id: str = app_id
        self.nats_urls = urls
        self.nats_client: nats.NATS = None
        self.js: nats.js.JetStreamContext = None
        self.object_store: nats.js.ObjectStore = None
        self._is_initialized = False

    async def _debug_streams(self):
        rich.print("[bold green]Streams Info[/]")
        rich.print(await self.js.streams_info())
        if self.object_store is not None:
            try:
                rich.print("[bold green]Object Store Info[/]")
                rich.print(await self.object_store.list(ignore_deletes=True))
            except nats.js.errors.NotFoundError:
                pass

    def store_fullid(self, store_id: str) -> str:
        return f"{self.app_id}_{store_id}"

    async def delete_object_store(self, store_id: str) -> bool:
        try:
            res = await self.object_store.delete(store_id)

            os_store_id = self.store_fullid(store_id)
            res = await self.js.delete_object_store(os_store_id)

            return res
        except nats.js.errors.NotFoundError:
            rich.print(f"[red]Object Store {store_id} not found[/red]")
            pass
        except Exception as e:
            pass
        return False

    async def get_object_store(
        self, store_id: str, create_if_not_exists: bool = True
    ) -> nats.js.object_store.ObjectStore:
        # try to retrieve the object store if it exists
        object_store = None
        try:
            object_store = await self.js.object_store(self.store_fullid(store_id))
        except Exception as e:
            if not create_if_not_exists:
                # TODO: Add logging
                raise e
            pass

        if object_store is not None:
            return object_store

        # Keep the name of the object store in the main object store
        await self.object_store.put(store_id, b"")
        object_store = await self.js.create_object_store(
            bucket=self.store_fullid(store_id),
            storage=nats.js.api.StorageType.FILE,
        )

        return object_store

    def _key(self, key: str) -> str:
        return f"{self.app_id}.{key}"

    async def write_data(self, key: str, data: Union[bytes, str]):
        """
        Writes data to the object store
        """
        await self.object_store.put(self._key(key), data)

    async def read_data(self, key: str) -> bytes:
        """
        Reads data from the object store
        """
        obr = await self.object_store.get(self._key(key))
        return obr.data

    async def delete_data(self, key: str):
        """
        Deletes data from the object store
        """
        await self.object_store.delete(self._key(key))

    async def list_object_stores(self):
        """
        Lists all object stores
        """
        if self.object_store is None:
            return []
        try:
            obj_infos = await self.object_store.list(ignore_deletes=True)
        except nats.js.errors.NotFoundError:
            return []
        return [obj.name for obj in obj_infos]

    async def list_streams(self) -> List[nats.js.api.StreamInfo]:
        """
        Returns the list of streams
        """
        streams = await self.js.streams_info()
        return streams

    async def _close_context(self):
        try:
            await self.nats_client.close()
        except Exception as e:
            raise e

    async def _init_context(self):
        """
        Initializes the NATS context : connects to the NATS server, creates the object store
        """
        try:
            self.nats_client = await nats.connect(servers=self.nats_urls)
            self.js = self.nats_client.jetstream()
            bucket_store_id = f"{self.app_id}_object_store"

            try:
                self.object_store = await asyncio.wait_for(
                    self.js.object_store(bucket=bucket_store_id), 10
                )
                self._is_initialized = True
            except (asyncio.TimeoutError, nats.js.errors.BucketNotFoundError):
                rich.print(f"[red]Creating Object Store {bucket_store_id}[/red]")
                self.object_store = await self.js.create_object_store(
                    bucket=f"{self.app_id}_object_store",
                    storage=nats.js.api.StorageType.FILE,
                )
                self._is_initialized = True
                pass
            except Exception as e:
                rich.print(f"[red]Error Creating Object Store {bucket_store_id}[/red]")
                raise e
        except Exception as e:
            raise e

    async def __aexit__(self, exc_type, exc_value, traceback):
        """
        Finalizes the context : closes the connection to the NATS server
        """
        await self._close_context()

    async def __aenter__(self):
        """
        Initializes the context : connects to the NATS server, creates the object store
        """
        try:
            await asyncio.wait_for(self._init_context(), 10)
        except Exception as e:
            rich.print("[red]Error initializing NATS context. Caught exception[/]")
            raise e
        return self
