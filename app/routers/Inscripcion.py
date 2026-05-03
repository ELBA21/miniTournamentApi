from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.models.schemas import Inscripcion_schema
from app.models.tables import Inscripcion
from app.crud.Inscripcion import (
    create_inscripcion,
    get_inscripciones_all,
    get_inscripcion_by_id,
    delete_inscripcion,
)
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
    result = create_inscripcion(session, data)

    # En tu lógica, 404 significa que el Equipo o el Torneo_Categoria no existen
    if result == 404:
        raise HTTPException(
            status_code=404,
            detail="No se pudo crear la inscripción: El Equipo o el Torneo_Categoria no existen.",
        )

    # Error de integridad o de conexión
    if result == 500:
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al procesar la inscripción.",
        )

    return result


@router.get("/all")
def router_get_all(session: Session = Depends(get_session)):
    return get_inscripciones_all(session)


@router.get("/{inscripcion_id}")
def router_get_by_id(inscripcion_id: int, session: Session = Depends(get_session)):
    result = get_inscripcion_by_id(session, inscripcion_id)
    if result == 404:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return result


@router.delete("/anular/{inscripcion_id}")
def router_delete(inscripcion_id: int, session: Session = Depends(get_session)):
    result = delete_inscripcion(session, inscripcion_id)
    if result == 404:
        raise HTTPException(
            status_code=404, detail="No se encontró la inscripción para eliminar"
        )
    return {"message": "Inscripción anulada correctamente"}
