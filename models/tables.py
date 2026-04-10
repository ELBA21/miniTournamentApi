from typing import Optional, List
from sqlmodel import Field, Relationship, SQLModel, table
from datetime import date


class Jugador(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    nombre: str | None = None
    puntaje: int | None = 0
    generacion: date | None = None

    carrera_id: int = Field(default=None, foreign_key="carrera.id")
    # Basicamente el nombre de 'carrera' se pondra en el relationship de carrera comoa atributo
    # mientras "jugadores" es un atributo de class Carrera
    carrera: Optional["Carrera"] = Relationship(back_populates="jugadores")
    equipos: List["Equipo"] = Relationship(
        back_populates="jugadores", link_model="Jugador_Equipo"
    )


class Carrera(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    nombre_carrera: str

    # No descomentar, la fk no va de este lado, se queda para recordar mi error
    # jugadores: int | None = Field(default=None, foreign_key=Jugador.id)

    jugadores: List["Jugador"] = Relationship(back_populates="carrera")


class Equipo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    # FK
    inscripcion_id: int = Field(default=None, foreign_key="inscripcion.id")

    jugadores: List["Jugador"] = Relationship(
        back_populates="equipos", link_model="Jugador_Equipo"
    )
    partidos: List["Partido"] = Relationship(
        back_populates="equipos", link_model="Partido_Equipo"
    )


class Jugador_Equipo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    puntaje: int | None = 0
    # FK
    jugador_id: int = Field(default=None, foreign_key="jugador.id")
    equipo_id: int = Field(default=None, foreign_key="equipo.id")


class Partido(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # Fk
    fase_id: int = Field(default=None, foreign_key="fase.id")
    # RelationSHips
    equipos: List["Equipo"] = Relationship(
        back_populates="partidos", link_model="Partido_Equipo"
    )
    fase: "Fase" = Relationship(back_populates="partidosJugados")
    secciones: List["Seccion"] = Relationship(back_populates="partidos")


class Fase(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # Fk
    torneo_categoria_id: int = Field(default=None, foreign_key="torneo_categoria.id")
    # Relationship
    partidosJugados: List[Partido] = Relationship(back_populates="fase")
    torneos_categorias: List["Torneo_Categoria"] = Relationship(back_populates="fases")


class Partido_Equipo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ganador: bool | None
    # FK
    equipo_id: int = Field(default=None, foreign_key="equipo.id")
    partido_id: int = Field(default=None, foreign_key="partido.id")


class Torneo_Categoria(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # FKs
    torneo_id: int = Field(default=None, foreign_key="torneo.id")
    categoria_id: int = Field(default=None, foreign_key="categoria.id")

    fases: List["Fase"] = Relationship(back_populates="torneos_categorias")


class Torneo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str | None
    fecha: date | None
    categorias: List["Categoria"] = Relationship(
        back_populates="torneos", link_model="Torneo_Categoria"
    )


class Categoria(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tipo: str | None
    torneos: List["Torneo"] = Relationship(
        back_populates="categorias", link_model="Torneo_Categoria"
    )


class Seccion(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    partido_id: int = Field(default=None, foreign_key="partido.id")


class PuntajeEquipo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    puntaje: int | None

    partido_equipo_id: int = Field(default=None, foreign_key="partido_equipo.id")
    seccion_id: int = Field(default=None, foreign_key="seccion.id")


class Inscripcion(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    fecha: date | None
    equipo_id: int = Field(default=None, foreign_key="equipo.id")
    torneo_categoria_id: int = Field(default=None, foreign_key="torneo_categoria.id")
