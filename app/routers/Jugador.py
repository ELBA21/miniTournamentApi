from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.crud.Jugador import (
    create_jugador,
    get_jugador_all,
    get_jugador_byId,
    update_jugador,
    delete_jugador,
)
from app.models.schemas import JugadorSchema
from datetime import date

router = APIRouter(tags=["Jugador"])


@router.post("/jugador/create")
def router_create_jugador(
    nombre: str,
    puntaje: int,
    generacion: date,
    carrera_id: int,
    session: Session = Depends(get_session),
):
    result = create_jugador(session, nombre, puntaje, generacion, carrera_id)
    if result == 400:
        raise HTTPException(status_code=400, detail="Falta dato")
    if result == 401:
        raise HTTPException(
            status_code=400, detail=f"Id carrera: {carrera_id} invalido"
        )
    return result


@router.get("/jugador/get/all")
def router_get_jugador_all(session: Session = Depends(get_session)):
    result = get_jugador_all(session)
    if not result:
        raise HTTPException(status_code=404, detail="No hay Jugadores")
    return result


@router.get("/jugador/get/{search_id}")
def router_get_jugador_byId(search_id: int, session: Session = Depends(get_session)):
    result = get_jugador_byId(session, search_id)
    if not result:
        raise HTTPException(
            status_code=404, detail=f"No se encuentra jugador con id {search_id}"
        )
    return result


@router.put("/jugador/update/{jugador_id}")
def router_update_jugador(
    jugador_id: int, datos: JugadorSchema, session: Session = Depends(get_session)
):
    datos_dict = datos.model_dump(exclude_unset=True)
    result = update_jugador(session, jugador_id, **datos_dict)
    if result == 404:
        raise HTTPException(status_code=404, detail="No encontrado")
    return result


@router.delete("/jugador/delete/{jugador_id}")
def router_delete_jugador(jugador_id: int, session: Session = Depends(get_session)):
    result = delete_jugador(session, jugador_id)
    if result == 404:
        raise HTTPException(status_code=404, detail="No se encontro a jugador")
    return result
