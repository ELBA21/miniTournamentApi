from sqlmodel import Session, select
from app.models.tables import Jugador_Equipo, Jugador, Equipo


def create_relacion_jugador_equipo(
    session: Session, jugador_id: int, equipo_id: int, puntaje: int = 0
):
    # Validar que existan ambos
    db_jugador = session.get(Jugador, jugador_id)
    db_equipo = session.get(Equipo, equipo_id)

    if not db_jugador or not db_equipo:
        return 404  # Uno de los dos no existe

    nueva_relacion = Jugador_Equipo(
        jugador_id=jugador_id, equipo_id=equipo_id, puntaje=puntaje
    )
    session.add(nueva_relacion)
    session.commit()
    session.refresh(nueva_relacion)
    return nueva_relacion


def get_relaciones_all(session: Session):
    return session.exec(select(Jugador_Equipo)).all()


def update_puntaje_relacion(session: Session, relacion_id: int, nuevo_puntaje: int):
    relacion_db = session.get(Jugador_Equipo, relacion_id)
    if not relacion_db:
        return 404

    relacion_db.puntaje = nuevo_puntaje
    session.add(relacion_db)
    session.commit()
    session.refresh(relacion_db)
    return relacion_db


def delete_relacion(session: Session, relacion_id: int):
    relacion_db = session.get(Jugador_Equipo, relacion_id)
    if not relacion_db:
        return 404
    session.delete(relacion_db)
    session.commit()
    return True
