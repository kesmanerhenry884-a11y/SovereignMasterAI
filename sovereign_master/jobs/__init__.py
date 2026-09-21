from dataclasses import dataclass
from typing import Any

@dataclass
class Job:
    id: str
    kind: str
    payload: dict[str, Any]
    status: str = "queued"

class JobQueue:
    def __init__(self): self.jobs: dict[str, Job] = {}
    def enqueue(self, job: Job) -> Job:
        self.jobs[job.id] = job
        return job
    def get(self, job_id: str): return self.jobs.get(job_id)
