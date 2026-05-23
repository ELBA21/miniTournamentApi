from math import log, ceil
from typing import List
from sqlmodel import Session, select
from app.models.schemas import (
    Fase_schema,
    Torneos_Categorias_schema,
    Partido_schema,
)
from app.models.tables import Equipo, Inscripcion
from app.crud.Fase import create_fase
from app.crud.Partido import create_partido
from app.crud.Torneo_Categoria import create_relacion_torneo_categoria


def get_equipos(session: Session, torneo_categoria_id: int) -> List[Equipo]:
    statement = (
        select(Equipo)
        .join(Inscripcion)
        .where(Inscripcion.torneo_categoria_id == torneo_categoria_id)
    )
    return list(session.exec(statement).all())


def generar_rondas(torneo_categoria_id: int, session: Session):
    cant_equipos = len(get_equipos(session, torneo_categoria_id))
    # Indicamos la cantidad de fases
    cant_fases = ceil(log(cant_equipos, 2))
    fases_creadas = []
    partidos_creados = []
    i = 0
    for i in range(1, cant_fases + 1):
        nombre_fase = f"Ronda {i}"
        if i == 1:
            nombre_fase = "Final"
        elif i == 2:
            nombre_fase = "Semifinal"
        elif i == 3:
            nombre_fase = "Cuartos de final"
        elif i == 4:
            nombre_fase = "Octavos de final"

        nueva_fase = Fase_schema(
            nombre=nombre_fase, orden=i, torneo_categoria_id=torneo_categoria_id
        )
        fase_db = create_fase(session, nueva_fase)
        fases_creadas.append(fase_db)

        return fases_creadas
