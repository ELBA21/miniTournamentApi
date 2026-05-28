from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.models.tables import Jugador
from app.models.schemas import JugadorSchema, Jugador_schema_Update
from app.crud.factory import crud_jugador as cj

router = APIRouter(
    prefix="/Jugador",
    tags=["Jugador"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/create", response_model=Jugador)
def router_create_jugador(data: JugadorSchema, session: Session = Depends(get_session)):
    try:
        return cj.create(session, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get/all")
def router_get_jugador_all(session: Session = Depends(get_session)):
    result = cj.get_all(session)
    if not result:
        raise HTTPException(status_code=404, detail="No hay Jugadores")
    return result


@router.get("/get/{search_id}")
def router_get_jugador_byId(search_id: int, session: Session = Depends(get_session)):
    try:
        return cj.get_by_id(session, search_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/update/{jugador_id}", response_model=Jugador)
def router_patch_jugador(
    jugador_id: int,
    data: JugadorSchema,
    session: Session = Depends(get_session),
):
    try:
        return cj.update(session, jugador_id, data)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/delete/{jugador_id}")
def router_delete_jugador(jugador_id: int, session: Session = Depends(get_session)):
    try:
        return cj.delete(session, jugador_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
