from sqlmodel import Session, select
from app.models.tables import Partido, Fase


def create_partido(session: Session, fase_id: int):
    # Validar que la fase exista
    db_fase = session.get(Fase, fase_id)
    if not db_fase:
        return 404

    nuevo_partido = Partido(fase_id=fase_id)
    session.add(nuevo_partido)
    session.commit()
    session.refresh(nuevo_partido)
    return nuevo_partido


def get_partido_all(session: Session):
    return session.exec(select(Partido)).all()


def get_partido_by_id(session: Session, partido_id: int):
    partido = session.get(Partido, partido_id)
    return partido if partido else 404


def update_partido_fase(session: Session, partido_id: int, nueva_fase_id: int):
    partido_db = session.get(Partido, partido_id)
    if not partido_db:
        return 404

    # Validar que la nueva fase exista
    db_fase = session.get(Fase, nueva_fase_id)
    if not db_fase:
        return 400

    partido_db.fase_id = nueva_fase_id
    session.add(partido_db)
    session.commit()
    session.refresh(partido_db)
    return partido_db


def delete_partido(session: Session, partido_id: int):
    partido_db = session.get(Partido, partido_id)
    if not partido_db:
        return 404
    session.delete(partido_db)
    session.commit()
    return True
