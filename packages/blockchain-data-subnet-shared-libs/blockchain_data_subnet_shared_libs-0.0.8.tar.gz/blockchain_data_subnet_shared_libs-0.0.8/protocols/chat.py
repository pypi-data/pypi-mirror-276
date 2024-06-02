from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from protocols.llm_engine import QueryOutput


class ChatMessageRequest(BaseModel):
    network: str
    user_id: UUID
    prompt: str


class ChatMessageVariantRequest(BaseModel):
    network: str
    user_id: UUID
    prompt: str
    temperature: float
    miner_id: int


class ChatMessageResponse(BaseModel):
    miner_id: Optional[int] = None
    response: List[QueryOutput]


class ContentType(str, Enum):
    text = "text"
    graph = "graph"
    table = "table"


