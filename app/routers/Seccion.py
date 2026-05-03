from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session
from app.database import get_session
from app.crud.Seccion import (
    create_seccion,
    get_secciones_all,
    get_seccion_by_id,
    update_seccion,
    delete_seccion,
)
from app.models.tables import Seccion_schema
from app.models.tables import Seccion

router = APIRouter(
    prefix="/Seccion",
    tags=["Sección de Partido"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/create", response_model=Seccion)
def router_create_seccion(
    data: Seccion_schema, session: Session = Depends(get_session)
):
    result = create_seccion(session, data)

    # Si el partido asociado no existe
    if result == 404:
        raise HTTPException(
            status_code=404,
            detail="No se pudo crear la sección: El Partido asociado no existe.",
        )

    if result == 500:
        raise HTTPException(
            status_code=500, detail="Error interno al crear la sección."
        )

    return result


@router.get("/all", response_model=List[Seccion])
def router_get_secciones_all(session: Session = Depends(get_session)):
    # Retorna la lista de todas las secciones
    return get_secciones_all(session)


@router.get("/{seccion_id}", response_model=Seccion)
def router_get_seccion_by_id(seccion_id: int, session: Session = Depends(get_session)):
    result = get_seccion_by_id(session, seccion_id)

    # Capturamos el 404 que devuelve tu función CRUD
    if result == 404:
        raise HTTPException(
            status_code=404, detail=f"Sección con ID {seccion_id} no encontrada."
        )

    return result


@router.patch("/update/{seccion_id}", response_model=Seccion)
def router_patch_seccion(
    seccion_id: int, data: Seccion_schema, session: Session = Depends(get_session)
):
    result = update_seccion(session, seccion_id, data)

    # 1. La sección no existe
    if result == 404:
        raise HTTPException(
            status_code=404, detail=f"Sección con ID {seccion_id} no encontrada."
        )

    # 2. El partido nuevo al que se quiere mover no existe
    if result == 400:
        raise HTTPException(
            status_code=400,
            detail="El partido_id proporcionado para la actualización no existe.",
        )

    if result == 500:
        raise HTTPException(
            status_code=500, detail="Error interno al actualizar la sección."
        )

    return result


@router.delete("/delete/{seccion_id}")
def router_delete_seccion(seccion_id: int, session: Session = Depends(get_session)):
    result = delete_seccion(session, seccion_id)
    if result == 404:
        raise HTTPException(status_code=404, detail="ID de sección no encontrado")
    return {"message": f"Sección {seccion_id} eliminada"}
