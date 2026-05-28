from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.models.schemas import Torneos_Categorias_schema
from app.models.tables import Torneo_Categoria
from app.crud.factory import crud_torneo_categoria as crud

router = APIRouter(
    prefix="/TorneoCategoria",
    tags=["Relación Torneo-Categoría"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/create", response_model=Torneo_Categoria)
def router_create_Torneo_Categoria(
    data: Torneos_Categorias_schema, session: Session = Depends(get_session)
):
    try:
        return crud.create(session, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/all")
def router_get_all_tc(session: Session = Depends(get_session)):
    return crud.get_all(session)


@router.get("/{search_id}")
def router_get_tc_by_id(search_id: int, session: Session = Depends(get_session)):
    try:
        return crud.get_by_id(session, search_id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/desvincular/{search_id}")
def router_desvincular_torneo_categoria(
    search_id: int, session: Session = Depends(get_session)
):
    try:
        return crud.delete(session, search_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
