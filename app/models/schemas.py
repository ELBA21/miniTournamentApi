from pydantic import BaseModel
from datetime import date
from sqlmodel import Field, SQLModel


class JugadorSchema(BaseModel):
    nombre: str | None = None
    puntaje: int | None = 0
    generacion: date | None = None
    carrera_id: int | None = None


# Jugador_Equipo


class Jugador_Equipo_schema(SQLModel):
    puntaje: int | None = 0
    # FK
    jugador_id: int = Field(default=None, foreign_key="Jugadores.id")
    equipo_id: int = Field(default=None, foreign_key="Equipos.id")


class Jugador_Equipo_schema_update(SQLModel):
    puntaje: int | None = None


# Carrera
class Carrera_schema(SQLModel):
    nombre_carrera: str | None


class Categoria_schema(SQLModel):
    tipo: str | None
