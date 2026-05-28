from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session

from app.service.tournament import (
    generar_rondas_para_torneo_categoria as generador_fases,
)


router = APIRouter(
    prefix="/service", tags=["Generador"], responses={404: {"description": "Error"}}
)


@router.post("/generar_fases")
def generar_fases_router(
    torneo_categoria_id: int, session: Session = Depends(get_session)
):
    try:
        return generador_fases(torneo_categoria_id, session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
