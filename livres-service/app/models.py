import uuid

from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class Livre(Base):
    __tablename__ = "livres"
    __table_args__ = {"schema": "livres_schema"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titre = Column(String, nullable=False)
    auteur = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=False)
    quantite_totale = Column(Integer, nullable=False, default=1)
    quantite_disponible = Column(Integer, nullable=False)
    date_ajout = Column(DateTime(timezone=True), server_default=func.now())
