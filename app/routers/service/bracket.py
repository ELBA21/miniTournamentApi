# routers/service/bracket.py
from fastapi import Depends, HTTPException, APIRouter
from sqlmodel import Session
from app.service.bracket import get_bracket
from app.database import get_session

router = APIRouter(
    prefix="/bracket",
    tags=["Generador"],
    responses={404: {"description": "No encontrado"}},
)


@router.get("/{torneo_categoria_id}")
def get_bracket_router(
    torneo_categoria_id: int, session: Session = Depends(get_session)
):
    try:
        return get_bracket(session, torneo_categoria_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
