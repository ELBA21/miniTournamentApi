from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.models.schemas import Torneo_schema
from app.models.tables import Torneo
from app.crud.factory import crud_torneo as crud

router = APIRouter(
    prefix="/torneo",
    tags=["Torneo"],
    responses={404: {"description": "Torneo no encontrado"}},
)


@router.post("/create", response_model=Torneo)
def router_create_torneo(data: Torneo_schema, session: Session = Depends(get_session)):
    try:
        return crud.create(session, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/all")
def router_get_torneo_all(session: Session = Depends(get_session)):
    return crud.get_all(session)


@router.get("/{search_id}")
def router_get_torneo_by_id(search_id: int, session: Session = Depends(get_session)):
    try:
        return crud.get_by_id(session, search_id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/update/{search_id}", response_model=Torneo)
def router_patch_torneo(
    search_id: int, data: Torneo_schema, session: Session = Depends(get_session)
):
    try:
        return crud.update(session, search_id, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete/{search_id}")
def router_delete_torneo(search_id: int, session: Session = Depends(get_session)):
    try:
        return crud.delete(session, search_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
