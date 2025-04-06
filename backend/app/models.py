from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    session_id: Optional[str] = None
    stream: bool = False

class ChatResponse(BaseModel):
    content: str

class SessionHistoryRequest(BaseModel):
    session_id: str

class HistoryMessage(BaseModel):
    id: int
    role: str
    content: str
    created_at: str

class SessionHistoryResponse(BaseModel):
    messages: List[HistoryMessage] 