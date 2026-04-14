from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.crud.Partido_Equipo import (
    create_partido_equipo,
    get_partido_equipo_all,
    update_resultado_partido,
    delete_partido_equipo,
)

router = APIRouter(prefix="/AsignacionPartido", tags=["Asignación Equipo a Partido"])


@router.post("/vincular")
def router_vincular_equipo_partido(
    equipo_id: int,
    partido_id: int,
    ganador: bool = False,
    session: Session = Depends(get_session),
):
    result = create_partido_equipo(session, equipo_id, partido_id, ganador)
    if result == 404:
        raise HTTPException(status_code=404, detail="Equipo o Partido no encontrado")
    return result


@router.get("/all")
def router_get_all_vinculos(session: Session = Depends(get_session)):
    return get_partido_equipo_all(session)


@router.put("/definir-ganador/{pe_id}")
def router_set_ganador(
    pe_id: int, es_ganador: bool, session: Session = Depends(get_session)
):
    result = update_resultado_partido(session, pe_id, es_ganador)
    if result == 404:
        raise HTTPException(
            status_code=404, detail="Registro de partido_equipo no encontrado"
        )
    return result


@router.delete("/eliminar/{pe_id}")
def router_delete_vinculo(pe_id: int, session: Session = Depends(get_session)):
    result = delete_partido_equipo(session, pe_id)
    if result == 404:
        raise HTTPException(status_code=404, detail="ID no encontrado")
    return {"message": "Vínculo eliminado correctamente"}
