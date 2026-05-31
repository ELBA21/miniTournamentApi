from fastapi import Depends, HTTPException, APIRouter
from sqlmodel import Session
from app.service.partidos import definir_ganador_partido
from app.database import get_session

router = APIRouter(
    prefix="/partidos",
    tags=["Generador"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/ganador_partido/{partido_id}/{equipo_ganador_id}")
def definir_ganador_partido_router(
    partido_id: int, equipo_ganador_id: int, session: Session = Depends(get_session)
):
    try:
        return definir_ganador_partido(session, partido_id, equipo_ganador_id)
    # Finalmente entiendo como usar cada uno ctm
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
