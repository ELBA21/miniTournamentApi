from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.crud.Partido import (
    create_partido,
    get_partido_all,
    get_partido_by_id,
    update_partido,
    delete_partido,
)
from app.models.tables import Partido
from app.models.schemas import Partido_schema

router = APIRouter(
    prefix="/Partido",
    tags=["Partido"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/create", response_model=Partido)
def router_create_partido(
    data: Partido_schema, session: Session = Depends(get_session)
):
    result = create_partido(session, data)

    # Si la fase no existe
    if result == 404:
        raise HTTPException(
            status_code=404,
            detail="No se pudo crear el partido: La Fase especificada no existe.",
        )

    if result == 500:
        raise HTTPException(
            status_code=500, detail="Error interno del servidor al crear el partido."
        )

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


@router.patch("/update/{partido_id}", response_model=Partido)
def router_patch_partido(
    partido_id: int, data: Partido_schema, session: Session = Depends(get_session)
):
    result = update_partido(session, partido_id, data)

    if result == 404:
        raise HTTPException(
            status_code=404, detail=f"Partido con ID {partido_id} no encontrado."
        )

    if result == 400:
        raise HTTPException(
            status_code=400,
            detail="La Fase proporcionada para la actualización no es válida.",
        )

    if result == 500:
        raise HTTPException(
            status_code=500, detail="Error interno al actualizar el partido."
        )

    return result


@router.delete("/delete/{partido_id}")
def router_delete_partido(partido_id: int, session: Session = Depends(get_session)):
    result = delete_partido(session, partido_id)
    if result == 404:
        raise HTTPException(
            status_code=404, detail="No se pudo eliminar: ID inexistente"
        )
    return {"message": f"Partido {partido_id} eliminado exitosamente"}
