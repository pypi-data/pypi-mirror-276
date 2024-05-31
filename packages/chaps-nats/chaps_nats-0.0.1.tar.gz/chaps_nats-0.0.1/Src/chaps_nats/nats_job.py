"""
This module contains the NatsJob abstractions.

NatsJob manages the interactions with a specific job (defines the status, progress, etc.).
It is associated with a specific object store in the NATS server, for storing input/output data.

@author: Pierre Dellenbach
"""

import nats
import nats.aio
import nats.aio.subscription
import nats.aio.transport
import nats.errors
import nats.js
import nats.js.api
import nats.js.errors
import nats.js.object_store
import struct

from typing import Optional, List
import enum
import rich
import random
import string

from .nats_context import NatsContext


def _generate_id(length: int = 6, chars=string.ascii_lowercase + string.digits) -> str:
    """
    Generates a random id for a job
    """
    return "".join(random.SystemRandom().choice(chars) for _ in range(length))


class JobStatus(enum.Enum):
    """
    Defines the status of a job.

    Useful for querying the status of a job in the NATS context
    """

    CREATED = "CREATED"
    RUNNING = "RUNNING"
    CRASHED = "CRASHED"
    INTERRUPTED = "INTERRUPTED"
    COMPLETED = "COMPLETED"
    INVALID_STATE = "INVALID_STATE"

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def from_str(status: str) -> "JobStatus":
        key = status.upper()
        if key not in JobStatus.__members__:
            return JobStatus.INVALID_STATE
        return JobStatus[key]


class NatsJob:
    """
    A class for managing a job within the NATS context
    """

    def __init__(self, job_id: str, nats_context: NatsContext):
        self.job_id = job_id
        self.nats_context = nats_context
        self.object_store = None
        assert job_id is not None, "job_id must not be None"

    @staticmethod
    async def create(
        nats_context: NatsContext,
        job_id: Optional[str] = None,
        create_if_not_exists: bool = False,
    ) -> "NatsJob":
        """
        Creates a job within the NATS context

        If the job does not exist, it creates the job and sets the status to CREATED
        """
        assert nats_context._is_initialized, "NatsContext must be initialized"
        if job_id is None:
            assert (
                create_if_not_exists
            ), "job_id must be provided if create_if_not_exists is False"
            job_id = _generate_id()

        job = NatsJob(job_id, nats_context)
        await job._init_job(create_if_not_exists)
        return job

    @property
    def status_key(self):
        return "status"

    @property
    def progress_key(self):
        return "progress"

    @staticmethod
    def get_store_id(job_id: str) -> str:
        return f"job_{job_id}"

    @property
    def store_id(self):
        return self.get_store_id(self.job_id)

    @staticmethod
    async def list_jobs(nats_context: NatsContext) -> List[str]:
        job_ids = []
        for store in await nats_context.list_object_stores():
            if store.startswith("job_"):
                job_id = "_".join(store.split("_")[1:])
                job_ids.append(job_id)

        return job_ids

    async def _init_job(self, create_if_not_exists: bool = True):
        """
        Connects the job to the NATS context, and creates/loads an associated object store
        If the job does not exist, it creates the job and sets the status to CREATED
        """
        self.object_store = await self.nats_context.get_object_store(
            self.store_id, create_if_not_exists
        )
        status: JobStatus = None
        progress: float = None
        try:
            status = await self.object_store.get(self.status_key)
        except nats.js.errors.ObjectNotFoundError:
            status = None

        try:
            progress = await self.object_store.get(self.progress_key)
        except nats.js.errors.ObjectNotFoundError:
            progress = None

        if not status:
            await self.object_store.put(self.status_key, str(JobStatus.CREATED))
        if not progress:
            await self.object_store.put(self.progress_key, struct.pack("f", 0.0))

    async def status(self) -> JobStatus:
        """
        Returns the status of the job
        """
        assert self.object_store is not None, "Job not initialized"
        try:
            res: nats.js.object_store.ObjectStore.ObjectResult = (
                await self.object_store.get(self.status_key)
            )
            status_str = res.data.decode("utf-8")
        except nats.js.errors.ObjectNotFoundError:
            return JobStatus.INVALID_STATE

        return JobStatus.from_str(status_str)

    async def update_status(self, status: JobStatus):
        """
        Updates the status of the job
        """
        assert self.object_store is not None, "Job not initialized"
        status_value = str(status)
        await self.object_store.put(self.status_key, status_value)

    async def progress(self) -> float:
        """
        Returns the progress of the job
        """
        assert self.object_store is not None, "Job not initialized"
        try:
            res: nats.js.object_store.ObjectStore.ObjectResult = (
                await self.object_store.get(self.progress_key)
            )
            progress = struct.unpack("f", res.data)[0]
        except nats.js.errors.ObjectNotFoundError:
            return 0.0

        return progress

    async def update_progress(self, progress: float):
        """
        Updates the progress of the job
        """
        assert isinstance(progress, float), "Progress must be a float"
        assert progress >= 0.0 and progress <= 1.0, "Progress must be between 0 and 1"
        try:
            await self.object_store.put(self.progress_key, struct.pack("f", progress))
        except Exception as e:
            raise e

    async def delete_job(self) -> bool:
        """
        Deletes the job, and the associated object store(s)
        """
        try:
            res = await self.nats_context.delete_object_store(self.store_id)
            self.object_store = None
            return res
        except Exception as e:
            rich.print(f"[red]Error Deleting Job: {e}[/red]")
            raise e

    async def list_objects(self) -> List[str]:
        """
        Lists all objects in the object store of the job
        """
        obj_infos = await self.object_store.list(ignore_deletes=True)
        return [obj.name for obj in obj_infos]

    async def start_job(self):
        """
        Starts the job
        """
        status = await self.status()
        if status != JobStatus.CREATED:
            raise Exception("Job must be in CREATED state to start")
        await self.update_status(JobStatus.RUNNING)
        # Publish a message to the job's subject to start the job
        await self.nats_context.nats_client.publish(
            f"{self.jobs_subject_prefix(self.nats_context)}.{self.job_id}",
            self.job_id.encode("utf-8"),
        )
        await self.nats_context.nats_client.flush(timeout=1)
        rich.print(f"[green]Job {self.job_id} started[/green]")

    @staticmethod
    def jobs_subject_prefix(nats_context: NatsContext) -> str:
        return f"{nats_context.app_id}.job"
