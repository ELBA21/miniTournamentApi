from sqlmodel import Session, select
from app.models.tables import Torneo_Categoria, Torneo, Categoria


def create_relacion_torneo_categoria(
    session: Session, torneo_id: int, categoria_id: int
):
    # Validar que existan ambos antes de unir
    db_torneo = session.get(Torneo, torneo_id)
    db_categoria = session.get(Categoria, categoria_id)

    if not db_torneo or not db_categoria:
        return 404

    nueva_relacion = Torneo_Categoria(torneo_id=torneo_id, categoria_id=categoria_id)
    session.add(nueva_relacion)
    session.commit()
    session.refresh(nueva_relacion)
    return nueva_relacion


def get_relaciones_tc_all(session: Session):
    return session.exec(select(Torneo_Categoria)).all()


def get_relacion_tc_by_id(session: Session, tc_id: int):
    result = session.get(Torneo_Categoria, tc_id)
    return result if result else 404


def delete_relacion_torneo_categoria(session: Session, tc_id: int):
    db_relacion = session.get(Torneo_Categoria, tc_id)
    if not db_relacion:
        return 404
    session.delete(db_relacion)
    session.commit()
    return True
