from datetime import datetime

from pydantic import BaseModel, Field


class StoreBase(BaseModel):
    name: str = Field(min_length=4, max_length=20)
    owner: str

class Store(StoreBase):
    id: int

class DbStore(Store):
    created_at: datetime = datetime.now()

class CreateStore(StoreBase):
    pass

class PatchStore(BaseModel):
    name: str | None = Field(default=None, min_length=4, max_length=20)
    owner: str | None = None
