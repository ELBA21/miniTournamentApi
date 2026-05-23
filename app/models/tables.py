from typing import Optional, List, Any
from sqlmodel import Field, Relationship
from app.models.schemas import (
    Jugador_Equipo_schema,
    Partido_Equipo_schema,
    Torneos_Categorias_schema,
    Carrera_schema,
    Categoria_schema,
    JugadorSchema,
    Equipo_schema,
    Partido_schema,
    Fase_schema,
    Torneo_schema,
    Seccion_schema,
    PuntajeEquipo_schema,
    Inscripcion_schema,
)


class Jugador_Equipo(Jugador_Equipo_schema, table=True):
    __tablename__: Any = "Jugador_Equipo"
    id: int = Field(default=None, primary_key=True)

    # Relationship
    jugador: Optional["Jugador"] = Relationship(back_populates="relacion_equipos")
    equipo: Optional["Equipo"] = Relationship(back_populates="relacion_jugador")


class Partido_Equipo(Partido_Equipo_schema, table=True):
    __tablename__: Any = "Partidos_Equipos"
    id: int | None = Field(default=None, primary_key=True)
    # Relationship
    equipo: Optional["Equipo"] = Relationship(back_populates="relacion_partido")
    partido: Optional["Partido"] = Relationship(back_populates="relacion_equipos")
    puntajeEquipo: List["PuntajeEquipo"] = Relationship(back_populates="relacion_PE")


# a
class Torneo_Categoria(Torneos_Categorias_schema, table=True):
    __tablename__: Any = "Torneos_Categorias"
    id: int | None = Field(default=None, primary_key=True)

    inscripciones: List["Inscripcion"] = Relationship(back_populates="relacion_TC")
    fases: List["Fase"] = Relationship(back_populates="torneos_categorias")
    torneo: Optional["Torneo"] = Relationship(back_populates="relacion_categoria")
    categoria: Optional["Categoria"] = Relationship(back_populates="relacion_Torneo")


class Carrera(Carrera_schema, table=True):
    __tablename__: Any = "Carreras"
    id: int | None = Field(default=None, primary_key=True)

    # No descomentar, la fk no va de este lado, se queda para recordar mi error
    # jugadores: int | None = Field(default=None, foreign_key=Jugador.id)

    jugadores: List["Jugador"] = Relationship(back_populates="carrera")


class Categoria(Categoria_schema, table=True):
    __tablename__: Any = "Categorias"
    id: int | None = Field(default=None, primary_key=True)
    # Relationship
    torneos: List["Torneo"] = Relationship(
        back_populates="categorias", link_model=Torneo_Categoria
    )
    relacion_Torneo: List[Torneo_Categoria] = Relationship(back_populates="categoria")


class Jugador(JugadorSchema, table=True):
    __tablename__: Any = "Jugadores"
    id: int | None = Field(default=None, primary_key=True)

    carrera: Optional["Carrera"] = Relationship(back_populates="jugadores")
    equipos: List["Equipo"] = Relationship(
        back_populates="jugadores", link_model=Jugador_Equipo
    )
    relacion_equipos: List["Jugador_Equipo"] = Relationship(back_populates="jugador")


class Equipo(Equipo_schema, table=True):
    __tablename__: Any = "Equipos"
    id: int | None = Field(default=None, primary_key=True)
    inscripciones: List["Inscripcion"] = Relationship(back_populates="equipo")
    jugadores: List["Jugador"] = Relationship(
        back_populates="equipos", link_model=Jugador_Equipo
    )
    partidos: List["Partido"] = Relationship(
        back_populates="equipos", link_model=Partido_Equipo
    )
    relacion_jugador: List["Jugador_Equipo"] = Relationship(back_populates="equipo")
    relacion_partido: List["Partido_Equipo"] = Relationship(back_populates="equipo")


class Partido(Partido_schema, table=True):
    __tablename__: Any = "Partidos"
    id: int | None = Field(default=None, primary_key=True)

    # RelationSHips
    equipos: List["Equipo"] = Relationship(
        back_populates="partidos", link_model=Partido_Equipo
    )
    fase: Optional["Fase"] = Relationship(back_populates="partidosJugados")
    secciones: List["Seccion"] = Relationship(back_populates="partido")
    relacion_equipos: List["Partido_Equipo"] = Relationship(back_populates="partido")
    partido_siguiente: Optional["Partido"] = Relationship(
        back_populates="partidos_anteriores",
        sa_relationship_kwargs={"remote_side": "Partido.id"},
    )
    partidos_anteriores: List["Partido"] = Relationship(
        back_populates="partido_siguiente"
    )


class Fase(Fase_schema, table=True):
    __tablename__: Any = "Fases"
    id: int | None = Field(default=None, primary_key=True)
    # Relationship
    partidosJugados: List[Partido] = Relationship(back_populates="fase")
    torneos_categorias: Optional["Torneo_Categoria"] = Relationship(
        back_populates="fases"
    )


class Torneo(Torneo_schema, table=True):
    __tablename__: Any = "Torneos"
    id: int | None = Field(default=None, primary_key=True)
    # Relationship
    categorias: List["Categoria"] = Relationship(
        back_populates="torneos", link_model=Torneo_Categoria
    )
    relacion_categoria: List[Torneo_Categoria] = Relationship(back_populates="torneo")


class Seccion(Seccion_schema, table=True):
    __tablename__: Any = "Secciones"
    id: int | None = Field(default=None, primary_key=True)
    # Relationship
    partido: Optional[Partido] = Relationship(back_populates="secciones")
    puntajesEquipos: List["PuntajeEquipo"] = Relationship(back_populates="seccion")


class PuntajeEquipo(PuntajeEquipo_schema, table=True):
    __tablename__: Any = "Puntajes_De_Equipos"
    id: int | None = Field(default=None, primary_key=True)
    puntaje: int | None
    # Relationship
    relacion_PE: Optional[Partido_Equipo] = Relationship(back_populates="puntajeEquipo")
    seccion: Optional[Seccion] = Relationship(back_populates="puntajesEquipos")


class Inscripcion(Inscripcion_schema, table=True):
    __tablename__: Any = "Inscripciones"
    id: int | None = Field(default=None, primary_key=True)
    # Relationship
    equipo: Optional[Equipo] = Relationship(back_populates="inscripciones")
    relacion_TC: Optional[Torneo_Categoria] = Relationship(
        back_populates="inscripciones"
    )


# Esto obliga a SQLModel a procesar todas las relaciones y tipos string
# una vez que TODAS las clases ya fueron cargadas en memoria.
Jugador.model_rebuild()
Equipo.model_rebuild()
Partido.model_rebuild()
Fase.model_rebuild()
Torneo.model_rebuild()
Seccion.model_rebuild()
PuntajeEquipo.model_rebuild()
Inscripcion.model_rebuild()
Jugador_Equipo.model_rebuild()
Partido_Equipo.model_rebuild()
Torneo_Categoria.model_rebuild()
