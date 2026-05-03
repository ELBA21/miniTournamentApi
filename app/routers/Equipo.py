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
from app.models.schemas import Equipo_schema
from app.models.tables import Equipo

router = APIRouter(
    prefix="/Equipo", tags=["Equipo"], responses={404: {"description": "No encontrado"}}
)


@router.post("/create", response_model=Equipo)
def router_create_Equipo(data: Equipo_schema, session: Session = Depends(get_session)):
    result = create_Equipo(session, data)

    # Si el CRUD falló y devolvió el entero 404
    if result == 404:
        raise HTTPException(
            status_code=400, detail="Error al crear: Datos inválidos o conflicto"
        )

    return result


@router.get("/get/{equipo_id}")
def router_get_Equipo_byId(equipo_id: int, session: Session = Depends(get_session)):
    result = get_Equipo_byId(session, equipo_id)
    if result == 400:
        raise HTTPException(status_code=400, detail="Falta datos")
    if result == 404:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return result


@router.patch("/update/{equipo_id}", response_model=Equipo)
def router_patch_Equipo(
    equipo_id: int, data: Equipo_schema, session: Session = Depends(get_session)
):
    result = update_Equipo(session, equipo_id, data)

    # Manejo de respuestas basado en lo que devuelve tu CRUD
    if result == 404:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")

    if result == 500:
        raise HTTPException(
            status_code=500, detail="Error interno del servidor al actualizar"
        )

    return result


@router.delete("/delete/{equipo_id}")
def router_delete_equipo(equipo_id: int, session: Session = Depends(get_session)):
    result = delete_Equipo(session, equipo_id)
    if result == 404:
        raise HTTPException(status_code=404, detail=f"No se ha encontrado {equipo_id}")
    return result
