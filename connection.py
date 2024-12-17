from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from contextlib import contextmanager
from ..config import DATABASE_URL

engine = create_engine(DATABASE_URL)

@contextmanager
def get_db():
    try:
        db = Session(engine)
        yield db
    finally:
        db.close()