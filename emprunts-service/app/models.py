import enum
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import Column, DateTime, Enum, func
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class StatutEmprunt(str, enum.Enum):
    en_cours = "en_cours"
    retourne = "retourne"
    en_retard = "en_retard"


def _date_retour_prevue_par_defaut():
    return datetime.now(timezone.utc) + timedelta(days=14)


class Emprunt(Base):
    __tablename__ = "emprunts"
    __table_args__ = {"schema": "emprunts_schema"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    livre_id = Column(UUID(as_uuid=True), nullable=False)
    utilisateur_id = Column(UUID(as_uuid=True), nullable=False)
    date_emprunt = Column(DateTime(timezone=True), server_default=func.now())
    date_retour_prevue = Column(DateTime(timezone=True), nullable=False, default=_date_retour_prevue_par_defaut)
    date_retour_effective = Column(DateTime(timezone=True), nullable=True)
    statut = Column(
        Enum(StatutEmprunt, name="statut_emprunt_enum", schema="emprunts_schema"),
        nullable=False,
        default=StatutEmprunt.en_cours,
    )
