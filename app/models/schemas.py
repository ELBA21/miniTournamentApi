from pydantic import BaseModel
from datetime import date


class JugadorSchema(BaseModel):
    nombre: str | None = None
    puntaje: int | None = 0
    generacion: date | None = None
    carrera_id: int | None = None
