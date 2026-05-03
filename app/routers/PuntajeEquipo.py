from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from app.database import get_session
from app.models.schemas import PuntajeEquipo_schema
from app.models.tables import PuntajeEquipo
from app.crud.PuntajeEquipo import (
    create_puntaje_equipo,
    get_puntaje_equipo_all,
    get_puntaje_equipo_byId,
    update_puntaje_equipo,
    delete_puntaje,
)

router = APIRouter(
    prefix="/PuntajeEquipo",
    tags=["Puntajes de Equipos"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/create", response_model=PuntajeEquipo)
def router_create_PuntajeEquipo(
    data: PuntajeEquipo_schema, session: Session = Depends(get_session)
):
    result = create_puntaje_equipo(session, data)

    # Si no existe la relación partido-equipo o la sección
    if result == 404:
        raise HTTPException(
            status_code=404,
            detail="No se pudo registrar el puntaje: La relación Partido-Equipo o la Sección no existen.",
        )

    if result == 500:
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al registrar el puntaje.",
        )

    return result


@router.get("/all", response_model=List[PuntajeEquipo])
def router_get_puntaje_equipo_all(session: Session = Depends(get_session)):
    # Simplemente devuelve la lista (puede ser una lista vacía [])
    return get_puntaje_equipo_all(session)


@router.get("/{search_id}", response_model=PuntajeEquipo)
def router_get_puntaje_equipo_byId(
    search_id: int, session: Session = Depends(get_session)
):
    result = get_puntaje_equipo_byId(session, search_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró el registro de puntaje con ID {search_id}",
        )

    return result


@router.patch("/update/{puntaje_id}", response_model=PuntajeEquipo)
def router_patch_PuntajeEquipo(
    puntaje_id: int, data: PuntajeEquipo_schema, session: Session = Depends(get_session)
):
    result = update_puntaje_equipo(session, puntaje_id, data)

    # 1. El registro de puntaje específico no existe
    if result == 404:
        raise HTTPException(
            status_code=404,
            detail=f"Registro de puntaje con ID {puntaje_id} no encontrado.",
        )

    # 2. Las nuevas FKs proporcionadas no son válidas
    if result == 400:
        raise HTTPException(
            status_code=400,
            detail="Los IDs de Partido-Equipo o Sección proporcionados para la actualización no son válidos.",
        )

    if result == 500:
        raise HTTPException(
            status_code=500, detail="Error interno al actualizar el puntaje."
        )

    return result


@router.delete("/delete/{puntaje_id}")
def router_delete(puntaje_id: int, session: Session = Depends(get_session)):
    result = delete_puntaje(session, puntaje_id)
    if result == 404:
        raise HTTPException(status_code=404, detail="ID no encontrado")
    return {"message": "Puntaje eliminado correctamente"}
