from pydantic import BaseModel
from typing import List
from pydantic import BaseModel


class SearchRequest(BaseModel):
    text: str

class GarbageItemBase(BaseModel):
    id: int
    objname: str
    classify: str
    attention: str

    class Config:
        orm_mode = True

class GarbageSearchResponse(BaseModel):
    code: int = 0
    data: List[GarbageItemBase] = []
    msg: str = "success"