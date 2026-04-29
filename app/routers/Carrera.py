from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.models.schemas import Carrera_schema
from app.crud.Carrera import (
    create_carrera,
    get_carrera_all,
    get_carrera_byId,
    update_nombre_carrera,
    delete_carrera,
)

router = APIRouter(tags=["Carrera"])


@router.post("/carrera/create")
def router_create_carrera(
    data: Carrera_schema, session: Session = Depends(get_session)
):
    result = create_carrera(session, data)
    if result == 400:
        raise HTTPException(status_code=400, detail="Falta dato o es invalido")
    if result == 404:
        raise HTTPException(status_code=404, detail="Error")
    return result


@router.get("/carrera/get/all")
def router_get_carrera_all(session: Session = Depends(get_session)):
    return get_carrera_all(session)


@router.get("/carrera/get/{carrera_id}")
def router_get_carrera_byId(carrera_id: int, session: Session = Depends(get_session)):
    return get_carrera_byId(session, carrera_id)


@router.put("/carrera/update/{carrera_id}")
def router_update_nombre_carrera(
    carrera_id: int, data: Carrera_schema, session: Session = Depends(get_session)
):
    result = update_nombre_carrera(session, carrera_id, data)
    if result == 404:
        raise HTTPException(status_code=404, detail="Dato faltante")
    if result == 500:
        raise HTTPException(
            status_code=500,
            detail=f"No se pudo actualizar: La carrera con ID {carrera_id} no existe",
        )
    return result


@router.delete("/carrera/delete/{carrera_id}")
def router_delete_carrera(carrera_id: int, session: Session = Depends(get_session)):
    result = delete_carrera(session, carrera_id)
    if result == 400:
        raise HTTPException(status_code=400, detail="Dato faltante")
    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"No se pudo eliminar: La carrera con ID {carrera_id} no se encontro",
        )
    return {"message": f"Carrera con ID {carrera_id} eliminada"}
