from sqlmodel import Session, select
from app.models.tables import Partido, Fase
from app.models.schemas import Partido_schema


def create_partido(session: Session, data: Partido_schema):
    # 1. Validar que la fase exista
    db_fase = session.get(Fase, data.fase_id)
    if not db_fase:
        return 404

    try:
        # 2. Validar y crear modelo desde el schema
        nuevo_partido = Partido.model_validate(data)

        session.add(nuevo_partido)
        session.commit()
        session.refresh(nuevo_partido)
        return nuevo_partido

    except Exception as e:
        session.rollback()
        print(f"Error al crear partido: {e}")
        return 500


def get_partido_all(session: Session):
    return session.exec(select(Partido)).all()


def get_partido_by_id(session: Session, partido_id: int):
    partido = session.get(Partido, partido_id)
    return partido if partido else 404


def update_partido(session: Session, partido_id: int, data: Partido_schema):
    partido_db = session.get(Partido, partido_id)
    if not partido_db:
        return 404

    try:
        if data.fase_id is not None:
            db_fase = session.get(Fase, data.fase_id)
            if not db_fase:
                return 400

        datos_nuevos = data.model_dump(exclude_unset=True)
        partido_db.sqlmodel_update(datos_nuevos)

        session.add(partido_db)
        session.commit()
        session.refresh(partido_db)
        return partido_db

    except Exception as e:
        session.rollback()
        print(f"Error al actualizar partido: {e}")
        return 500


def delete_partido(session: Session, partido_id: int):
    partido_db = session.get(Partido, partido_id)
    if not partido_db:
        return 404
    session.delete(partido_db)
    session.commit()
    return True
