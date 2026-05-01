from sqlmodel import Session, select
from app.models.tables import Inscripcion, Equipo, Torneo_Categoria
from datetime import date
from app.models.schemas import Inscripcion_schema


def create_inscripcion(session: Session, data: Inscripcion_schema):
    # 1. Validar que existan ambos extremos (Relaciones)
    db_equipo = session.get(Equipo, data.equipo_id)
    db_tc = session.get(Torneo_Categoria, data.torneo_categoria_id)

    if not db_equipo or not db_tc:
        return 404  # Equipo o Categoría de Torneo no encontrados

    try:
        # 2. Validar y transformar el schema a modelo de tabla
        nueva_inscripcion = Inscripcion.model_validate(data)

        # 3. Lógica de fecha por defecto si no viene en el data
        if not nueva_inscripcion.fecha:
            nueva_inscripcion.fecha = date.today()

        # 4. Guardar en BD
        session.add(nueva_inscripcion)
        session.commit()
        session.refresh(nueva_inscripcion)
        return nueva_inscripcion

    except Exception as e:
        session.rollback()
        print(f"Error en base de datos al crear inscripción: {e}")
        return 500


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
