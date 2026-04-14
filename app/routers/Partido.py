from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.crud.Partido import (
    create_partido,
    get_partido_all,
    get_partido_by_id,
    update_partido_fase,
    delete_partido,
)

router = APIRouter(
    prefix="/Partido",
    tags=["Partido"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/create")
def router_create_partido(fase_id: int, session: Session = Depends(get_session)):
    result = create_partido(session, fase_id)
    if result == 404:
        raise HTTPException(status_code=404, detail="La Fase especificada no existe")
    return result


@router.get("/all")
def router_get_partidos(session: Session = Depends(get_session)):
    return get_partido_all(session)


@router.get("/{partido_id}")
def router_get_partido(partido_id: int, session: Session = Depends(get_session)):
    result = get_partido_by_id(session, partido_id)
    if result == 404:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return result


@router.put("/update-fase/{partido_id}")
def router_update_fase(
    partido_id: int, nueva_fase_id: int, session: Session = Depends(get_session)
):
    result = update_partido_fase(session, partido_id, nueva_fase_id)
    if result == 404:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    if result == 400:
        raise HTTPException(status_code=400, detail="La nueva Fase no es válida")
    return result


@router.delete("/delete/{partido_id}")
def router_delete_partido(partido_id: int, session: Session = Depends(get_session)):
    result = delete_partido(session, partido_id)
    if result == 404:
        raise HTTPException(
            status_code=404, detail="No se pudo eliminar: ID inexistente"
        )
    return {"message": f"Partido {partido_id} eliminado exitosamente"}
