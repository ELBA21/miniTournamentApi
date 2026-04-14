from sqlmodel import Session, select
from app.models.tables import Categoria


def create_categoria(session: Session, tipo: str):
    if not tipo:
        return 400
    nueva_categoria = Categoria(tipo=tipo)
    session.add(nueva_categoria)
    session.commit()
    session.refresh(nueva_categoria)
    return nueva_categoria


def get_categoria_all(session: Session):
    categorias = session.exec(select(Categoria)).all()
    return categorias if categorias else []


def get_categoria_by_id(session: Session, categoria_id: int):
    categoria = session.get(Categoria, categoria_id)
    return categoria if categoria else 404


def update_categoria(session: Session, categoria_id: int, nuevo_tipo: str):
    if not nuevo_tipo:
        return 400
    categoria_db = session.get(Categoria, categoria_id)
    if not categoria_db:
        return 404

    categoria_db.tipo = nuevo_tipo
    session.add(categoria_db)
    session.commit()
    session.refresh(categoria_db)
    return categoria_db


def delete_categoria(session: Session, categoria_id: int):
    categoria_db = session.get(Categoria, categoria_id)
    if not categoria_db:
        return 404
    session.delete(categoria_db)
    session.commit()
    return True
