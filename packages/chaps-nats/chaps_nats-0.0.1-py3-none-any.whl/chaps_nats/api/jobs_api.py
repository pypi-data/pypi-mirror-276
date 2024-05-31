"""
This module defines the JobAPI class.

The JobAPI class is an abstract class to construct standardized Jobs APIs on top of NATS.

@author: Pierre Dellenbach
"""

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, Query, status
from fastapi.security import HTTPBearer
import nats
import nats.aio
import nats.js.object_store
import os
from pydantic import BaseModel
import rich
from typing import Optional, Callable, List, Union


import chaps_nats


class _JobID(BaseModel):
    """
    Result of a job submission
    """

    job_id: str = "awshZ2"


class JobAPI:
    """
    An abstract class for an API which receives job submissions and either processes them (for rapid jobs)
    Or pushes them to a NATS queue for processing by workers.

    app_id is the unique identifier for the NATS workspace.
    It is important, as it is used to create the NATS object stores and queues

    Workers:
    app_id.workers.>worker_id (worker_id is the unique identifier for the worker)

    Queue:
    app_id.job_id.message
    """

    def __init__(
        self,
        app_id: str,
        nats_urls: List[str],
        api_prefix: str = "",
        app: Optional[FastAPI] = None,
        title: str = "TODO: Chaps Job API",
        description: str = "TODO: Add a description",
        *args,
        **kwargs,
    ):
        self.api_prefix = api_prefix
        self.app_id = app_id
        self.nats_urls = nats_urls

        # Create the FastAPI app
        self.app = app
        self.auth = None
        if self.app is None:
            # Create the FastAPI app using the default model expected by iaparc
            self.app = FastAPI(
                lifespan=self._get_lifespan(self),
                title=title,
                description=description,
                openapi_url="/docs/openapi.json",
                root_path=os.getenv(key="ROOT_URL", default=""),
            )
            self.auth = HTTPBearer()
        else:
            assert isinstance(self.app, FastAPI), "app must be an instance of FastAPI"

        self.add_routes()

    @staticmethod
    def _get_lifespan(_self: "JobAPI"):
        """
        Returns the lifespan of the FastAPI app
        """

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            # ============ Check Environment variables ============ #
            # ============ Load the flags database ============ #
            # Load from environment
            await _self.init_lifespan()
            yield
            await _self.close_lifespan()

        return lifespan

    def _make_nats_context(self) -> chaps_nats.NatsContext:
        context = chaps_nats.NatsContext(app_id=self.app_id, urls=self.nats_urls)
        return context

    async def init_lifespan(self):
        try:
            # Try to initialize the NATS context with a timeout
            nats_context = self._make_nats_context()
            await asyncio.wait_for(nats_context._init_context(), timeout=10)
        except Exception as e:
            rich.print("[b red]Error initializing NATS context. Caught exception[/]")
            rich.print(e)
            exit(1)

    async def close_lifespan(self):
        """
        Closes the context (typically resources like processes, connections, etc..)
        """
        pass

    def add_routes(self):
        """
        Adds API routes to the FastAPI app
        """
        # Submit job
        _submit_job_fun = self._job_submit_fun()
        if _submit_job_fun is not None:
            self.app.post(
                f"{self.api_prefix}/submit_job", tags=["Jobs"], response_model=_JobID
            )(_submit_job_fun)

        # Results
        _results_job_fun = self._job_results_fun()
        if _results_job_fun is not None:
            self.app.get(f"{self.api_prefix}/job_results/{{job_id}}", tags=["Jobs"])(
                _results_job_fun
            )

        # Status
        _jobs_status_fun = self._jobs_status_fun()
        if _jobs_status_fun is not None:
            self.app.get(f"{self.api_prefix}/job_status/{{job_id}}", tags=["Jobs"])(
                _jobs_status_fun
            )

        # Delete
        _job_delete_fun = self._job_delete_fun()
        if _job_delete_fun is not None:
            self.app.delete(f"{self.api_prefix}/delete_job/{{job_id}}", tags=["Jobs"])(
                _job_delete_fun
            )

        # List Jobs
        _job_lists_fun = self._job_lists_fun()
        if _job_lists_fun is not None:
            self.app.get(f"{self.api_prefix}/job_list", tags=["Jobs"])(_job_lists_fun)

    def _job_submit_fun(self) -> Optional[Callable]:
        return None

    def _job_results_fun(self) -> Optional[Callable]:
        return None

    def _job_delete_fun(self) -> Optional[Callable]:
        """
        Returns the default delete job function
        """

        async def delete_job(
            job_id: str,
            auth: HTTPBearer = Depends(self.auth),
        ):
            """
            Deletes a job
            """
            async with self._make_nats_context() as nats_context:
                try:
                    job = await chaps_nats.NatsJob.create(nats_context, job_id)
                    delete_job = await job.delete_job()
                    await asyncio.sleep(0)
                    return {"ok": delete_job}
                except Exception as e:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail={"message": "Job not found", "error": str(e)},
                    )

        return delete_job

    def _jobs_status_fun(self) -> Optional[Callable]:
        """
        Returns the default job status function
        """

        async def job_status(
            job_id: str,
            # TODO: Add a functionality to append / store messages for a job with_messages: bool = Query(
            #     False,
            #     description="Include the array of messages in the response (key **'messages'**).",
            # ),
            auth: HTTPBearer = Depends(self.auth),
        ):
            """
            ## Returns the status of a job
            """
            async with self._make_nats_context() as nats_context:
                try:
                    job = await chaps_nats.NatsJob.create(nats_context, job_id)
                except Exception as e:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail={"message": "Job not found", "error": str(e)},
                    )
                result = {
                    "status": await job.status(),
                    "progress": await job.progress(),
                }
                # TODO: Add a message mechanism
                return result

        return job_status

    def _job_lists_fun(self) -> Callable:
        """
        Returns the default job list function
        """

        async def info(
            auth: HTTPBearer = Depends(self.auth),
        ):
            """
            Get the list of jobs and their status
            """
            async with self._make_nats_context() as nats_context:
                jobs = await chaps_nats.NatsJob.list_jobs(nats_context)

                jobs_model = []
                for job_id in jobs:
                    job = await chaps_nats.NatsJob.create(nats_context, job_id)
                    try:
                        jobs_model.append(
                            {
                                "job_id": job.job_id,
                                "status": await job.status(),
                                "progress": await job.progress(),
                            }
                        )
                    except Exception as e:
                        continue

                return {"jobs": jobs_model}

        return info
