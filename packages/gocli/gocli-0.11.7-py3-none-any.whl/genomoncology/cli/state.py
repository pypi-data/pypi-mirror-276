import asyncio

from pydantic import BaseModel


class State(BaseModel):
    hard_failure: bool = True
    glob: list[str] = []
    include_tar: bool = False
    batch_size: int = 50
    parallel_batches: int = 25
    run_id: str | None = None
    pipeline: str | None = None
    build: str | None = None
    runner: asyncio.Runner | None = None

    class Config:
        arbitrary_types_allowed = True
