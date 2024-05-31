from typing import Union, Optional
from pydantic import BaseModel


class Collection(BaseModel):
    uid: str
    name: str
    videos_count: int
    videos: Optional[list] = None
    total_seconds: Optional[int] = None
    created_at: str
