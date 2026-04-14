from sqlmodel import Session, select
from app.models.tables import Seccion, Partido


def create_seccion(session: Session, partido_id: int):
    # Validar que el partido exista
    db_partido = session.get(Partido, partido_id)
    if not db_partido:
        return 404

    nueva_seccion = Seccion(partido_id=partido_id)
    session.add(nueva_seccion)
    session.commit()
    session.refresh(nueva_seccion)
    return nueva_seccion


def get_secciones_all(session: Session):
    return session.exec(select(Seccion)).all()


def get_seccion_by_id(session: Session, seccion_id: int):
    seccion = session.get(Seccion, seccion_id)
    return seccion if seccion else 404


def delete_seccion(session: Session, seccion_id: int):
    seccion_db = session.get(Seccion, seccion_id)
    if not seccion_db:
        return 404
    session.delete(seccion_db)
    session.commit()
    return True
