from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class MessageBase(BaseModel):
    content: str
    role: str

class MessageCreate(MessageBase):
    conversation_id: int

class Message(MessageBase):
    id: int
    conversation_id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

class ConversationBase(BaseModel):
    title: str
    temperature: float

class ConversationCreate(ConversationBase):
    pass

class Conversation(ConversationBase):
    id: int
    last_updated: datetime
    messages: List[Message] = []

    class Config:
        from_attributes = True