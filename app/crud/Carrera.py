from typing import List
from sqlmodel import Session, select
from app.models.tables import Carrera


def crear_carrera(session: Session, nombre: str) -> Carrera:
    nueva_carrera = Carrera(nombre_carrera=nombre)

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
    carrera_db = session.get(Carrera, carrera_id)
    if not carrera_db:
        return None
    carrera_db.nombre_carrera = nuevo_nombre

    session.add(carrera_db)
    session.commit()
    session.refresh(carrera_db)

    return carrera_db


def borrar_carrera(session: Session, carrera_id: int):
    carrera_db = session.get(Carrera, carrera_id)
    if not carrera_db:
        return False
    session.delete(carrera_db)
    session.commit()
    return True
