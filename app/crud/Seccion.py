from sqlmodel import Session, select
from app.models.tables import Seccion, Partido
from app.models.schemas import Seccion_schema


def create_seccion(session: Session, data: Seccion_schema):
    # 1. Validar que el partido asociado exista
    db_partido = session.get(Partido, data.partido_id)
    if not db_partido:
        return 404

    try:
        # 2. Validar y transformar a modelo de tabla
        nueva_seccion = Seccion.model_validate(data)

        session.add(nueva_seccion)
        session.commit()
        session.refresh(nueva_seccion)
        return nueva_seccion

    except Exception as e:
        session.rollback()
        print(f"Error al crear sección: {e}")
        return 500


def get_secciones_all(session: Session):
    return session.exec(select(Seccion)).all()


def get_seccion_by_id(session: Session, seccion_id: int):
    seccion = session.get(Seccion, seccion_id)
    return seccion if seccion else 404


def update_seccion(session: Session, seccion_id: int, data: Seccion_schema):
    # 1. Buscar la sección
    seccion_db = session.get(Seccion, seccion_id)
    if not seccion_db:
        return 404

    try:
        # 2. Si se intenta cambiar el partido_id, validar que el nuevo exista
        if data.partido_id is not None:
            db_partido = session.get(Partido, data.partido_id)
            if not db_partido:
                return 400  # El nuevo partido no existe

        # 3. Actualización inteligente
        datos_nuevos = data.model_dump(exclude_unset=True)
        seccion_db.sqlmodel_update(datos_nuevos)

        session.add(seccion_db)
        session.commit()
        session.refresh(seccion_db)
        return seccion_db

    except Exception as e:
        session.rollback()
        print(f"Error al actualizar sección {seccion_id}: {e}")
        return 500


def delete_seccion(session: Session, seccion_id: int):
    seccion_db = session.get(Seccion, seccion_id)
    if not seccion_db:
        return 404
    session.delete(seccion_db)
    session.commit()
    return True
