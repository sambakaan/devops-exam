from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from app import auth
from app.models import User
from app.schemas import UserCreate


class EmailDejaUtiliseError(Exception):
    pass


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id) -> User | None:
    try:
        user_uuid = uuid.UUID(str(user_id))
    except ValueError:
        return None
    return db.query(User).filter(User.id == user_uuid).first()


def get_all_users(db: Session) -> list[User]:
    return db.query(User).all()


def create_user(db: Session, user: UserCreate) -> User:
    if get_user_by_email(db, user.email) is not None:
        raise EmailDejaUtiliseError(f"Un compte existe déjà avec l'email {user.email}")

    db_user = User(
        nom=user.nom,
        prenom=user.prenom,
        email=user.email,
        mot_de_passe_hash=auth.hash_password(user.mot_de_passe),
        type_utilisateur=user.type_utilisateur,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
