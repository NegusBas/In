from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from ..models.schemas import (
    Message, MessageCreate, 
    Conversation, ConversationCreate
)
from ..database.connection import get_db
from typing import List

router = APIRouter()

@router.get("/conversations/", response_model=List[Conversation])
def get_conversations():
    """
    Retrieve all conversations with their messages.
    """
    with get_db() as db:
        result = db.execute(
            text("""
                SELECT c.id, c.title, c.temperature, c.last_updated,
                       m.id as message_id, m.content, m.role, m.timestamp
                FROM conversation c
                LEFT JOIN message m ON c.id = m.conversation_id
                ORDER BY c.last_updated DESC, m.timestamp ASC
            """)
        )
        
        conversations = {}
        for row in result:
            if row.id not in conversations:
                conversations[row.id] = {
                    "id": row.id,
                    "title": row.title,
                    "temperature": float(row.temperature),
                    "last_updated": row.last_updated,
                    "messages": []
                }
            
            if row.message_id:
                conversations[row.id]["messages"].append({
                    "id": row.message_id,
                    "content": row.content,
                    "role": row.role,
                    "conversation_id": row.id,
                    "timestamp": row.timestamp
                })
        
        return list(conversations.values())

@router.get("/conversations/{conversation_id}/messages/", response_model=List[Message])
def get_messages(conversation_id: int):
    """
    Retrieve all messages for a specific conversation.
    """
    with get_db() as db:
        result = db.execute(
            text("""
                SELECT id, conversation_id, content, role, timestamp
                FROM message
                WHERE conversation_id = :conversation_id
                ORDER BY timestamp ASC
            """),
            {"conversation_id": conversation_id}
        )
        
        messages = []
        for row in result:
            messages.append({
                "id": row.id,
                "conversation_id": row.conversation_id,
                "content": row.content,
                "role": row.role,
                "timestamp": row.timestamp
            })
            
        if not messages:
            raise HTTPException(status_code=404, detail="Conversation not found")
            
        return messages

@router.post("/conversations/", response_model=Conversation)
def create_conversation(conversation: ConversationCreate):
    """
    Create a new conversation.
    """
    with get_db() as db:
        if not (0 <= conversation.temperature <= 2):
            raise HTTPException(
                status_code=400,
                detail="Temperature must be between 0 and 2"
            )
            
        result = db.execute(
            text("""
                INSERT INTO conversation (title, temperature)
                VALUES (:title, :temperature)
                RETURNING id, title, temperature, last_updated
            """),
            {
                "title": conversation.title,
                "temperature": conversation.temperature
            }
        )
        
        db.commit()
        new_conversation = result.first()
        
        return {
            "id": new_conversation.id,
            "title": new_conversation.title,
            "temperature": float(new_conversation.temperature),
            "last_updated": new_conversation.last_updated,
            "messages": []
        }

@router.post("/messages/", response_model=Message)
def create_message(message: MessageCreate):
    """
    Create a new message in a conversation.
    """
    with get_db() as db:
        if message.role not in ['user', 'assistant']:
            raise HTTPException(
                status_code=400,
                detail="Role must be either 'user' or 'assistant'"
            )
            
        conversation = db.execute(
            text("SELECT id FROM conversation WHERE id = :id"),
            {"id": message.conversation_id}
        ).first()
        
        if not conversation:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found"
            )
            
        result = db.execute(
            text("""
                INSERT INTO message (conversation_id, content, role)
                VALUES (:conversation_id, :content, :role)
                RETURNING id, conversation_id, content, role, timestamp
            """),
            {
                "conversation_id": message.conversation_id,
                "content": message.content,
                "role": message.role
            }
        )
        
        db.execute(
            text("""
                UPDATE conversation
                SET last_updated = CURRENT_TIMESTAMP
                WHERE id = :conversation_id
            """),
            {"conversation_id": message.conversation_id}
        )
        
        db.commit()
        new_message = result.first()
        
        return {
            "id": new_message.id,
            "conversation_id": new_message.conversation_id,
            "content": new_message.content,
            "role": new_message.role,
            "timestamp": new_message.timestamp
        }