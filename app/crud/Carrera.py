from typing import List
from sqlmodel import Session, select
from app.models.tables import Carrera


def create_carrera(session: Session, nombre: str):
    if not nombre:
        return 400
    nueva_carrera = Carrera(nombre_carrera=nombre)
    if not nueva_carrera:
        return 404  # Creo que esto no pasara nunca xD
    session.add(nueva_carrera)
    session.commit()
    session.refresh(nueva_carrera)
    return nueva_carrera


def get_carrera_all(session: Session):
    return session.exec(select(Carrera)).all()


def get_carrera_byId(session: Session, search_id: int):
    # es mas efectivo session.get(Carrera, search_id), pero queda mi error
    return session.exec(select(Carrera).where(Carrera.id == search_id)).first()


def update_nombre_carrera(session: Session, carrera_id: int, nuevo_nombre: str):
    if not carrera_id or not nuevo_nombre or nuevo_nombre.strip() == "":
        return 400
    carrera_db = session.get(Carrera, carrera_id)
    if not carrera_db:
        return None
    carrera_db.nombre_carrera = nuevo_nombre

    session.add(carrera_db)
    session.commit()
    session.refresh(carrera_db)

    return carrera_db


def delete_carrera(session: Session, carrera_id: int):
    if not carrera_id:
        return 400
    carrera_db = session.get(Carrera, carrera_id)
    if not carrera_db:
        return None
    session.delete(carrera_db)
    session.commit()
    return True
