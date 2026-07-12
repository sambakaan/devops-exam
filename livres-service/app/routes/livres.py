from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud
from app.auth import get_current_user
from app.database import get_db
from app.schemas import LivreCreate, LivreOut, LivreUpdate

router = APIRouter(prefix="/livres", tags=["livres"])


@router.post("", response_model=LivreOut, status_code=status.HTTP_201_CREATED)
def create_livre(
    livre: LivreCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return crud.create_livre(db, livre)
    except crud.IsbnDejaUtiliseError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/search", response_model=list[LivreOut])
def search_livres(
    q: str = Query(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return crud.search_livres(db, q)


@router.get("", response_model=list[LivreOut])
def list_livres(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return crud.get_livres(db, skip, limit)


@router.get("/{livre_id}", response_model=LivreOut)
def get_livre(livre_id: UUID, db: Session = Depends(get_db)):
    livre = crud.get_livre(db, livre_id)
    if livre is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livre introuvable")
    return livre


@router.put("/{livre_id}", response_model=LivreOut)
def update_livre(
    livre_id: UUID,
    livre_update: LivreUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    livre = crud.update_livre(db, livre_id, livre_update)
    if livre is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livre introuvable")
    return livre


@router.delete("/{livre_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_livre(
    livre_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    deleted = crud.delete_livre(db, livre_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livre introuvable")
