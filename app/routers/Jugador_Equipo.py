from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.crud.Jugador_Equipo import (
    create_relacion_jugador_equipo,
    get_relaciones_all,
    get_relaciones_byId,
    update_puntaje_relacion,
    delete_relacion,
)
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
    result = create_relacion_jugador_equipo(session, data)

    # En tu lógica, 404 significa que el Jugador o el Equipo no existen
    if result == 404:
        raise HTTPException(
            status_code=404,
            detail="No se pudo crear la relación: El Jugador o el Equipo no existen.",
        )

    if result == 500:
        raise HTTPException(
            status_code=500, detail="Error interno al procesar la asignación."
        )

    return result


@router.get("/get/all")
def router_get_all_asignaciones(session: Session = Depends(get_session)):
    return get_relaciones_all(session)


@router.get("/get/byId/{search_id}")
def router_get_relaciones_byId(search_id: int, session: Session = Depends(get_session)):
    return get_relaciones_byId(session, search_id)


@router.patch("/update/{relacion_id}", response_model=Jugador_Equipo)
def router_patch_Jugador_Equipo(
    relacion_id: int,
    data: Jugador_Equipo_schema_update,
    session: Session = Depends(get_session),
):
    result = update_puntaje_relacion(session, relacion_id, data)

    # 404 si el ID de la tabla intermedia no existe
    if result == 404:
        raise HTTPException(
            status_code=404, detail=f"Asignación con ID {relacion_id} no encontrada."
        )

    if result == 500:
        raise HTTPException(
            status_code=500,
            detail="Error interno al intentar actualizar el puntaje de la asignación.",
        )

    return result


@router.delete("/separar/{relacion_id}")
def router_delete_relacion(relacion_id: int, session: Session = Depends(get_session)):
    result = delete_relacion(session, relacion_id)
    if result == 404:
        raise HTTPException(status_code=404, detail="No se pudo eliminar: ID no existe")
    return {"message": "Jugador removido del equipo"}
