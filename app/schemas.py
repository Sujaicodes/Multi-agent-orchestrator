from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class QueryRequest(BaseModel):
    query: str
    user_id: str

class TaskState(BaseModel):
    id: str
    title: str
    status: str = "pending"
    deadline: Optional[str] = None

class OrchestratorResponse(BaseModel):
    query: str
    plan: List[str]
    agents_used: List[str]
    tools_used: List[str]
    final_response: str
    logs: List[Dict[str, Any]]