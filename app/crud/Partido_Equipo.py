from sqlmodel import Session, select
from app.models.tables import Partido_Equipo, Equipo, Partido


def create_partido_equipo(
    session: Session, equipo_id: int, partido_id: int, ganador: bool = False
):
    # Validar integridad referencial
    db_equipo = session.get(Equipo, equipo_id)
    db_partido = session.get(Partido, partido_id)

    if not db_equipo or not db_partido:
        return 404

    nueva_relacion = Partido_Equipo(
        equipo_id=equipo_id, partido_id=partido_id, ganador=ganador
    )
    session.add(nueva_relacion)
    session.commit()
    session.refresh(nueva_relacion)
    return nueva_relacion


def get_partido_equipo_all(session: Session):
    return session.exec(select(Partido_Equipo)).all()


def update_resultado_partido(session: Session, pe_id: int, es_ganador: bool):
    pe_db = session.get(Partido_Equipo, pe_id)
    if not pe_db:
        return 404

    pe_db.ganador = es_ganador
    session.add(pe_db)
    session.commit()
    session.refresh(pe_db)
    return pe_db


def delete_partido_equipo(session: Session, pe_id: int):
    pe_db = session.get(Partido_Equipo, pe_id)
    if not pe_db:
        return 404
    session.delete(pe_db)
    session.commit()
    return True
