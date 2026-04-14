from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.crud.Torneo import (
    create_torneo,
    get_torneo_all,
    get_torneo_by_id,
    update_torneo,
    delete_torneo,
)
from datetime import date

router = APIRouter(
    prefix="/Torneo",
    tags=["Torneo"],
    responses={404: {"description": "Torneo no encontrado"}},
)


@router.post("/create")
def router_create_torneo(
    nombre: str, fecha: date, session: Session = Depends(get_session)
):
    result = create_torneo(session, nombre, fecha)
    if result == 400:
        raise HTTPException(status_code=400, detail="Nombre y fecha son requeridos")
    return result


@router.get("/all")
def router_get_torneo_all(session: Session = Depends(get_session)):
    return get_torneo_all(session)


@router.get("/{torneo_id}")
def router_get_torneo_by_id(torneo_id: int, session: Session = Depends(get_session)):
    result = get_torneo_by_id(session, torneo_id)
    if result == 404:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")
    return result


@router.put("/update/{torneo_id}")
def router_update_torneo(
    torneo_id: int,
    nombre: str | None = None,
    fecha: date | None = None,
    session: Session = Depends(get_session),
):
    result = update_torneo(session, torneo_id, nombre, fecha)
    if result == 404:
        raise HTTPException(
            status_code=404, detail="No se encontró el torneo para actualizar"
        )
    return result


@router.delete("/delete/{torneo_id}")
def router_delete_torneo(torneo_id: int, session: Session = Depends(get_session)):
    result = delete_torneo(session, torneo_id)
    if result == 404:
        raise HTTPException(
            status_code=404, detail="Torneo no encontrado para eliminar"
        )
    return {"message": "Torneo eliminado con éxito"}
