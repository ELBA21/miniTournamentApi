from sqlmodel import Session, select
from app.models.tables import Jugador, Carrera
from app.models.schemas import JugadorSchema, Jugador_schema_Update
from datetime import date


def create_jugador(session: Session, data: JugadorSchema):
    carrera = session.get(Carrera, data.carrera_id)
    if not carrera:
        return 404

    try:
        nuevo_jugador = Jugador.model_validate(data)

        session.add(nuevo_jugador)
        session.commit()
        session.refresh(nuevo_jugador)
        return nuevo_jugador

    except Exception as e:
        session.rollback()
        print(f"Error al crear jugador: {e}")
        return 500


def get_jugador_all(session: Session):
    return session.exec(select(Jugador)).all()


def get_jugador_byId(session: Session, search_id: int):
    return session.get(Jugador, search_id)


# kwargs son -> Key words arguments
def update_jugador(session: Session, jugador_id: int, data: Jugador_schema_Update):
    # 1. Buscar jugador
    jugador_db = session.get(Jugador, jugador_id)
    if not jugador_db:
        return 404

    try:
        datos_nuevos = data.model_dump(exclude_unset=True)
        jugador_db.sqlmodel_update(datos_nuevos)

        session.add(jugador_db)
        session.commit()
        session.refresh(jugador_db)
        return jugador_db

    except Exception as e:
        session.rollback()
        print(f"Error al actualizar jugador: {e}")
        return 500


def delete_jugador(session: Session, jugador_id: int):
    jugador_db = session.get(Jugador, jugador_id)
    if not jugador_db:
        return 404

    session.delete(jugador_db)
    session.commit()
    return True
