from sqlmodel import Session, select
from app.models.tables import Torneo
from datetime import date


def create_torneo(session: Session, nombre: str, fecha: date):
    if not nombre or not fecha:
        return 400
    nuevo_torneo = Torneo(nombre=nombre, fecha=fecha)
    session.add(nuevo_torneo)
    session.commit()
    session.refresh(nuevo_torneo)
    return nuevo_torneo


def get_torneo_all(session: Session):
    torneos = session.exec(select(Torneo)).all()
    return torneos if torneos else []


def get_torneo_by_id(session: Session, torneo_id: int):
    torneo = session.get(Torneo, torneo_id)
    return torneo if torneo else 404


def update_torneo(session: Session, torneo_id: int, nombre: str, fecha: date):
    torneo_db = session.get(Torneo, torneo_id)
    if not torneo_db:
        return 404

    if nombre:
        torneo_db.nombre = nombre
    if fecha:
        torneo_db.fecha = fecha

    session.add(torneo_db)
    session.commit()
    session.refresh(torneo_db)
    return torneo_db


def delete_torneo(session: Session, torneo_id: int):
    torneo_db = session.get(Torneo, torneo_id)
    if not torneo_db:
        return 404
    session.delete(torneo_db)
    session.commit()
    return True
