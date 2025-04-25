from pydantic import BaseModel
from datetime import datetime
from typing import List

class SearchHistoryBase(BaseModel):
    id: int
    keyword: str
    created_at: datetime

    class Config:
        orm_mode = True

class SearchHistoryResponse(BaseModel):
    code: int = 0
    data: List[SearchHistoryBase] = []
    msg: str = "success"