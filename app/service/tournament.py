from math import log, ceil
from typing import List
import random
from sqlmodel import Session, desc, select
from app.models.schemas import Fase_schema, Partido_schema, Partido_Equipo_schema
from app.models.tables import Fase, Partido, Equipo, Inscripcion, Torneo_Categoria
from app.crud.factory import (
    crud_fase as fase,
    crud_partido as partido,
    crud_partido_equipo as partido_equipo,
)


def get_equipos_participantes(
    session: Session, torneo_categoria_id: int
) -> List[Equipo]:
    return list(
        session.exec(
            select(Equipo)
            .join(Inscripcion)
            .where(Inscripcion.torneo_categoria_id == torneo_categoria_id)
        ).all()
    )


def bool_fase_final(session: Session, torneo_categoria_id) -> bool:
    fase_final = session.exec(
        select(Fase).where(
            Fase.torneo_categoria_id == torneo_categoria_id, Fase.nombre == "Final"
        )
    ).first()
    if fase_final is not None:
        return True
    return False


def generar_rondas_para_torneo_categoria(
    torneo_categoria_id: int, session: Session
) -> tuple[list[Fase], list[Partido]]:
    if bool_fase_final(session, torneo_categoria_id):
        return [], []
    equipos = get_equipos_participantes(session, torneo_categoria_id)
    cant_equipos = len(equipos)
    if cant_equipos < 2:
        return [], []

    # Indicamos la cantidad de fases
    cant_fases: int = ceil(log(cant_equipos, 2))
    fases_creadas = []
    partidos_creados = []
    partidos_ronda_sig = []  # lista de segunda iteracion
    i = 0
    for i in range(cant_fases):
        nombre_fase = f"Ronda {i}"
        if i == 0:
            nombre_fase = "Final"
        elif i == 1:
            nombre_fase = "Semifinal"
        elif i == 2:
            nombre_fase = "Cuartos de final"
        elif i == 3:
            nombre_fase = "Octavos de final"

        nueva_fase = Fase_schema(
            nombre=nombre_fase, orden=i, torneo_categoria_id=torneo_categoria_id
        )
        fase_db = fase.create(session, nueva_fase)
        fases_creadas.append(fase_db)
        # Obtenemos los partidos a jugar en la fase actual
        cant_partidos_fase: int = 2**i
        partidos_esta_ronda = []
        # La unica finalidad de esta linea es callar al pyright
        assert fase_db.id is not None

        for j in range(cant_partidos_fase):
            partido_sig_id = None

            if i > 0 and list(partidos_ronda_sig):
                partido_sig_id = partidos_ronda_sig[j // 2].id
            nuevo_partido = Partido_schema(
                # esta weaita del int esta nomas para callar al pyright
                fase_id=fase_db.id,
                partido_siguiente_id=partido_sig_id,
            )
            partido_db = partido.create(session, nuevo_partido)
            partidos_esta_ronda.append(partido_db)
            partidos_creados.append(partido_db)

        partidos_ronda_sig = partidos_esta_ronda

    fases_creadas.reverse()
    partidos_creados.reverse()
    return fases_creadas, partidos_creados


def inicializar_torneo(torneo_categoria_id: int, session: Session):
    try:
        equipos_en_torneo_categoria = get_equipos_participantes(
            session, torneo_categoria_id
        )
        cant_equipos = len(equipos_en_torneo_categoria)
        if cant_equipos < 2:
            raise ValueError("Se necesitan mas equipos")

        tam_fase = 2 ** ceil(log(cant_equipos, 2))
        random.shuffle(equipos_en_torneo_categoria)
        equipos_en_torneo_categoria += [None] * (tam_fase - cant_equipos)

        fase_inicial = session.exec(
            select(Fase)
            .where(Fase.torneo_categoria_id == torneo_categoria_id)
            .order_by(desc(Fase.orden))
        ).first()

        if fase_inicial is None:
            raise ValueError("No exite la fase, genere rondas primero")

        id_de_la_fase_mayor = fase_inicial.id
        partidos_fase_mayor = session.exec(
            select(Partido).where(Partido.fase_id == id_de_la_fase_mayor)
        ).all()

        for i, partido in enumerate(partidos_fase_mayor):
            equipo_a = equipos_en_torneo_categoria[i * 2]
            equipo_b = equipos_en_torneo_categoria[i * 2 + 1]

            if equipo_a is None and equipo_b is None:
                continue

            if partido.id is None:
                raise ValueError("Partido sin ID")

            if equipo_a is not None:
                partido_equipo.create(
                    session,
                    Partido_Equipo_schema(
                        ganador=False, partido_id=partido.id, equipo_id=equipo_a.id
                    ),
                )

            if equipo_b is not None:
                partido_equipo.create(
                    session,
                    Partido_Equipo_schema(
                        ganador=False, partido_id=partido.id, equipo_id=equipo_b.id
                    ),
                )

    except Exception:
        raise
