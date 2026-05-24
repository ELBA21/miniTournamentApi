from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.models.schemas import Inscripcion_schema
from app.models.tables import Inscripcion
from app.crud.factory import crud_inscripcion as crud
from datetime import date

router = APIRouter(
    prefix="/Inscripcion",
    tags=["Inscripciones de Equipos"],
    responses={404: {"descripcion": "No encontrado"}},
)


@router.post("/create", response_model=Inscripcion)
def router_create_inscripcion(
    data: Inscripcion_schema, session: Session = Depends(get_session)
):
    try:
        return crud.create(session, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/all")
def router_get_all(session: Session = Depends(get_session)):
    return crud.get_all(session)


@router.get("/{search_id}")
def router_get_by_id(search_id: int, session: Session = Depends(get_session)):
    try:
        return crud.get_by_id(session, search_id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/anular/{search_id}")
def router_delete(search_id: int, session: Session = Depends(get_session)):
    try:
        return crud.delete(session, search_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
