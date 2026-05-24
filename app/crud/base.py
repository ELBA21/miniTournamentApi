from typing import Generic, Type, TypeVar, List, Any
from sqlmodel import Session, select, SQLModel, inspect


# Primera vez que experimento con esto
# TypeVar es como un 'joker' en typado de clases, y bound obliga a que sea si o si parte de SQLModel
ModelType = TypeVar("ModelType", bound=SQLModel)
SchemaType = TypeVar("SchemaType", bound=SQLModel)


def _validar_fk(session: Session, fk_constraints: List[dict], data_dict: dict):
    for fk in fk_constraints:
        field_name = fk["local_field"]
        fk_value = data_dict.get(field_name)

        if fk_value is not None:
            parent_model = None
            for cls in SQLModel.__subclasses__():
                if getattr(cls, "__tablename__", None) == fk["target_table"]:
                    parent_model = cls
                    break
            if parent_model:
                parent_obj = session.get(parent_model, fk_value)
                if not parent_obj:
                    raise LookupError(
                        f"No existe registro en {fk['target_table']} con id {fk_value}"
                    )


class CRUDBase(Generic[ModelType, SchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model
        self.fk_constraints = []

        # Mapeamos las FKs una sola vez al levantar la app
        mapper = inspect(self.model)
        for column in mapper.columns:
            if column.foreign_keys:
                for fk in column.foreign_keys:
                    self.fk_constraints.append(
                        {
                            "local_field": column.name,
                            "target_table": fk.column.table.name,
                        }
                    )

    def create(self, session: Session, data: SchemaType) -> ModelType:
        data_dict = data.model_dump()
        _validar_fk(session, self.fk_constraints, data_dict)
        try:
            db_obj = self.model.model_validate(data)
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
            return db_obj
        except Exception:
            session.rollback()
            raise

    def get_all(self, session: Session) -> list[ModelType]:
        try:
            return list(session.exec(select(self.model)).all())
        except Exception:
            raise

    def get_by_id(self, session: Session, search_id: Any) -> ModelType:
        obj = session.get(self.model, search_id)
        if not obj:
            raise LookupError(f"{self.model.__name__} no encontrado")
        return obj

    def update(self, session: Session, search_id: Any, data: SchemaType) -> ModelType:
        try:
            db_obj = self.get_by_id(session, search_id)
            if not db_obj:
                raise LookupError(f"{self.model.__name__} no econtrado")
            data_dict = data.model_dump()
            _validar_fk(session, self.fk_constraints, data_dict)
            update_data = data.model_dump(exclude_unset=True)
            db_obj.sqlmodel_update(update_data)
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
            return db_obj
        except Exception:
            session.rollback()
            raise

    def delete(self, session: Session, search_id: Any) -> bool:
        try:
            db_obj = self.get_by_id(session, search_id)
            session.delete(db_obj)
            session.commit()
            return True
        except Exception:
            session.rollback()
            raise
