from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.crud.Equipo import (
    create_Equipo,
    get_Equipo_all,
    get_Equipo_byId,
    update_Equipo,
    delete_Equipo,
)

router = APIRouter(
    prefix="/Equipo", tags=["Equipo"], responses={404: {"description": "No encontrado"}}
)


@router.post("/create")
def router_create_equipo(nombre: str, session: Session = Depends(get_session)):
    result = create_Equipo(session, nombre)
    if result == 400:
        raise HTTPException(status_code=400, detail="Falta dato")
    return result


@router.get("/get/all")
def router_get_Equipo_all(session: Session = Depends(get_session)):
    result = get_Equipo_all(session)
    return result


@router.get("/get/{equipo_id}")
def router_get_Equipo_byId(equipo_id: int, session: Session = Depends(get_session)):
    result = get_Equipo_byId(session, equipo_id)
    if result == 400:
        raise HTTPException(status_code=400, detail="Falta datos")
    if result == 404:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return result


@router.put("/update/{equipo_id}")
def router_update_equipo(
    equipo_id: int, new_nombre: str, session: Session = Depends(get_session)
):
    result = update_Equipo(session, equipo_id, new_nombre)
    if result == 404:
        raise HTTPException(status_code=404, detail=f"Equipo {equipo_id} no encontrado")
    return result


@router.delete("/delete/{equipo_id}")
def router_delete_equipo(equipo_id: int, session: Session = Depends(get_session)):
    result = delete_Equipo(session, equipo_id)
    if result == 404:
        raise HTTPException(status_code=404, detail=f"No se ha encontrado {equipo_id}")
    return result
