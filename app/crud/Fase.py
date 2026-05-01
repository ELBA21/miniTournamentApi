from sqlmodel import Session, select
from app.models.tables import Fase, Torneo_Categoria
from app.models.schemas import Fase_schema


def create_fase(session: Session, data: Fase_schema):
    tc = session.get(Torneo_Categoria, data.torneo_categoria_id)
    if not tc:
        return 404

    try:
        nueva_fase = Fase.model_validate(data)

        session.add(nueva_fase)
        session.commit()
        session.refresh(nueva_fase)
        return nueva_fase

    except Exception as e:
        session.rollback()
        print(f"Error en base de datos al crear fase: {e}")
        return 500


def get_fase_all(session: Session):
    fases = session.exec(select(Fase)).all()
    return fases if fases else []


def get_fase_by_id(session: Session, fase_id: int):
    fase = session.get(Fase, fase_id)
    return fase if fase else 404


def update_fase(session: Session, fase_id: int, data: Fase_schema):
    fase_db = session.get(Fase, fase_id)
    if not fase_db:
        return 404

    try:
        if data.torneo_categoria_id is not None:
            tc = session.get(Torneo_Categoria, data.torneo_categoria_id)
            if not tc:
                return 400
        datos_nuevos = data.model_dump(exclude_unset=True)
        fase_db.sqlmodel_update(datos_nuevos)

        session.add(fase_db)
        session.commit()
        session.refresh(fase_db)
        return fase_db

    except Exception as e:
        session.rollback()
        print(f"Error al actualizar fase {fase_id}: {e}")
        return 500


def delete_fase(session: Session, fase_id: int):
    fase_db = session.get(Fase, fase_id)
    if not fase_db:
        return 404
    session.delete(fase_db)
    session.commit()
    return True
