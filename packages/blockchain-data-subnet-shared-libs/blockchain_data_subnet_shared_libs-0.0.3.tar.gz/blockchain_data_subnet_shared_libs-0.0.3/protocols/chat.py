from uuid import UUID
from pydantic import BaseModel
from typing import List
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
    miner_id: str


class ChatMessageResponse(BaseModel):
    miner_id: str = ""
    response: List[QueryOutput]


class ContentType(str, Enum):
    text = "text"
    graph = "graph"
    table = "table"


