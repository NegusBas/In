# Messaging API

A FastAPI-based messaging system API that provides endpoints for managing conversations and messages.

## Features

- Retrieve conversations with messages
- Retrieve messages for specific conversations
- Create new conversations
- Create new messages
- Input validation
- Error handling
- API documentation

## Prerequisites

- Python 3.8+
- PostgreSQL database
- Docker (optional)

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd messaging-api
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp .env.example .env
```
Edit the `.env` file with your database credentials.

## Running the Application

### Using Python

```bash
uvicorn src.main:app --reload
```

### Using Docker

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

## API Endpoints

- `GET /conversations/`: Retrieve all conversations
- `GET /conversations/{conversation_id}/messages/`: Retrieve messages for a specific conversation
- `POST /conversations/`: Create a new conversation
- `POST /messages/`: Create a new message

## Testing

Run tests using pytest:
```bash
pytest
```

## License

MIT License