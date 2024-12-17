import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Messaging System API"}

def test_create_conversation():
    response = client.post(
        "/api/v1/conversations/",
        json={"title": "Test Conversation", "temperature": 1.0}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Conversation"
    assert abs(data["temperature"] - 1.0) < 1e-6  # Using epsilon comparison for floating point

def test_create_conversation_invalid_temperature():
    response = client.post(
        "/api/v1/conversations/",
        json={"title": "Test Conversation", "temperature": 3.0}
    )
    assert response.status_code == 400

def test_get_conversations():
    response = client.get("/api/v1/conversations/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_message():
    # First create a conversation
    conv_response = client.post(
        "/api/v1/conversations/",
        json={"title": "Test Conversation", "temperature": 1.0}
    )
    conv_id = conv_response.json()["id"]
    
    # Then create a message
    response = client.post(
        "/api/v1/messages/",
        json={
            "conversation_id": conv_id,
            "content": "Test message",
            "role": "user"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Test message"
    assert data["role"] == "user"

def test_create_message_invalid_role():
    response = client.post(
        "/api/v1/messages/",
        json={
            "conversation_id": 1,
            "content": "Test message",
            "role": "invalid"
        }
    )
    assert response.status_code == 400