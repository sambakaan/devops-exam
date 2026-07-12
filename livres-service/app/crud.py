from __future__ import annotations

import uuid

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models import Livre
from app.schemas import LivreCreate, LivreUpdate


class IsbnDejaUtiliseError(Exception):
    pass


def _to_uuid(livre_id) -> uuid.UUID | None:
    try:
        return uuid.UUID(str(livre_id))
    except ValueError:
        return None


def get_livre(db: Session, livre_id) -> Livre | None:
    livre_uuid = _to_uuid(livre_id)
    if livre_uuid is None:
        return None
    return db.query(Livre).filter(Livre.id == livre_uuid).first()


def get_livre_by_isbn(db: Session, isbn: str) -> Livre | None:
    return db.query(Livre).filter(Livre.isbn == isbn).first()


def get_livres(db: Session, skip: int = 0, limit: int = 100) -> list[Livre]:
    return db.query(Livre).offset(skip).limit(limit).all()


def search_livres(db: Session, q: str) -> list[Livre]:
    pattern = f"%{q}%"
    return (
        db.query(Livre)
        .filter(or_(Livre.titre.ilike(pattern), Livre.auteur.ilike(pattern), Livre.isbn.ilike(pattern)))
        .all()
    )


def create_livre(db: Session, livre: LivreCreate) -> Livre:
    if get_livre_by_isbn(db, livre.isbn) is not None:
        raise IsbnDejaUtiliseError(f"Un livre existe déjà avec l'ISBN {livre.isbn}")

    db_livre = Livre(
        titre=livre.titre,
        auteur=livre.auteur,
        isbn=livre.isbn,
        quantite_totale=livre.quantite_totale,
        quantite_disponible=livre.quantite_totale,
    )
    db.add(db_livre)
    db.commit()
    db.refresh(db_livre)
    return db_livre


def update_livre(db: Session, livre_id, livre_update: LivreUpdate) -> Livre | None:
    db_livre = get_livre(db, livre_id)
    if db_livre is None:
        return None

    for field, value in livre_update.model_dump(exclude_unset=True).items():
        setattr(db_livre, field, value)

    if db_livre.quantite_disponible > db_livre.quantite_totale:
        db_livre.quantite_disponible = db_livre.quantite_totale

    db.commit()
    db.refresh(db_livre)
    return db_livre


def delete_livre(db: Session, livre_id) -> bool:
    db_livre = get_livre(db, livre_id)
    if db_livre is None:
        return False
    db.delete(db_livre)
    db.commit()
    return True
