from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool

from app.database import sql_connection_check, create_db_and_tables
from app.config import FastAPIConfig, CorsConfig, ENV
from app.routers.crud.Carrera import router as carrera_router
from app.routers.crud.Jugador import router as jugador_router
from app.routers.crud.Equipo import router as equipo_router
from app.routers.crud.Jugador_Equipo import router as jugador_Equipo_router
from app.routers.crud.Categoria import router as categoria_router
from app.routers.crud.Torneo import router as torneo_router
from app.routers.crud.Torneo_Categoria import router as torneo_categoria_router
from app.routers.crud.Fase import router as fase_router
from app.routers.crud.Partido import router as partido_router
from app.routers.crud.Partido_Equipo import router as partido_equipo_router
from app.routers.crud.Seccion import router as seccion_router
from app.routers.crud.PuntajeEquipo import router as puntajeEquipo_router
from app.routers.crud.Inscripcion import router as inscripcion_router
from app.routers.service.tournament import router as fases_generador_router
from app.routers.service.partidos import router as partido_manager_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Esto corre la función síncrona en un hilo separado de forma segura
    await run_in_threadpool(sql_connection_check)
    # await run_in_threadpool(create_db_and_tables)
    yield


# Inicia fastAPI
app = FastAPI(**FastAPIConfig.dict(), lifespan=lifespan)


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CorsConfig.origins,
    allow_credentials=CorsConfig.allow_credentials,
    allow_methods=CorsConfig.allow_methods,
    allow_headers=CorsConfig.allow_headers,
    max_age=CorsConfig.max_age,
)
app.include_router(carrera_router)
app.include_router(jugador_router)
app.include_router(equipo_router)
app.include_router(jugador_Equipo_router)
app.include_router(categoria_router)
app.include_router(torneo_router)
app.include_router(torneo_categoria_router)
app.include_router(fase_router)
app.include_router(partido_router)
app.include_router(partido_equipo_router)
app.include_router(seccion_router)
app.include_router(puntajeEquipo_router)
app.include_router(inscripcion_router)
app.include_router(fases_generador_router)
app.include_router(partido_manager_router)


# Healthcheck Endpoint
@app.get("/", tags=["Healthcheck"])
def healthcheck():
    return {"status": "ok", "name": app.title, "version": app.version, "env": ENV}
