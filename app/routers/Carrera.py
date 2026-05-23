from fastapi import APIRouter, Depends, HTTPException, status
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
    try:
        return create_carrera(session, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/carrera/get/all")
def router_get_carrera_all(session: Session = Depends(get_session)):
    return get_carrera_all(session)


@router.get("/carrera/get/{carrera_id}")
def router_get_carrera_byId(carrera_id: int, session: Session = Depends(get_session)):
    try:
        return get_carrera_byId(session, carrera_id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/carrera/update/{carrera_id}")
def router_update_nombre_carrera(
    carrera_id: int, data: Carrera_schema, session: Session = Depends(get_session)
):
    try:
        return update_nombre_carrera(session, carrera_id, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/carrera/delete/{carrera_id}")
def router_delete_carrera(carrera_id: int, session: Session = Depends(get_session)):
    try:
        return delete_carrera(session, carrera_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
