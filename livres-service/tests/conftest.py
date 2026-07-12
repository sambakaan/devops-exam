import os

os.environ.setdefault("DATABASE_URL", "postgresql://bibliotheque:changeme@localhost:5432/bibliotheque")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("JWT_EXPIRATION_MINUTES", "1440")

import uuid
from datetime import datetime, timedelta, timezone

import pytest
from jose import jwt
from sqlalchemy import text

from app.database import SessionLocal, init_db
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def clean_livres_table():
    init_db()
    db = SessionLocal()
    db.execute(text("TRUNCATE TABLE livres_schema.livres CASCADE"))
    db.commit()
    db.close()
    yield


def make_token(sub=None, email="test@example.com", type_utilisateur="etudiant"):
    payload = {
        "sub": sub or str(uuid.uuid4()),
        "email": email,
        "type_utilisateur": type_utilisateur,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }
    return jwt.encode(payload, os.environ["JWT_SECRET_KEY"], algorithm=os.environ["JWT_ALGORITHM"])


@pytest.fixture()
def auth_headers():
    return {"Authorization": f"Bearer {make_token()}"}
