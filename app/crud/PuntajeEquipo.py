from sqlmodel import Session, select
from app.models.tables import PuntajeEquipo, Partido_Equipo, Seccion
from app.models.schemas import PuntajeEquipo_schema


def create_puntaje_equipo(session: Session, data: PuntajeEquipo_schema):
    # 1. Validar que existan ambos extremos de la relación
    pe = session.get(Partido_Equipo, data.partido_equipo_id)
    sec = session.get(Seccion, data.seccion_id)

    if not pe or not sec:
        return 404  # Relación partido-equipo o sección no encontrados

    try:
        # 2. Validar y crear modelo desde schema
        nuevo_puntaje = PuntajeEquipo.model_validate(data)

        session.add(nuevo_puntaje)
        session.commit()
        session.refresh(nuevo_puntaje)
        return nuevo_puntaje

    except Exception as e:
        session.rollback()
        print(f"Error al registrar puntaje: {e}")
        return 500


def get_puntaje_equipo_all(session: Session):
    return session.exec(select(PuntajeEquipo)).all()


def get_puntaje_equipo_byId(session: Session, search_id: int):
    return session.get(PuntajeEquipo, search_id)


def update_puntaje_equipo(
    session: Session, puntaje_id: int, data: PuntajeEquipo_schema
):
    # 1. Buscar el registro de puntaje
    puntaje_db = session.get(PuntajeEquipo, puntaje_id)
    if not puntaje_db:
        return 404

    try:
        # 2. Si se intenta cambiar las FKs, validar que los nuevos destinos existan
        if data.partido_equipo_id is not None:
            if not session.get(Partido_Equipo, data.partido_equipo_id):
                return 400

        if data.seccion_id is not None:
            if not session.get(Seccion, data.seccion_id):
                return 400

        # 3. Actualización parcial (solo el valor del puntaje o lo que venga en el JSON)
        datos_nuevos = data.model_dump(exclude_unset=True)
        puntaje_db.sqlmodel_update(datos_nuevos)

        session.add(puntaje_db)
        session.commit()
        session.refresh(puntaje_db)
        return puntaje_db

    except Exception as e:
        session.rollback()
        print(f"Error al actualizar puntaje {puntaje_id}: {e}")
        return 500


def delete_puntaje(session: Session, puntaje_id: int):
    puntaje_db = session.get(PuntajeEquipo, puntaje_id)
    if not puntaje_db:
        return 404
    session.delete(puntaje_db)
    session.commit()
    return True
