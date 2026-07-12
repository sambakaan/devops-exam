import enum
import uuid

from sqlalchemy import Column, DateTime, Enum, String, func
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class TypeUtilisateur(str, enum.Enum):
    etudiant = "etudiant"
    professeur = "professeur"
    personnel_administratif = "personnel_administratif"


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "users_schema"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    mot_de_passe_hash = Column(String, nullable=False)
    type_utilisateur = Column(
        Enum(TypeUtilisateur, name="type_utilisateur_enum", schema="users_schema"),
        nullable=False,
    )
    date_creation = Column(DateTime(timezone=True), server_default=func.now())
