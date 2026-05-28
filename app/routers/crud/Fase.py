from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.models.schemas import Fase_schema
from app.models.tables import Fase
from app.crud.factory import crud_fase as crud

router = APIRouter(
    prefix="/Fase", tags=["Fase"], responses={404: {"description": "No encontrado"}}
)


@router.post("/create", response_model=Fase)
def router_create_fase(data: Fase_schema, session: Session = Depends(get_session)):
    try:
        return crud.create(session, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/all")
def router_get_fase_all(session: Session = Depends(get_session)):
    return crud.get_all(session)


@router.get("/{search_id}")
def router_get_fase_by_id(search_id: int, session: Session = Depends(get_session)):
    try:
        return crud.get_by_id(session, search_id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/update/{search_id}", response_model=Fase)
def router_patch_fase(
    search_id: int, data: Fase_schema, session: Session = Depends(get_session)
):
    try:
        return crud.update(session, search_id, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete/{search_id}")
def router_delete_fase(search_id: int, session: Session = Depends(get_session)):
    try:
        return crud.delete(session, search_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
