from typing import List
from sqlmodel import Session, select
from app.models.tables import Carrera
from app.models.schemas import Carrera_schema


def create_carrera(session: Session, data: Carrera_schema):
    try:
        nueva_carrera = Carrera.model_validate(data)

        session.add(nueva_carrera)
        session.commit()
        session.refresh(nueva_carrera)
        return nueva_carrera
    except Exception as e:
        session.rollback()
        print(f"Error en base de datos: {e}")
        return 404


def get_carrera_all(session: Session):
    return session.exec(select(Carrera)).all()


def get_carrera_byId(session: Session, search_id: int):
    # es mas efectivo session.get(Carrera, search_id), pero queda mi error
    return session.exec(select(Carrera).where(Carrera.id == search_id)).first()


def update_nombre_carrera(session: Session, carrera_id: int, data: Carrera_schema):

    carrera_db = session.get(Carrera, carrera_id)
    if not carrera_db:
        return 404
    try:
        datos_nuevos = data.model_dump(exclude_unset=True)
        carrera_db.sqlmodel_update(datos_nuevos)

        session.add(carrera_db)
        session.commit()
        session.refresh(carrera_db)

        return carrera_db
    except Exception as e:
        session.rollback()
        print(f"Error al actualizar: {e}")
        return 500


def delete_carrera(session: Session, carrera_id: int):
    if not carrera_id:
        return 400
    carrera_db = session.get(Carrera, carrera_id)
    try:
        if not carrera_db:
            return None
        session.delete(carrera_db)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"No se puede eliminar: {e}")
        return False
