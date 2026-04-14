from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.crud.Seccion import (
    create_seccion,
    get_secciones_all,
    get_seccion_by_id,
    delete_seccion,
)

router = APIRouter(
    prefix="/Seccion",
    tags=["Sección de Partido"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/create")
def router_create_seccion(partido_id: int, session: Session = Depends(get_session)):
    result = create_seccion(session, partido_id)
    if result == 404:
        raise HTTPException(status_code=404, detail="El Partido especificado no existe")
    return result


@router.get("/all")
def router_get_secciones(session: Session = Depends(get_session)):
    return get_secciones_all(session)


@router.get("/{seccion_id}")
def router_get_seccion(seccion_id: int, session: Session = Depends(get_session)):
    result = get_seccion_by_id(session, seccion_id)
    if result == 404:
        raise HTTPException(status_code=404, detail="Sección no encontrada")
    return result


@router.delete("/delete/{seccion_id}")
def router_delete_seccion(seccion_id: int, session: Session = Depends(get_session)):
    result = delete_seccion(session, seccion_id)
    if result == 404:
        raise HTTPException(status_code=404, detail="ID de sección no encontrado")
    return {"message": f"Sección {seccion_id} eliminada"}
