from sqlmodel import Session, select
from app.models.tables import Fase, Torneo_Categoria


def create_fase(session: Session, torneo_categoria_id: int):
    # Validar que la relación TC exista
    tc = session.get(Torneo_Categoria, torneo_categoria_id)
    if not tc:
        return 404

    nueva_fase = Fase(torneo_categoria_id=torneo_categoria_id)
    session.add(nueva_fase)
    session.commit()
    session.refresh(nueva_fase)
    return nueva_fase


def get_fase_all(session: Session):
    fases = session.exec(select(Fase)).all()
    return fases if fases else []


def get_fase_by_id(session: Session, fase_id: int):
    fase = session.get(Fase, fase_id)
    return fase if fase else 404


def update_fase(session: Session, fase_id: int, nuevo_tc_id: int):
    fase_db = session.get(Fase, fase_id)
    if not fase_db:
        return 404

    # Validar que el nuevo TC existe si se va a cambiar
    tc = session.get(Torneo_Categoria, nuevo_tc_id)
    if not tc:
        return 400  # Bad request, el nuevo ID no existe

    fase_db.torneo_categoria_id = nuevo_tc_id
    session.add(fase_db)
    session.commit()
    session.refresh(fase_db)
    return fase_db


def delete_fase(session: Session, fase_id: int):
    fase_db = session.get(Fase, fase_id)
    if not fase_db:
        return 404
    session.delete(fase_db)
    session.commit()
    return True
