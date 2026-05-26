from math import log, ceil
from typing import List
from sqlmodel import Session, select
from app.models.schemas import (
    Fase_schema,
    Torneos_Categorias_schema,
    Partido_schema,
)
from app.models.tables import Equipo, Inscripcion
from app.crud.factory import (
    crud_fase as fase,
    crud_partido as partido,
    crud_torneo_categoria as torneo_categoria,
)


def get_equipos(session: Session, torneo_categoria_id: int) -> List[Equipo]:
    return list(
        session.exec(
            select(Equipo)
            .join(Inscripcion)
            .where(Inscripcion.torneo_categoria_id == torneo_categoria_id)
        ).all()
    )


def generar_rondas(torneo_categoria_id: int, session: Session):
    equipos = get_equipos(session, torneo_categoria_id)
    cant_equipos = len(equipos)
    if cant_equipos < 2:
        return []

    # Indicamos la cantidad de fases
    cant_fases = ceil(log(cant_equipos, 2))
    fases_creadas = []
    partidos_creados = []
    nombres = {
        0: "Final",
        1: "Semi",
        2: "Cuartos",
        3: "Octavos",
    }
    for paso in range(cant_fases):
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
        fase_db = fase.create(session, nueva_fase)
        fases_creadas.append(fase_db)
        if i == 1:
            nuevo_partido = Partido_schema(fase_id=fase_db.id)
        nuevo_partido = Partido_schema(
            fase_id=fase_db.id, partido_siguiente_id=partidos_creados[-1]
        )
        return fases_creadas
