from app.crud.base import CRUDBase
from app.models.schemas import (
    Carrera_schema,
    Categoria_schema,
    Equipo_schema,
    Fase_schema,
    Inscripcion_schema,
    JugadorSchema,
    Jugador_Equipo_schema,
    Partido_schema,
    Partido_Equipo_schema,
    PuntajeEquipo_schema,
    Seccion_schema,
    Torneo_schema,
    Torneos_Categorias_schema,
)
from app.models.tables import (
    Carrera,
    Categoria,
    Equipo,
    Fase,
    Inscripcion,
    Jugador,
    Jugador_Equipo,
    Partido,
    Partido_Equipo,
    PuntajeEquipo,
    Seccion,
    Torneo,
    Torneo_Categoria,
)

crud_carrera = CRUDBase[Carrera, Carrera_schema](Carrera)
crud_categoria = CRUDBase[Categoria, Categoria_schema](Categoria)
crud_equipo = CRUDBase[Equipo, Equipo_schema](Equipo)
crud_fase = CRUDBase[Fase, Fase_schema](Fase)
crud_inscripcion = CRUDBase[Inscripcion, Inscripcion_schema](Inscripcion)
crud_jugador = CRUDBase[Jugador, JugadorSchema](Jugador)
crud_jugador_equipo = CRUDBase[Jugador_Equipo, Jugador_Equipo_schema](Jugador_Equipo)
crud_partido = CRUDBase[Partido, Partido_schema](Partido)
crud_partido_equipo = CRUDBase[Partido_Equipo, Partido_Equipo_schema](Partido_Equipo)
crud_puntajeEquipo = CRUDBase[PuntajeEquipo, PuntajeEquipo_schema](PuntajeEquipo)
crud_seccion = CRUDBase[Seccion, Seccion_schema](Seccion)
crud_torneo = CRUDBase[Torneo, Torneo_schema](Torneo)
crud_torneo_categoria = CRUDBase[Torneo_Categoria, Torneos_Categorias_schema](
    Torneo_Categoria
)
