from datetime import date
from sqlmodel import Field, SQLModel
from typing import Optional


#
# ================================
# Jugador_Equipo
class Jugador_Equipo_schema(SQLModel):
    puntaje: int | None = 0
    # FK
    jugador_id: int = Field(default=None, foreign_key="Jugadores.id")
    equipo_id: int = Field(default=None, foreign_key="Equipos.id")


class Jugador_Equipo_schema_update(SQLModel):
    puntaje: int | None = None


# ================================
# Partido_Equipo
class Partido_Equipo_schema(SQLModel):
    ganador: bool | None
    # FK
    equipo_id: int = Field(default=None, foreign_key="Equipos.id")
    partido_id: int = Field(default=None, foreign_key="Partidos.id")


class Partido_Equipo_schema_update(SQLModel):
    ganador: bool | None


# ================================
# Torneos_Categorias
class Torneos_Categorias_schema(SQLModel):
    # FKs
    torneo_id: int = Field(default=None, foreign_key="Torneos.id")
    categoria_id: int = Field(default=None, foreign_key="Categorias.id")


# ================================
# Carrera
class Carrera_schema(SQLModel):
    nombre_carrera: str | None


# ================================
# Categoria
class Categoria_schema(SQLModel):
    tipo: str | None


# ================================
#  Jugador
class JugadorSchema(SQLModel):
    nombre: str | None = None
    puntaje: int | None = 0
    generacion: date | None = None
    carrera_id: int = Field(default=None, foreign_key="Carreras.id")


class Jugador_schema_Update(SQLModel):
    nombre: str | None = None
    puntaje: int | None = 0
    generacion: date | None = None


# ================================
# Equipo
class Equipo_schema(SQLModel):
    nombre: str


# ================================
#  Partido
class Partido_schema(SQLModel):
    fase_id: int = Field(default=None, foreign_key="Fases.id")
    partido_siguiente_id: Optional[int] = Field(default=None, foreign_key="Partidos.id")


# ================================
# Fase
class Fase_schema(SQLModel):
    nombre: str
    orden: int
    # Fk
    torneo_categoria_id: int = Field(default=None, foreign_key="Torneos_Categorias.id")


# ================================
# Torneo
class Torneo_schema(SQLModel):
    nombre: str | None
    fecha: date | None


# ================================
# Seccion
class Seccion_schema(SQLModel):
    partido_id: int = Field(default=None, foreign_key="Partidos.id")


# ================================
# PuntajeEquipo
class PuntajeEquipo_schema(SQLModel):
    puntaje: int | None
    # Fk
    partido_equipo_id: int = Field(default=None, foreign_key="Partidos_Equipos.id")
    seccion_id: int = Field(default=None, foreign_key="Secciones.id")


# ================================
# Inscripcion
class Inscripcion_schema(SQLModel):
    fecha: date | None
    # Fk
    equipo_id: int = Field(default=None, foreign_key="Equipos.id")
    torneo_categoria_id: int = Field(default=None, foreign_key="Torneos_Categorias.id")


#
