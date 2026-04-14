from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.crud.PuntajeEquipo import (
    create_puntaje_equipo,
    get_puntajes_all,
    update_valor_puntaje,
    delete_puntaje,
)

router = APIRouter(prefix="/PuntajeMarcador", tags=["Marcador por Sección"])


@router.post("/registrar")
def router_registrar_puntaje(
    partido_equipo_id: int,
    seccion_id: int,
    puntaje: int,
    session: Session = Depends(get_session),
):
    result = create_puntaje_equipo(session, partido_equipo_id, seccion_id, puntaje)
    if result == 404:
        raise HTTPException(
            status_code=404, detail="Relación Partido-Equipo o Sección no encontrada"
        )
    return result


@router.get("/all")
def router_get_all(session: Session = Depends(get_session)):
    return get_puntajes_all(session)


@router.put("/update/{puntaje_id}")
def router_update_valor(
    puntaje_id: int, nuevo_valor: int, session: Session = Depends(get_session)
):
    result = update_valor_puntaje(session, puntaje_id, nuevo_valor)
    if result == 404:
        raise HTTPException(status_code=404, detail="Registro de puntaje no encontrado")
    return result


@router.delete("/delete/{puntaje_id}")
def router_delete(puntaje_id: int, session: Session = Depends(get_session)):
    result = delete_puntaje(session, puntaje_id)
    if result == 404:
        raise HTTPException(status_code=404, detail="ID no encontrado")
    return {"message": "Puntaje eliminado correctamente"}
