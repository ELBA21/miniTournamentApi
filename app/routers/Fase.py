from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
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


@router.post("/create")
def router_create_fase(
    torneo_categoria_id: int, session: Session = Depends(get_session)
):
    result = create_fase(session, torneo_categoria_id)
    if result == 404:
        raise HTTPException(
            status_code=404, detail="La relación Torneo-Categoría no existe"
        )
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


@router.put("/update/{fase_id}")
def router_update_fase(
    fase_id: int, nuevo_tc_id: int, session: Session = Depends(get_session)
):
    result = update_fase(session, fase_id, nuevo_tc_id)
    if result == 404:
        raise HTTPException(status_code=404, detail="Fase no encontrada")
    if result == 400:
        raise HTTPException(
            status_code=400, detail="El nuevo ID de Torneo-Categoría no es válido"
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
