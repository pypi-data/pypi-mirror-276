"""
An abstract class for a worker which processes jobs from a NATS queue
"""

from abc import abstractmethod
import asyncio

import multiprocessing as mp
from multiprocessing import Value as V
import nats
import nats.aio
import nats.aio.client
import nats.errors
from typing import Dict, List, Optional
import rich

import chaps_nats


class NatsJobWorkerProcess(mp.Process):
    """
    A worker which processes jobs from a NATS queue

    >>> class MyWorker(NatsJobWorkerProcess):
    >>>     async def process_job(self, job : chaps_nats.NatsJob) -> bool:
    >>>         # Process the job
    >>>         print(f"Processing Job: {job.job_id}")
    >>>         return True
    >>>
    >>> if __name__ == "__main__":
    >>>     worker = MyWorker(nats_urls=["nats://localhost:4222"], app_id="MyWorker")
    >>>     worker.start()
    >>>     worker.join()

    """

    def __init__(
        self,
        nats_urls: List[str],
        queue_group: str = "",
        app_id: str = "",
        timeout: float = 0.1,
        *args,
        **kwargs,
    ):
        """
        Constructor
        :param nats_client: NatsClient
        :param subject: str
        :param queue_group: str
        """
        super().__init__(*args, **kwargs)
        self.nats_urls = nats_urls
        self.queue_group = queue_group
        self.app_id = app_id
        self._do_stop = V("b", False)
        self.timeout_s = timeout

    def stop(self):
        """
        Stops the worker
        """
        with self._do_stop.get_lock():
            self._do_stop.value = True

    def run(self):
        """
        Runs the worker
        """
        asyncio.run(self._run())

    async def init_context(self, nats_context: chaps_nats.NatsContext) -> Dict:
        """
        Initializes a context for the worker
        """
        return {}

    async def _run(self):
        """
        Runs the worker
        """
        async with chaps_nats.NatsContext(self.app_id, self.nats_urls) as nats_context:
            subject = chaps_nats.NatsJob.jobs_subject_prefix(nats_context) + ".>"
            sub = await nats_context.nats_client.subscribe(
                subject,
                queue=self.queue_group,
            )
            context = await self.init_context(nats_context)

            # Subscribe to the input subject
            while not self._do_stop.value:
                try:
                    await asyncio.sleep(0.001)

                    try:
                        msg = await sub.next_msg(timeout=self.timeout_s)
                    except asyncio.TimeoutError:
                        continue

                    job_id = msg.data.decode("utf-8")
                    rich.print(f"[green]Received Job: {job_id}[/green]")

                    try:
                        job = await chaps_nats.NatsJob.create(
                            nats_context, job_id, create_if_not_exists=False
                        )

                        # Check the status of the job
                        job_status = await job.status()
                        if job_status != chaps_nats.JobStatus.RUNNING:
                            rich.print(
                                f"[red]Job {job_id} is not in RUNNING state : {str(job_status)}[/red]"
                            )
                            continue

                        res = await self.process_job(job, context)
                        if not res:
                            await job.update_status(chaps_nats.JobStatus.CRASHED)
                            await job.update_progress(1.0)
                        else:
                            await job.update_status(chaps_nats.JobStatus.COMPLETED)
                            await job.update_progress(1.0)

                    except Exception as e:
                        rich.print(f"[red]Error Processing Job: {e}[/red]")
                        continue

                except asyncio.CancelledError:
                    with self._do_stop.get_lock():
                        self._do_stop.value = True
                    break

    @abstractmethod
    async def process_job(self, job: chaps_nats.NatsJob, context: Dict) -> bool:
        """
        Processes a job
        """
        raise NotImplementedError()
