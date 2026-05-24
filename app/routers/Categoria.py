from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.models.schemas import Categoria_schema
from app.crud.factory import crud_categoria as cc

router = APIRouter(
    prefix="/Categoria",
    tags=["Categoría"],
    responses={404: {"description": "Categoría no encontrada"}},
)


@router.post("/create")
def router_create_categoria(
    data: Categoria_schema, session: Session = Depends(get_session)
):
    try:
        return cc.create(session, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/all")
def router_get_categoria_all(session: Session = Depends(get_session)):
    return cc.get_all(session)


@router.get("/{categoria_id}")
def router_get_categoria_by_id(
    categoria_id: int, session: Session = Depends(get_session)
):
    try:
        return cc.get_by_id(session, categoria_id)
    except LookupError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/update/{categoria_id}")
def router_update_categoria(
    categoria_id: int, data: Categoria_schema, session: Session = Depends(get_session)
):
    try:
        return cc.update(session, categoria_id, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete/{categoria_id}")
def router_delete_categoria(categoria_id: int, session: Session = Depends(get_session)):
    try:
        return cc.delete(session, categoria_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
