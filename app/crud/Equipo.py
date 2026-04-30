from sqlmodel import Session, select
from app.models.tables import Equipo
from app.models.schemas import Equipo_schema


def create_Equipo(session: Session, data: Equipo_schema):
    try:
        nuevo_equipo = Equipo.model_validate(data)
        session.add(nuevo_equipo)
        session.commit()
        session.refresh(nuevo_equipo)
        return nuevo_equipo
    except Exception as e:
        session.rollback()
        print(f"Error en base de datos: {e}")
        return 404


def get_Equipo_all(session: Session):
    equipos = session.exec(select(Equipo)).all()
    if not equipos:
        return []
    return equipos


def get_Equipo_byId(session: Session, equipo_id: int):
    if not equipo_id:
        return 400
    equipo = session.get(Equipo, equipo_id)
    if not equipo:
        return 404
    return equipo


def update_Equipo(session: Session, equipo_id: int, data: Equipo_schema):
    equipo_db = session.get(Equipo, equipo_id)
    if not equipo_db:
        return 404
    try:
        datos_nuevos = data.model_dump(exclude_unset=True)
        equipo_db.sqlmodel_update(datos_nuevos)
        session.add(equipo_db)
        session.commit()
        session.refresh(equipo_db)
        return equipo_db
    except Exception as e:
        session.rollback()
        print(f"Error al actualizar: {e}")
        return 500


def delete_Equipo(session: Session, equipo_id: int):
    if not equipo_id:
        return 400
    equipo = session.get(Equipo, equipo_id)
    if not equipo:
        return 404
    session.delete(equipo)
    session.commit()
    return True
