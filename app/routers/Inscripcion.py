from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.crud.Inscripcion import (
    create_inscripcion,
    get_inscripciones_all,
    get_inscripcion_by_id,
    delete_inscripcion,
)
from datetime import date

router = APIRouter(prefix="/Inscripcion", tags=["Inscripciones de Equipos"])


@router.post("/registrar")
def router_registrar_inscripcion(
    equipo_id: int,
    torneo_categoria_id: int,
    fecha: date | None = None,
    session: Session = Depends(get_session),
):
    result = create_inscripcion(session, equipo_id, torneo_categoria_id, fecha)
    if result == 404:
        raise HTTPException(
            status_code=404, detail="Equipo o Relación Torneo-Categoría no encontrada"
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
