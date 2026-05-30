from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session

from app.service.tournament import (
    generar_rondas_para_torneo_categoria as generador_fases,
    inicializar_torneo,
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


@router.post("/asignar_partidos")
def inicializar_torneo_router(
    torneo_categoria_id: int, session: Session = Depends(get_session)
):
    try:
        return inicializar_torneo(torneo_categoria_id, session)
    # Finalmente entiendo como usar cada uno ctm
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
