from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool

from app.database import sql_connection_check, create_db_and_tables
from app.config import FastAPIConfig, CorsConfig, ENV


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


# Healthcheck Endpoint
@app.get("/", tags=["Healthcheck"])
def healthcheck():
    return {"status": "ok", "name": app.title, "version": app.version, "env": ENV}
