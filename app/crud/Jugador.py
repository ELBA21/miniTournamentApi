from sqlmodel import Session, select
from app.models.tables import Jugador, Carrera
from app.models.schemas import JugadorSchema, Jugador_schema_Update
from datetime import date


def create_jugador(session: Session, data: JugadorSchema):
    carrera = session.get(Carrera, data.carrera_id)
    if not carrera:
        raise LookupError("No hay carrera")
    try:
        nuevo_jugador = Jugador.model_validate(data)

        session.add(nuevo_jugador)
        session.commit()
        session.refresh(nuevo_jugador)
        return nuevo_jugador

    except Exception as e:
        session.rollback()
        raise


def get_jugador_all(session: Session):
    return session.exec(select(Jugador)).all()


def get_jugador_byId(session: Session, search_id: int):
    jugador = session.get(Jugador, search_id)
    if not jugador:
        raise LookupError("Jugador no encontrado")
    return jugador


def update_jugador(session: Session, jugador_id: int, data: Jugador_schema_Update):
    try:
        if not jugador_id:
            raise LookupError("No hay id")
        jugador_db = get_jugador_byId(session, jugador_id)
        if not jugador_db:
            raise LookupError("No existe el jugador")
        datos_nuevos = data.model_dump(exclude_unset=True)
        jugador_db.sqlmodel_update(datos_nuevos)

        session.add(jugador_db)
        session.commit()
        session.refresh(jugador_db)

        return jugador_db
    except Exception as e:
        session.rollback()
        raise


def delete_jugador(session: Session, jugador_id: int):
    try:
        if not jugador_id:
            raise LookupError("No hay id")
        jugador_db = get_jugador_byId(session, jugador_id)
        if not jugador_db:
            raise LookupError("No existe el jugador")
        session.delete(jugador_db)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise
