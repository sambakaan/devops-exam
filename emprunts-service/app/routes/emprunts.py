from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app import clients, crud
from app.auth import bearer_scheme, get_current_user
from app.database import get_db
from app.schemas import EmpruntCreate, EmpruntOut

router = APIRouter(prefix="/emprunts", tags=["emprunts"])


@router.post("", response_model=EmpruntOut, status_code=status.HTTP_201_CREATED)
def creer_emprunt(
    emprunt: EmpruntCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        return crud.creer_emprunt(db, emprunt, credentials.credentials)
    except clients.LivreIntrouvableError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except clients.UtilisateurIntrouvableError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except crud.LivreIndisponibleError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except clients.ServiceExterneIndisponibleError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc))


@router.put("/{emprunt_id}/retour", response_model=EmpruntOut)
def retourner_emprunt(
    emprunt_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        return crud.retourner_emprunt(db, emprunt_id, credentials.credentials)
    except crud.EmpruntIntrouvableError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except crud.EmpruntDejaRetourneError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except clients.LivreIntrouvableError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except clients.ServiceExterneIndisponibleError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc))


@router.get("", response_model=list[EmpruntOut])
def lister_emprunts(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return crud.get_emprunts(db)


@router.get("/utilisateur/{utilisateur_id}", response_model=list[EmpruntOut])
def historique_utilisateur(
    utilisateur_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return crud.get_historique_utilisateur(db, utilisateur_id)


@router.get("/retards", response_model=list[EmpruntOut])
def emprunts_en_retard(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return crud.get_emprunts_en_retard(db)
