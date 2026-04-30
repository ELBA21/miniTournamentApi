from sqlmodel import Session, select
from app.models.tables import Categoria
from app.models.schemas import Categoria_schema


def create_categoria(session: Session, data: Categoria_schema):
    try:
        nueva_categoria = Categoria.model_validate(data)
        session.add(nueva_categoria)
        session.commit()
        session.refresh(nueva_categoria)
        return nueva_categoria
    except Exception as e:
        session.rollback()
        print(f"Error en base de datos: {e}")
        return 404


def get_categoria_all(session: Session):
    categorias = session.exec(select(Categoria)).all()
    return categorias if categorias else []


def get_categoria_by_id(session: Session, categoria_id: int):
    categoria = session.get(Categoria, categoria_id)
    return categoria if categoria else 404


def update_categoria(session: Session, categoria_id: int, data: Categoria_schema):
    categoria_db = session.get(Categoria, categoria_id)
    if not categoria_db:
        return 404
    try:
        datos_nuevos = data.model_dump(exclude_unset=True)
        categoria_db.sqlmodel_update(datos_nuevos)
        session.add(categoria_db)
        session.commit()
        session.refresh(categoria_db)
        return categoria_db
    except Exception as e:
        session.rollback()
        print(f"Error al actualizar: {e}")
        return 500


def delete_categoria(session: Session, categoria_id: int):
    categoria_db = session.get(Categoria, categoria_id)
    if not categoria_db:
        return 404
    session.delete(categoria_db)
    session.commit()
    return True
