from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool

from app.database import sql_connection_check, create_db_and_tables
from app.config import FastAPIConfig, CorsConfig, ENV
from app.routers.Carrera import router as carrera_router
from app.routers.Jugador import router as jugador_router
from app.routers.Equipo import router as equipo_router
from app.routers.Jugador_Equipo import router as jugador_Equipo_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Esto corre la función síncrona en un hilo separado de forma segura
    await run_in_threadpool(sql_connection_check)
    await run_in_threadpool(create_db_and_tables)
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


# Healthcheck Endpoint
@app.get("/", tags=["Healthcheck"])
def healthcheck():
    return {"status": "ok", "name": app.title, "version": app.version, "env": ENV}
