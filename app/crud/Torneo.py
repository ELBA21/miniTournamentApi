from sqlmodel import Session, select
from app.models.tables import Torneo
from app.models.schemas import Torneo_schema


def create_torneo(session: Session, data: Torneo_schema):
    try:
        nuevo_torneo = Torneo.model_validate(data)

        session.add(nuevo_torneo)
        session.commit()
        session.refresh(nuevo_torneo)
        return nuevo_torneo

    except Exception as e:
        session.rollback()
        print(f"Error al crear torneo en BD: {e}")
        return 500


def get_torneo_all(session: Session):
    torneos = session.exec(select(Torneo)).all()
    return torneos if torneos else []


def get_torneo_by_id(session: Session, torneo_id: int):
    torneo = session.get(Torneo, torneo_id)
    return torneo if torneo else 404


def update_torneo(session: Session, torneo_id: int, data: Torneo_schema):
    torneo_db = session.get(Torneo, torneo_id)
    if not torneo_db:
        return 404

    try:
        datos_nuevos = data.model_dump(exclude_unset=True)

        torneo_db.sqlmodel_update(datos_nuevos)

        session.add(torneo_db)
        session.commit()
        session.refresh(torneo_db)
        return torneo_db

    except Exception as e:
        session.rollback()
        print(f"Error al actualizar torneo {torneo_id}: {e}")
        return 500


def delete_torneo(session: Session, torneo_id: int):
    torneo_db = session.get(Torneo, torneo_id)
    if not torneo_db:
        return 404
    session.delete(torneo_db)
    session.commit()
    return True
