from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models import TypeUtilisateur


class UserCreate(BaseModel):
    nom: str
    prenom: str
    email: str
    mot_de_passe: str
    type_utilisateur: TypeUtilisateur


class UserLogin(BaseModel):
    email: str
    mot_de_passe: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    nom: str
    prenom: str
    email: str
    type_utilisateur: TypeUtilisateur
    date_creation: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
