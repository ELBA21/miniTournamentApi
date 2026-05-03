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
    result = create_jugador(session, data)

    # Según tu CRUD: 404 si la Carrera no existe
    if result == 404:
        raise HTTPException(
            status_code=404,
            detail="No se pudo crear el jugador: La Carrera especificada no existe.",
        )

    if result == 500:
        raise HTTPException(
            status_code=500,
            detail="Error interno al crear el jugador en la base de datos.",
        )

    return result


@router.get("/get/all")
def router_get_jugador_all(session: Session = Depends(get_session)):
    result = get_jugador_all(session)
    if not result:
        raise HTTPException(status_code=404, detail="No hay Jugadores")
    return result


@router.get("/get/{search_id}")
def router_get_jugador_byId(search_id: int, session: Session = Depends(get_session)):
    result = get_jugador_byId(session, search_id)
    if not result:
        raise HTTPException(
            status_code=404, detail=f"No se encuentra jugador con id {search_id}"
        )
    return result


@router.patch("/update/{jugador_id}", response_model=Jugador)
def router_patch_jugador(
    jugador_id: int,
    data: Jugador_schema_Update,
    session: Session = Depends(get_session),
):
    result = update_jugador(session, jugador_id, data)

    # 404 si el jugador no existe
    if result == 404:
        raise HTTPException(
            status_code=404, detail=f"Jugador con ID {jugador_id} no encontrado."
        )

    if result == 500:
        raise HTTPException(
            status_code=500,
            detail="Error interno al intentar actualizar los datos del jugador.",
        )

    return result


@router.delete("/delete/{jugador_id}")
def router_delete_jugador(jugador_id: int, session: Session = Depends(get_session)):
    result = delete_jugador(session, jugador_id)
    if result == 404:
        raise HTTPException(status_code=404, detail="No se encontro a jugador")
    return result
