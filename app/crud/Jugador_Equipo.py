from sqlmodel import Session, select
from app.models.tables import Jugador_Equipo, Jugador, Equipo
from app.models.schemas import Jugador_Equipo_schema, Jugador_Equipo_schema_update


def create_relacion_jugador_equipo(session: Session, data: Jugador_Equipo_schema):
    # Validar que existan ambos
    db_jugador = session.get(Jugador, data.jugador_id)
    db_equipo = session.get(Equipo, data.equipo_id)

    if not db_jugador or not db_equipo:
        return 404  # Uno de los dos no existe
    try:
        nueva_relacion = Jugador_Equipo.model_validate(data)
        session.add(nueva_relacion)
        session.commit()
        session.refresh(nueva_relacion)
        return nueva_relacion
    except Exception as e:
        session.rollback()
        print(f"Error en base de datos: {e}")
        return 500


def get_relaciones_all(session: Session):
    return session.exec(select(Jugador_Equipo)).all()


def update_puntaje_relacion(
    session: Session, relacion_id: int, data: Jugador_Equipo_schema_update
):
    relacion_db = session.get(Jugador_Equipo, relacion_id)
    if not relacion_db:
        return 404
    try:
        datos_nuevos = data.model_dump(exclude_unset=True)
        relacion_db.sqlmodel_update(datos_nuevos)
        session.add(relacion_db)
        session.commit()
        session.refresh(relacion_db)
        return relacion_db
    except Exception as e:
        session.rollback()  # Limpiamos la sesión si algo falló
        print(f"Error al actualizar: {e}")
        return 500


def delete_relacion(session: Session, relacion_id: int):
    relacion_db = session.get(Jugador_Equipo, relacion_id)
    if not relacion_db:
        return 404
    session.delete(relacion_db)
    session.commit()
    return True
