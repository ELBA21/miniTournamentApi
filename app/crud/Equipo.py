from sqlmodel import Session, select
from app.models.tables import Equipo


def create_Equipo(session: Session, nombre: str):
    if not nombre:
        return 400
    nuevo_equipo = Equipo(nombre=nombre)
    session.add(nuevo_equipo)
    session.commit()
    session.refresh(nuevo_equipo)
    return nuevo_equipo


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


def update_Equipo(session: Session, equipo_id: int, new_nombre: str):
    if not equipo_id or not new_nombre:
        return 400
    equipo = session.get(Equipo, equipo_id)
    if not equipo:
        return 404
    equipo.nombre = new_nombre
    session.add(equipo)
    session.commit()
    session.refresh(equipo)
    return equipo


def delete_Equipo(session: Session, equipo_id: int):
    if not equipo_id:
        return 400
    equipo = session.get(Equipo, equipo_id)
    if not equipo:
        return 404
    session.delete(equipo)
    session.commit()
    return True
