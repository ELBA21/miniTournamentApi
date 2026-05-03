from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.models.schemas import Fase_schema
from app.models.tables import Fase
from app.crud.Fase import (
    create_fase,
    get_fase_all,
    get_fase_by_id,
    update_fase,
    delete_fase,
)

router = APIRouter(
    prefix="/Fase", tags=["Fase"], responses={404: {"description": "No encontrado"}}
)


@router.post("/create", response_model=Fase)
def router_create_fase(data: Fase_schema, session: Session = Depends(get_session)):
    result = create_fase(session, data)

    if result == 404:
        # En el create, el 404 significa que el Torneo_Categoria no existe
        raise HTTPException(status_code=404, detail="Torneo_Categoria no encontrado")

    if result == 500:
        raise HTTPException(status_code=500, detail="Error interno al crear la fase")

    return result


@router.get("/all")
def router_get_fase_all(session: Session = Depends(get_session)):
    return get_fase_all(session)


@router.get("/{fase_id}")
def router_get_fase_by_id(fase_id: int, session: Session = Depends(get_session)):
    result = get_fase_by_id(session, fase_id)
    if result == 404:
        raise HTTPException(status_code=404, detail="Fase no encontrada")
    return result


@router.patch("/update/{fase_id}", response_model=Fase)
def router_patch_fase(
    fase_id: int, data: Fase_schema, session: Session = Depends(get_session)
):
    result = update_fase(session, fase_id, data)

    if result == 404:
        raise HTTPException(status_code=404, detail="Fase no encontrada")

    if result == 400:
        raise HTTPException(
            status_code=400, detail="El ID de Torneo_Categoria proporcionado no existe"
        )

    if result == 500:
        raise HTTPException(
            status_code=500, detail="Error interno al actualizar la fase"
        )

    return result


@router.delete("/delete/{fase_id}")
def router_delete_fase(fase_id: int, session: Session = Depends(get_session)):
    result = delete_fase(session, fase_id)
    if result == 404:
        raise HTTPException(
            status_code=404, detail="No se encontró la fase para eliminar"
        )
    return {"message": f"Fase {fase_id} eliminada"}
