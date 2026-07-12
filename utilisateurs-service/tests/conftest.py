import os

os.environ.setdefault("DATABASE_URL", "postgresql://bibliotheque:changeme@localhost:5432/bibliotheque")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("JWT_EXPIRATION_MINUTES", "1440")

import pytest
from sqlalchemy import text

from app.database import SessionLocal, init_db
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def clean_users_table():
    init_db()
    db = SessionLocal()
    db.execute(text("TRUNCATE TABLE users_schema.users CASCADE"))
    db.commit()
    db.close()
    yield
