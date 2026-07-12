from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class LivreCreate(BaseModel):
    titre: str
    auteur: str
    isbn: str
    quantite_totale: int = 1


class LivreUpdate(BaseModel):
    titre: Optional[str] = None
    auteur: Optional[str] = None
    isbn: Optional[str] = None
    quantite_totale: Optional[int] = None
    quantite_disponible: Optional[int] = None


class LivreOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    titre: str
    auteur: str
    isbn: str
    quantite_totale: int
    quantite_disponible: int
    date_ajout: datetime
