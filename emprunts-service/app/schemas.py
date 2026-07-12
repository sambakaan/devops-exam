from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models import StatutEmprunt


class EmpruntCreate(BaseModel):
    livre_id: UUID
    utilisateur_id: UUID


class EmpruntOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    livre_id: UUID
    utilisateur_id: UUID
    date_emprunt: datetime
    date_retour_prevue: datetime
    date_retour_effective: Optional[datetime] = None
    statut: StatutEmprunt
