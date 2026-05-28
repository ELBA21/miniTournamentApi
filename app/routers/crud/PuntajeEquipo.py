from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from app.database import get_session
from app.models.schemas import PuntajeEquipo_schema
from app.models.tables import PuntajeEquipo
from app.crud.factory import crud_puntajeEquipo as crud

router = APIRouter(
    prefix="/PuntajeEquipo",
    tags=["Puntajes de Equipos"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/create", response_model=PuntajeEquipo)
def router_create_PuntajeEquipo(
    data: PuntajeEquipo_schema, session: Session = Depends(get_session)
):
    try:
        return crud.create(session, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/all", response_model=List[PuntajeEquipo])
def router_get_puntaje_equipo_all(session: Session = Depends(get_session)):
    # Simplemente devuelve la lista (puede ser una lista vacía [])
    return crud.get_all(session)


@router.get("/{search_id}", response_model=PuntajeEquipo)
def router_get_puntaje_equipo_byId(
    search_id: int, session: Session = Depends(get_session)
):
    try:
        return crud.get_by_id(session, search_id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/update/{search_id}", response_model=PuntajeEquipo)
def router_patch_PuntajeEquipo(
    search_id: int, data: PuntajeEquipo_schema, session: Session = Depends(get_session)
):
    try:
        return crud.update(session, search_id, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete/{search_id}")
def router_delete(search_id: int, session: Session = Depends(get_session)):
    try:
        return crud.delete(session, search_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
