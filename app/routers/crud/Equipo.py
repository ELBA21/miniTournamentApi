from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.crud.factory import crud_equipo as crud
from app.models.schemas import Equipo_schema
from app.models.tables import Equipo

router = APIRouter(
    prefix="/Equipo",
    tags=["Equipo"],
    responses={404: {"description": "Equipo no encontrado"}},
)


@router.post("/create", response_model=Equipo)
def router_create_Equipo(data: Equipo_schema, session: Session = Depends(get_session)):
    try:
        return crud.create(session, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get/all")
def router_get_Equipo_all(session: Session = Depends(get_session)):
    return crud.get_all(session)


@router.get("/get/{search_id}")
def router_get_Equipo_byId(search_id: int, session: Session = Depends(get_session)):
    try:
        return crud.get_by_id(session, search_id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/update/{search_id}", response_model=Equipo)
def router_patch_Equipo(
    search_id: int, data: Equipo_schema, session: Session = Depends(get_session)
):
    try:
        return crud.update(session, search_id, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete/{search_id}")
def router_delete_equipo(search_id: int, session: Session = Depends(get_session)):
    try:
        return crud.delete(session, search_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
