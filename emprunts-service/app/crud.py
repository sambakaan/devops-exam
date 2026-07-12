from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app import clients
from app.models import Emprunt, StatutEmprunt
from app.schemas import EmpruntCreate


class LivreIndisponibleError(Exception):
    pass


class EmpruntIntrouvableError(Exception):
    pass


class EmpruntDejaRetourneError(Exception):
    pass


def _to_uuid(value) -> uuid.UUID | None:
    try:
        return uuid.UUID(str(value))
    except ValueError:
        return None


def get_emprunt(db: Session, emprunt_id) -> Emprunt | None:
    emprunt_uuid = _to_uuid(emprunt_id)
    if emprunt_uuid is None:
        return None
    return db.query(Emprunt).filter(Emprunt.id == emprunt_uuid).first()


def get_emprunts(db: Session) -> list[Emprunt]:
    return db.query(Emprunt).all()


def get_historique_utilisateur(db: Session, utilisateur_id) -> list[Emprunt]:
    utilisateur_uuid = _to_uuid(utilisateur_id)
    if utilisateur_uuid is None:
        return []
    return db.query(Emprunt).filter(Emprunt.utilisateur_id == utilisateur_uuid).all()


def get_emprunts_en_retard(db: Session) -> list[Emprunt]:
    now = datetime.now(timezone.utc)
    emprunts = (
        db.query(Emprunt)
        .filter(Emprunt.statut == StatutEmprunt.en_cours, Emprunt.date_retour_prevue < now)
        .all()
    )
    for emprunt in emprunts:
        emprunt.statut = StatutEmprunt.en_retard
    db.commit()
    for emprunt in emprunts:
        db.refresh(emprunt)
    return emprunts


def creer_emprunt(db: Session, emprunt: EmpruntCreate, token: str) -> Emprunt:
    livre = clients.get_livre(emprunt.livre_id, token)
    if livre["quantite_disponible"] <= 0:
        raise LivreIndisponibleError(f"Le livre {emprunt.livre_id} n'a plus d'exemplaire disponible")

    clients.get_utilisateur(emprunt.utilisateur_id, token)

    clients.update_livre_quantite(emprunt.livre_id, livre["quantite_disponible"] - 1, token)

    db_emprunt = Emprunt(
        livre_id=emprunt.livre_id,
        utilisateur_id=emprunt.utilisateur_id,
        statut=StatutEmprunt.en_cours,
    )
    db.add(db_emprunt)
    db.commit()
    db.refresh(db_emprunt)
    return db_emprunt


def retourner_emprunt(db: Session, emprunt_id, token: str) -> Emprunt:
    db_emprunt = get_emprunt(db, emprunt_id)
    if db_emprunt is None:
        raise EmpruntIntrouvableError(f"Emprunt {emprunt_id} introuvable")
    if db_emprunt.statut == StatutEmprunt.retourne:
        raise EmpruntDejaRetourneError(f"Emprunt {emprunt_id} déjà retourné")

    livre = clients.get_livre(db_emprunt.livre_id, token)
    clients.update_livre_quantite(db_emprunt.livre_id, livre["quantite_disponible"] + 1, token)

    db_emprunt.date_retour_effective = datetime.now(timezone.utc)
    db_emprunt.statut = StatutEmprunt.retourne
    db.commit()
    db.refresh(db_emprunt)
    return db_emprunt
