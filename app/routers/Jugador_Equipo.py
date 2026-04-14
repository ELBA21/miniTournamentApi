from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.crud.Jugador_Equipo import (
    create_relacion_jugador_equipo,
    get_relaciones_all,
    update_puntaje_relacion,
    delete_relacion,
)

router = APIRouter(prefix="/Asignacion", tags=["Asignación Jugador-Equipo"])


@router.post("/unir")
def router_unir_jugador_equipo(
    jugador_id: int,
    equipo_id: int,
    puntaje: int = 0,
    session: Session = Depends(get_session),
):
    result = create_relacion_jugador_equipo(session, jugador_id, equipo_id, puntaje)
    if result == 404:
        raise HTTPException(status_code=404, detail="Jugador o Equipo no encontrado")
    return result


@router.get("/all")
def router_get_all_asignaciones(session: Session = Depends(get_session)):
    return get_relaciones_all(session)


@router.put("/update-puntaje/{relacion_id}")
def router_update_puntaje(
    relacion_id: int, nuevo_puntaje: int, session: Session = Depends(get_session)
):
    result = update_puntaje_relacion(session, relacion_id, nuevo_puntaje)
    if result == 404:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    return result


@router.delete("/separar/{relacion_id}")
def router_delete_relacion(relacion_id: int, session: Session = Depends(get_session)):
    result = delete_relacion(session, relacion_id)
    if result == 404:
        raise HTTPException(status_code=404, detail="No se pudo eliminar: ID no existe")
    return {"message": "Jugador removido del equipo"}
