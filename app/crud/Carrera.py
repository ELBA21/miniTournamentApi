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
    except Exception:
        session.rollback()
        raise


def get_carrera_all(session: Session):
    return session.exec(select(Carrera)).all()


def get_carrera_byId(session: Session, search_id: int):
    carrera = session.get(Carrera, search_id)
    if not carrera:
        raise LookupError("Carrera no encontrada")
    return carrera


def update_nombre_carrera(session: Session, carrera_id: int, data: Carrera_schema):
    try:
        carrera_db = session.get(Carrera, carrera_id)
        if not carrera_db:
            raise
        datos_nuevos = data.model_dump(exclude_unset=True)
        carrera_db.sqlmodel_update(datos_nuevos)

        session.add(carrera_db)
        session.commit()
        session.refresh(carrera_db)

        return carrera_db
    except Exception as e:
        session.rollback()
        raise


def delete_carrera(session: Session, carrera_id: int):
    try:
        if not carrera_id:
            raise
        carrera_db = session.get(Carrera, carrera_id)
        if not carrera_db:
            raise
        session.delete(carrera_db)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise
