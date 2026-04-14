from sqlmodel import Session, select
from app.models.tables import PuntajeEquipo, Partido_Equipo, Seccion


def create_puntaje_equipo(
    session: Session, partido_equipo_id: int, seccion_id: int, puntaje: int
):
    # Validar que ambas partes existan
    pe = session.get(Partido_Equipo, partido_equipo_id)
    sec = session.get(Seccion, seccion_id)

    if not pe or not sec:
        return 404

    nuevo_puntaje = PuntajeEquipo(
        partido_equipo_id=partido_equipo_id, seccion_id=seccion_id, puntaje=puntaje
    )
    session.add(nuevo_puntaje)
    session.commit()
    session.refresh(nuevo_puntaje)
    return nuevo_puntaje


def get_puntajes_all(session: Session):
    return session.exec(select(PuntajeEquipo)).all()


def update_valor_puntaje(session: Session, puntaje_id: int, nuevo_valor: int):
    puntaje_db = session.get(PuntajeEquipo, puntaje_id)
    if not puntaje_db:
        return 404

    puntaje_db.puntaje = nuevo_valor
    session.add(puntaje_db)
    session.commit()
    session.refresh(puntaje_db)
    return puntaje_db


def delete_puntaje(session: Session, puntaje_id: int):
    puntaje_db = session.get(PuntajeEquipo, puntaje_id)
    if not puntaje_db:
        return 404
    session.delete(puntaje_db)
    session.commit()
    return True
