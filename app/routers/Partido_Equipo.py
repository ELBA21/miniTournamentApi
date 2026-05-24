from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.models.schemas import Partido_Equipo_schema, Partido_Equipo_schema_update
from app.models.tables import Partido_Equipo
from app.crud.factory import crud_partido_equipo as crud

router = APIRouter(
    prefix="/AsignacionPartido",
    tags=["Asignación Equipo a Partido"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/create", response_model=Partido_Equipo)
def router_create_Partido_Equipo(
    data: Partido_Equipo_schema, session: Session = Depends(get_session)
):
    try:
        return crud.create(session, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/all")
def router_get_all_vinculos(session: Session = Depends(get_session)):
    return crud.get_all(session)


@router.patch("/update/{search_id}", response_model=Partido_Equipo)
def router_patch_Partido_Equipo(
    search_id: int,
    data: Partido_Equipo_schema,
    session: Session = Depends(get_session),
):
    try:
        return crud.update(session, search_id, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/eliminar/{search_id}")
def router_delete_vinculo(search_id: int, session: Session = Depends(get_session)):
    try:
        return crud.delete(session, search_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
