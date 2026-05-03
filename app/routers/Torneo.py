from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.models.schemas import Torneo_schema
from app.models.tables import Torneo
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


@router.post("/create", response_model=Torneo)
def router_create_torneo(data: Torneo_schema, session: Session = Depends(get_session)):
    result = create_torneo(session, data)

    # En el create de Torneo, si falla, es un error de servidor (500)
    if result == 500:
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al intentar crear el torneo.",
        )

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


@router.patch("/update/{torneo_id}", response_model=Torneo)
def router_patch_torneo(
    torneo_id: int, data: Torneo_schema, session: Session = Depends(get_session)
):
    result = update_torneo(session, torneo_id, data)

    # Si el ID del torneo no existe
    if result == 404:
        raise HTTPException(
            status_code=404, detail=f"Torneo con ID {torneo_id} no encontrado."
        )

    # Si falló la actualización por un error de BD
    if result == 500:
        raise HTTPException(
            status_code=500, detail="Error interno al intentar actualizar el torneo."
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
