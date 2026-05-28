from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.crud.factory import crud_partido as crud
from app.models.tables import Partido
from app.models.schemas import Partido_schema

router = APIRouter(
    prefix="/Partido",
    tags=["Partido"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/create", response_model=Partido)
def router_create_partido(
    data: Partido_schema, session: Session = Depends(get_session)
):
    try:
        return crud.create(session, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get/all")
def router_get_partidos(session: Session = Depends(get_session)):
    return crud.get_all(session)


@router.get("/get/{search_id}")
def router_get_partido(search_id: int, session: Session = Depends(get_session)):
    try:
        return crud.get_by_id(session, search_id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/update/{search_id}", response_model=Partido)
def router_patch_partido(
    search_id: int, data: Partido_schema, session: Session = Depends(get_session)
):
    try:
        return crud.update(session, search_id, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete/{search_id}")
def router_delete_partido(search_id: int, session: Session = Depends(get_session)):
    try:
        return crud.delete(session, search_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
