from sqlmodel import Session, asc, select
from app.models.tables import Fase, Partido, Partido_Equipo, Equipo


def get_bracket(session: Session, torneo_categoria_id: int):
    fases = session.exec(
        select(Fase)
        .where(Fase.torneo_categoria_id == torneo_categoria_id)
        .order_by(asc(Fase.orden))
    ).all()
    resultado = []
    for fase in fases:
        partidos = session.exec(select(Partido).where(Partido.fase_id == fase.id)).all()
        partidos_data = []

        for partido in partidos:
            partido_equipos = session.exec(
                select(Partido_Equipo).where(Partido_Equipo.partido_id == partido.id)
            ).all()

            equipo_data = []
            for pe in partido_equipos:
                equipo = session.get(Equipo, pe.equipo_id)
                if equipo is not None:
                    equipo_data.append(
                        {
                            "id": equipo.id,
                            "nombre": equipo.nombre,
                            "ganador": pe.ganador,
                        }
                    )
            partidos_data.append(
                {
                    "id": partido.id,
                    "partido_siguiente_id": partido.partido_siguiente_id,
                    "equipo": equipo_data,
                }
            )
        resultado.append(
            {"nombre": fase.nombre, "orden": fase.orden, "partidos": partidos_data}
        )
    return resultado
