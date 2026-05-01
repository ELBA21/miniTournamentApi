from sqlmodel import Session, select
from app.models.tables import Partido_Equipo, Equipo, Partido
from app.models.schemas import Partido_Equipo_schema, Partido_Equipo_schema_update


def create_partido_equipo(session: Session, data: Partido_Equipo_schema):
    # 1. Validar integridad referencial (FKs)
    db_equipo = session.get(Equipo, data.equipo_id)
    db_partido = session.get(Partido, data.partido_id)

    if not db_equipo or not db_partido:
        return 404

    try:
        # 2. Validar y transformar a modelo de tabla
        nueva_relacion = Partido_Equipo.model_validate(data)

        session.add(nueva_relacion)
        session.commit()
        session.refresh(nueva_relacion)
        return nueva_relacion

    except Exception as e:
        session.rollback()
        print(f"Error al crear relación partido-equipo: {e}")
        return 500


def get_partido_equipo_all(session: Session):
    return session.exec(select(Partido_Equipo)).all()


def update_partido_equipo(
    session: Session, pe_id: int, data: Partido_Equipo_schema_update
):
    # 1. Buscar la relación existente
    pe_db = session.get(Partido_Equipo, pe_id)
    if not pe_db:
        return 404

    try:
        datos_nuevos = data.model_dump(exclude_unset=True)
        pe_db.sqlmodel_update(datos_nuevos)

        session.add(pe_db)
        session.commit()
        session.refresh(pe_db)
        return pe_db

    except Exception as e:
        session.rollback()
        print(f"Error al actualizar resultado/relación {pe_id}: {e}")
        return 500


def delete_partido_equipo(session: Session, pe_id: int):
    pe_db = session.get(Partido_Equipo, pe_id)
    if not pe_db:
        return 404
    session.delete(pe_db)
    session.commit()
    return True
