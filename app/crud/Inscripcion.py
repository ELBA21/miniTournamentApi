from sqlmodel import Session, select
from app.models.tables import Inscripcion, Equipo, Torneo_Categoria
from datetime import date


def create_inscripcion(
    session: Session, equipo_id: int, torneo_categoria_id: int, fecha: date
):
    # Validar que existan ambos extremos
    db_equipo = session.get(Equipo, equipo_id)
    db_tc = session.get(Torneo_Categoria, torneo_categoria_id)

    if not db_equipo or not db_tc:
        return 404

    # Si no mandan fecha, usamos la de hoy
    if not fecha:
        fecha = date.today()

    nueva_inscripcion = Inscripcion(
        equipo_id=equipo_id, torneo_categoria_id=torneo_categoria_id, fecha=fecha
    )
    session.add(nueva_inscripcion)
    session.commit()
    session.refresh(nueva_inscripcion)
    return nueva_inscripcion


def get_inscripciones_all(session: Session):
    return session.exec(select(Inscripcion)).all()


def get_inscripcion_by_id(session: Session, inscripcion_id: int):
    inscripcion = session.get(Inscripcion, inscripcion_id)
    return inscripcion if inscripcion else 404


def delete_inscripcion(session: Session, inscripcion_id: int):
    inscripcion_db = session.get(Inscripcion, inscripcion_id)
    if not inscripcion_db:
        return 404
    session.delete(inscripcion_db)
    session.commit()
    return True
