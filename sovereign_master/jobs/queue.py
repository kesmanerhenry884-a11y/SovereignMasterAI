from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


@dataclass
class Job:
    id: str
    kind: str
    payload: dict[str, Any]
    status: str = "queued"
    created_at: str | None = None
    result: dict[str, Any] | None = None


class JobQueue:
    def __init__(self):
        self._jobs: dict[str, Job] = {}

    def enqueue(self, kind: str, payload: dict[str, Any] | None = None, job_id: str | None = None) -> Job:
        new_id = job_id or str(uuid4())
        job = Job(id=new_id, kind=kind, payload=payload or {}, status="queued", created_at="now")
        self._jobs[new_id] = job
        return job

    def update(self, job_id: str, **kwargs: Any) -> Job | None:
        job = self._jobs.get(job_id)
        if job is None:
            return None
        for key, value in kwargs.items():
            setattr(job, key, value)
        return job

    def get(self, job_id: str) -> Job | None:
        return self._jobs.get(job_id)

    def list(self) -> list[dict[str, Any]]:
        return [
            {
                "id": job.id,
                "kind": job.kind,
                "status": job.status,
                "payload": job.payload,
                "result": job.result,
            }
            for job in self._jobs.values()
        ]


JOB_QUEUE = JobQueue()
__all__ = ["Job", "JobQueue", "JOB_QUEUE"]
