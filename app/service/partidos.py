from app.models.schemas import Partido_Equipo_schema
from app.models.tables import Equipo, Partido, Partido_Equipo
from app.crud.factory import crud_partido_equipo as partido_equipo
from sqlmodel import Session, select
from typing import List


def obtener_equipos_en_partido(session: Session, partido_id: int) -> List[Equipo]:
    equipos = session.exec(
        select(Equipo)
        .join(Partido_Equipo)
        .where(Partido_Equipo.partido_id == partido_id)
    ).all()
    if not equipos:
        raise LookupError
    return list(equipos)


def definir_ganador_partido(session: Session, partido_id: int, equipo_ganador_id: int):
    equipos = obtener_equipos_en_partido(session, partido_id)

    partido_actual = session.get(Partido, partido_id)
    if partido_actual is None:
        raise LookupError

    ids_equipos = [e.id for e in equipos]
    if equipo_ganador_id not in ids_equipos:
        raise ValueError(
            f"El equipo {equipo_ganador_id} no pertenece al partido {partido_id}"
        )

    partido_equipos = session.exec(
        select(Partido_Equipo).where(Partido_Equipo.partido_id == partido_id)
    ).all()

    for pe in partido_equipos:
        pe.ganador = pe.equipo_id == equipo_ganador_id
        session.add(pe)

    if partido_actual.partido_siguiente_id is not None:
        partido_equipo.create(
            session,
            Partido_Equipo_schema(
                ganador=False,
                partido_id=partido_actual.partido_siguiente_id,
                equipo_id=equipo_ganador_id,
            ),
        )
    session.commit()
