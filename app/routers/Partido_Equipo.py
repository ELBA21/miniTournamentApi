from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.models.schemas import Partido_Equipo_schema, Partido_Equipo_schema_update
from app.models.tables import Partido_Equipo
from app.crud.Partido_Equipo import (
    create_partido_equipo,
    get_partido_equipo_all,
    update_partido_equipo,
    delete_partido_equipo,
)

router = APIRouter(
    prefix="/AsignacionPartido",
    tags=["Asignación Equipo a Partido"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/create", response_model=Partido_Equipo)
def router_create_Partido_Equipo(
    data: Partido_Equipo_schema, session: Session = Depends(get_session)
):
    result = create_partido_equipo(session, data)

    # Si falla una de las Foreign Keys (Equipo o Partido no existen)
    if result == 404:
        raise HTTPException(
            status_code=404,
            detail="No se pudo crear la asignación: El Equipo o el Partido no existen.",
        )

    if result == 500:
        raise HTTPException(
            status_code=500,
            detail="Error interno al procesar la asignación del equipo al partido.",
        )

    return result


@router.get("/all")
def router_get_all_vinculos(session: Session = Depends(get_session)):
    return get_partido_equipo_all(session)


@router.patch("/update/{pe_id}", response_model=Partido_Equipo)
def router_patch_Partido_Equipo(
    pe_id: int,
    data: Partido_Equipo_schema_update,
    session: Session = Depends(get_session),
):
    result = update_partido_equipo(session, pe_id, data)

    # Si la relación ID no existe en la tabla intermedia
    if result == 404:
        raise HTTPException(
            status_code=404,
            detail=f"Relación Partido-Equipo con ID {pe_id} no encontrada.",
        )

    if result == 500:
        raise HTTPException(
            status_code=500,
            detail="Error interno al intentar actualizar los datos de la relación.",
        )

    return result


@router.delete("/eliminar/{pe_id}")
def router_delete_vinculo(pe_id: int, session: Session = Depends(get_session)):
    result = delete_partido_equipo(session, pe_id)
    if result == 404:
        raise HTTPException(status_code=404, detail="ID no encontrado")
    return {"message": "Vínculo eliminado correctamente"}
