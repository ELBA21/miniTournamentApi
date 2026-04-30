from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.crud.Categoria import (
    create_categoria,
    get_categoria_all,
    get_categoria_by_id,
    update_categoria,
    delete_categoria,
)
from app.models.schemas import Categoria_schema

router = APIRouter(
    prefix="/Categoria",
    tags=["Categoría"],
    responses={404: {"description": "Categoría no encontrada"}},
)


@router.post("/create")
def router_create_categoria(
    data: Categoria_schema, session: Session = Depends(get_session)
):
    result = create_categoria(session, data)
    if result == 400:
        raise HTTPException(status_code=400, detail="Falta dato o es invalido")
    if result == 404:
        raise HTTPException(status_code=404, detail="Error")
    return result


@router.get("/all")
def router_get_categoria_all(session: Session = Depends(get_session)):
    return get_categoria_all(session)


@router.get("/{categoria_id}")
def router_get_categoria_by_id(
    categoria_id: int, session: Session = Depends(get_session)
):
    result = get_categoria_by_id(session, categoria_id)
    if result == 404:
        raise HTTPException(status_code=404, detail="ID de categoría no encontrado")
    return result


@router.put("/update/{categoria_id}")
def router_update_categoria(
    categoria_id: int, data: Categoria_schema, session: Session = Depends(get_session)
):
    result = update_categoria(session, categoria_id, data)
    if result == 404:
        raise HTTPException(status_code=404, detail="Dato faltante")
    if result == 500:
        raise HTTPException(
            status_code=500,
            detail=f"No se pudo actualizar: La carrera con ID {categoria_id} no existe",
        )
    return result


@router.delete("/delete/{categoria_id}")
def router_delete_categoria(categoria_id: int, session: Session = Depends(get_session)):
    result = delete_categoria(session, categoria_id)
    if result == 404:
        raise HTTPException(
            status_code=404, detail="No se pudo eliminar: ID inexistente"
        )
    return {"message": f"Categoría {categoria_id} eliminada correctamente"}
