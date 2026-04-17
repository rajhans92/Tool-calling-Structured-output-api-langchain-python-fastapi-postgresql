from pydantic import BaseModel
from typing import List

class HeaderDetail(BaseModel):
    userId: str

class RequestBody(BaseModel):
    message: str