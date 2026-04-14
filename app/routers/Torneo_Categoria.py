from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.crud.Torneo_Categoria import (
    create_relacion_torneo_categoria,
    get_relaciones_tc_all,
    get_relacion_tc_by_id,
    delete_relacion_torneo_categoria,
)

router = APIRouter(prefix="/TorneoCategoria", tags=["Asignación Torneo-Categoría"])


@router.post("/vincular")
def router_vincular_torneo_categoria(
    torneo_id: int, categoria_id: int, session: Session = Depends(get_session)
):
    result = create_relacion_torneo_categoria(session, torneo_id, categoria_id)
    if result == 404:
        raise HTTPException(
            status_code=404,
            detail="No se pudo crear la relación: Torneo o Categoría no encontrados",
        )
    return result


@router.get("/all")
def router_get_all_tc(session: Session = Depends(get_session)):
    return get_relaciones_tc_all(session)


@router.get("/{tc_id}")
def router_get_tc_by_id(tc_id: int, session: Session = Depends(get_session)):
    result = get_relacion_tc_by_id(session, tc_id)
    if result == 404:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    return result


@router.delete("/desvincular/{tc_id}")
def router_desvincular_torneo_categoria(
    tc_id: int, session: Session = Depends(get_session)
):
    result = delete_relacion_torneo_categoria(session, tc_id)
    if result == 404:
        raise HTTPException(status_code=404, detail="Relación inexistente")
    return {"message": "Categoría removida del torneo con éxito"}
