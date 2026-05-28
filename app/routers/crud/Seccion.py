from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session
from app.database import get_session
from app.models.tables import Seccion_schema
from app.models.tables import Seccion
from app.crud.factory import crud_seccion as crud

router = APIRouter(
    prefix="/Seccion",
    tags=["Sección de Partido"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/create", response_model=Seccion)
def router_create_seccion(
    data: Seccion_schema, session: Session = Depends(get_session)
):
    try:
        return crud.create(session, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/all", response_model=List[Seccion])
def router_get_secciones_all(session: Session = Depends(get_session)):
    # Retorna la lista de todas las secciones
    return crud.get_all(session)


@router.get("/{search_id}", response_model=Seccion)
def router_get_seccion_by_id(search_id: int, session: Session = Depends(get_session)):
    try:
        return crud.get_by_id(session, search_id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/update/{search_id}", response_model=Seccion)
def router_patch_seccion(
    search_id: int, data: Seccion_schema, session: Session = Depends(get_session)
):
    try:
        return crud.update(session, search_id, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete/{search_id}")
def router_delete_seccion(search_id: int, session: Session = Depends(get_session)):
    try:
        return crud.delete(session, search_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
