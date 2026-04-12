from typing import Optional, List, Any
from sqlmodel import Field, Relationship, SQLModel, table
from datetime import date


class Jugador_Equipo(SQLModel, table=True):
    __tablename__: Any = "Jugador_Equipo"
    id: int = Field(default=None, primary_key=True)
    puntaje: int | None = 0
    # FK
    jugador_id: int = Field(default=None, foreign_key="Jugadores.id")
    equipo_id: int = Field(default=None, foreign_key="Equipos.id")

    # Relationship
    jugador: Optional["Jugador"] = Relationship(back_populates="relacion_equipos")
    equipo: Optional["Equipo"] = Relationship(back_populates="relacion_jugador")


class Partido_Equipo(SQLModel, table=True):
    __tablename__: Any = "Partidos_Equipos"
    id: int | None = Field(default=None, primary_key=True)
    ganador: bool | None
    # FK
    equipo_id: int = Field(default=None, foreign_key="Equipos.id")
    partido_id: int = Field(default=None, foreign_key="Partidos.id")
    # Relationship
    equipo: Optional["Equipo"] = Relationship(back_populates="relacion_partido")
    partido: Optional["Partido"] = Relationship(back_populates="relacion_equipos")
    puntajeEquipo: List["PuntajeEquipo"] = Relationship(back_populates="relacion_PE")


class Torneo_Categoria(SQLModel, table=True):
    __tablename__: Any = "Torneos_Categorias"
    id: int | None = Field(default=None, primary_key=True)
    # FKs
    torneo_id: int = Field(default=None, foreign_key="Torneos.id")
    categoria_id: int = Field(default=None, foreign_key="Categorias.id")

    #  Relationship
    inscripciones: List["Inscripcion"] = Relationship(back_populates="relacion_TC")
    fases: List["Fase"] = Relationship(back_populates="torneos_categorias")

    torneo: Optional["Torneo"] = Relationship(back_populates="relacion_categoria")
    categoria: Optional["Categoria"] = Relationship(back_populates="relacion_Torneo")


class Carrera(SQLModel, table=True):
    __tablename__: Any = "Carreras"
    id: int | None = Field(default=None, primary_key=True)

    nombre_carrera: str | None

    # No descomentar, la fk no va de este lado, se queda para recordar mi error
    # jugadores: int | None = Field(default=None, foreign_key=Jugador.id)

    jugadores: List["Jugador"] = Relationship(back_populates="carrera")


class Categoria(SQLModel, table=True):
    __tablename__: Any = "Categorias"
    id: int | None = Field(default=None, primary_key=True)
    tipo: str | None
    # Relationship
    torneos: List["Torneo"] = Relationship(
        back_populates="categorias", link_model=Torneo_Categoria
    )
    relacion_Torneo: List[Torneo_Categoria] = Relationship(back_populates="categoria")


class Jugador(SQLModel, table=True):
    __tablename__: Any = "Jugadores"
    id: int | None = Field(default=None, primary_key=True)

    nombre: str | None = None
    puntaje: int | None = 0
    generacion: date | None = None

    carrera_id: int = Field(default=None, foreign_key="Carreras.id")
    # Basicamente el nombre de 'carrera' se pondra en el relationship de carrera comoa atributo
    # mientras "jugadores" es un atributo de class Carrera
    carrera: Optional["Carrera"] = Relationship(back_populates="jugadores")
    equipos: List["Equipo"] = Relationship(
        back_populates="jugadores", link_model=Jugador_Equipo
    )
    relacion_equipos: List["Jugador_Equipo"] = Relationship(back_populates="jugador")


class Equipo(SQLModel, table=True):
    __tablename__: Any = "Equipos"
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    # Relationship
    inscripciones: List["Inscripcion"] = Relationship(back_populates="equipo")
    jugadores: List["Jugador"] = Relationship(
        back_populates="equipos", link_model=Jugador_Equipo
    )
    partidos: List["Partido"] = Relationship(
        back_populates="equipos", link_model=Partido_Equipo
    )
    relacion_jugador: List["Jugador_Equipo"] = Relationship(back_populates="equipo")
    relacion_partido: List["Partido_Equipo"] = Relationship(back_populates="equipo")


class Partido(SQLModel, table=True):
    __tablename__: Any = "Partidos"
    id: int | None = Field(default=None, primary_key=True)
    # Fk
    fase_id: int = Field(default=None, foreign_key="Fases.id")

    # RelationSHips
    equipos: List["Equipo"] = Relationship(
        back_populates="partidos", link_model=Partido_Equipo
    )
    fase: Optional["Fase"] = Relationship(back_populates="partidosJugados")
    secciones: List["Seccion"] = Relationship(back_populates="partido")
    relacion_equipos: List["Partido_Equipo"] = Relationship(back_populates="partido")


class Fase(SQLModel, table=True):
    __tablename__: Any = "Fases"
    id: int | None = Field(default=None, primary_key=True)
    # Fk
    torneo_categoria_id: int = Field(default=None, foreign_key="Torneos_Categorias.id")
    # Relationship
    partidosJugados: List[Partido] = Relationship(back_populates="fase")
    torneos_categorias: Optional["Torneo_Categoria"] = Relationship(
        back_populates="fases"
    )


class Torneo(SQLModel, table=True):
    __tablename__: Any = "Torneos"
    id: int | None = Field(default=None, primary_key=True)
    nombre: str | None
    fecha: date | None
    # Relationship
    categorias: List["Categoria"] = Relationship(
        back_populates="torneos", link_model=Torneo_Categoria
    )
    relacion_categoria: List[Torneo_Categoria] = Relationship(back_populates="torneo")


class Seccion(SQLModel, table=True):
    __tablename__: Any = "Secciones"
    id: int | None = Field(default=None, primary_key=True)
    # Fk
    partido_id: int = Field(default=None, foreign_key="Partidos.id")
    # Relationship
    partido: Optional[Partido] = Relationship(back_populates="secciones")
    puntajesEquipos: List["PuntajeEquipo"] = Relationship(back_populates="seccion")


class PuntajeEquipo(SQLModel, table=True):
    __tablename__: Any = "Puntajes_De_Equipos"
    id: int | None = Field(default=None, primary_key=True)
    puntaje: int | None
    # Fk
    partido_equipo_id: int = Field(default=None, foreign_key="Partidos_Equipos.id")
    seccion_id: int = Field(default=None, foreign_key="Secciones.id")

    # Relationship
    relacion_PE: Optional[Partido_Equipo] = Relationship(back_populates="puntajeEquipo")
    seccion: Optional[Seccion] = Relationship(back_populates="puntajesEquipos")


class Inscripcion(SQLModel, table=True):
    __tablename__: Any = "Inscripciones"
    id: int | None = Field(default=None, primary_key=True)
    fecha: date | None
    # Fk
    equipo_id: int = Field(default=None, foreign_key="Equipos.id")
    torneo_categoria_id: int = Field(default=None, foreign_key="Torneos_Categorias.id")
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
