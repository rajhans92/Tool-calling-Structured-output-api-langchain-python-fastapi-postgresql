from pydantic import BaseModel
from typing import List, Dict, Any

class HeaderDetail(BaseModel):
    userId: str

class RequestBody(BaseModel):
    message: str

class ToolCall(BaseModel):
    tool: str
    args: Dict[str, Any]
    depends_on: List[str]

class ExecutionPlan(BaseModel):
    execution_plan: List[ToolCall]