from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.crud.factory import crud_jugador_equipo as crud
from app.models.schemas import Jugador_Equipo_schema, Jugador_Equipo_schema_update
from app.models.tables import Jugador_Equipo

router = APIRouter(
    prefix="/JugadorEquipo",
    tags=["Asignación Jugador-Equipo"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/create", response_model=Jugador_Equipo)
def router_create_Jugador_Equipo(
    data: Jugador_Equipo_schema, session: Session = Depends(get_session)
):
    try:
        return crud.create(session, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get/all")
def router_get_all_asignaciones(session: Session = Depends(get_session)):
    return crud.get_all(session)


@router.get("/get/byId/{search_id}")
def router_get_relaciones_byId(search_id: int, session: Session = Depends(get_session)):
    try:
        return crud.get_by_id(session, search_id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/update/{search_id}", response_model=Jugador_Equipo)
def router_patch_Jugador_Equipo(
    search_id: int,
    data: Jugador_Equipo_schema,
    session: Session = Depends(get_session),
):
    try:
        return crud.update(session, search_id, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/separar/{search_id}")
def router_delete_relacion(search_id: int, session: Session = Depends(get_session)):
    try:
        return crud.delete(session, search_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
