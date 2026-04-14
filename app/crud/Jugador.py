from sqlmodel import Session, select
from app.models.tables import Jugador, Carrera
from datetime import date


def create_Jugador(
    session: Session,
    nombre: str,
    puntaje: int,
    generacion: date,
    carrera_id: int,
):
    if not nombre or puntaje is None or not generacion or not carrera_id:
        return 400
    carrera = session.get(Carrera, carrera_id)
    if not carrera:
        return 401
    nuevo_jugador = Jugador(
        nombre=nombre, puntaje=puntaje, generacion=generacion, carrera_id=carrera_id
    )
    session.add(nuevo_jugador)
    session.commit()
    session.refresh(nuevo_jugador)

    return nuevo_jugador


def get_jugador_all(session: Session):
    return session.exec(select(Jugador)).all()


def get_jugador_byId(session: Session, search_id: int):
    return session.get(Jugador, search_id)


# kwargs son -> Key words arguments
def update_jugador(session: Session, jugador_id: int, **kwargs):
    jugador_db = session.get(Jugador, jugador_id)
    if not jugador_db:
        return 404

    for key, value in kwargs.items():
        if value is not None:
            setattr(jugador_db, key, value)

    session.add(jugador_db)
    session.commit()
    session.refresh(jugador_db)
    return jugador_db


def delete_jugador(session: Session, jugador_id: int):
    jugador_db = session.get(Jugador, jugador_id)
    if not jugador_db:
        return 404

    session.delete(jugador_db)
    session.commit()
    return True
