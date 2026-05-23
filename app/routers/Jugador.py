from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.models.tables import Jugador
from app.models.schemas import JugadorSchema, Jugador_schema_Update
from app.crud.Jugador import (
    create_jugador,
    get_jugador_all,
    get_jugador_byId,
    update_jugador,
    delete_jugador,
)

router = APIRouter(
    prefix="/Jugador",
    tags=["Jugador"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/create", response_model=Jugador)
def router_create_jugador(data: JugadorSchema, session: Session = Depends(get_session)):
    try:
        return create_jugador(session, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get/all")
def router_get_jugador_all(session: Session = Depends(get_session)):
    result = get_jugador_all(session)
    if not result:
        raise HTTPException(status_code=404, detail="No hay Jugadores")
    return result


@router.get("/get/{search_id}")
def router_get_jugador_byId(search_id: int, session: Session = Depends(get_session)):
    try:
        return get_jugador_byId(session, search_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/update/{jugador_id}", response_model=Jugador)
def router_patch_jugador(
    jugador_id: int,
    data: Jugador_schema_Update,
    session: Session = Depends(get_session),
):
    try:
        return update_jugador(session, jugador_id, data)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/delete/{jugador_id}")
def router_delete_jugador(jugador_id: int, session: Session = Depends(get_session)):
    try:
        return delete_jugador(session, jugador_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
