from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from protocols.llm_engine import QueryOutput


class ChatMessageRequest(BaseModel):
    network: str
    prompt: str


class ChatMessageVariantRequest(BaseModel):
    network: str
    prompt: str
    miner_hotkey: str


class ChatMessageResponse(BaseModel):
    miner_hotkey: Optional[str] = None
    response: List[QueryOutput]


class ContentType(str, Enum):
    text = "text"
    graph = "graph"
    table = "table"


