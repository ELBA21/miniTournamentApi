import pytest


# ==============================================================================
# HELPER FIXTURE O FUNCIÓN AUXILIAR
# ==============================================================================
def _crear_dependencias_jugador_equipo(client):
    """Helper optimizado para crear dependencias reales de forma segura"""
    # 1. Crear Equipo primero (este sabemos que funciona perfecto y no tiene FKs)
    equipo_res = client.post("/Equipo/create", json={"nombre": "Taca-Taca Devs"})
    equipo_id = equipo_res.json()["id"]

    # 2. Crear un Torneo y Categoría rápidos para tener una Carrera o datos válidos si se necesitan
    # Pero para ir a la segura con Jugador, intentaremos crearlo con un payload mínimo.
    # Si tu tabla jugador pide carrera_id obligatoria, primero creamos una carrera por HTTP:
    carrera_res = client.post("/carrera/create", json={"nombre": "Informática"})
    if carrera_res.status_code == 404:
        carrera_res = client.post("/Carrera/create", json={"nombre": "Informática"})

    carrera_id = carrera_res.json()["id"] if carrera_res.status_code == 200 else None

    # 3. Crear Jugador amarrado a esa carrera recién creada
    jugador_payload = {
        "nombre": "Benjamín",
        "apellido": "Gómez",
        "correo": "benja@test.com",
        "carrera_id": carrera_id,
    }

    jugador_res = client.post("/jugador/create", json=jugador_payload)
    if jugador_res.status_code == 404:
        jugador_res = client.post("/Jugador/create", json=jugador_payload)

    jugador_id = jugador_res.json()["id"]

    return jugador_id, equipo_id


# ==============================================================================
# TESTS PARA POST /create
# ==============================================================================


def test_crear_jugador_equipo_exitoso(client):
    jugador_id, equipo_id = _crear_dependencias_jugador_equipo(client)

    payload = {"puntaje": 10, "jugador_id": jugador_id, "equipo_id": equipo_id}
    response = client.post("/JugadorEquipo/create", json=payload)

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["jugador_id"] == jugador_id
    assert json_data["equipo_id"] == equipo_id
    assert json_data["puntaje"] == 10
    assert "id" in json_data


def test_crear_jugador_equipo_fallido_data_invalida(client):
    # Forzamos error de validación de Pydantic mandando un string en vez de un int en puntaje
    payload = {"puntaje": "muchos-puntos", "jugador_id": 1, "equipo_id": 1}
    response = client.post("/JugadorEquipo/create", json=payload)
    assert response.status_code == 422


# ==============================================================================
# TESTS PARA GET /get/all y GET /get/byId/{search_id}
# ==============================================================================


def test_obtener_todas_las_asignaciones(client):
    response = client.get("/JugadorEquipo/get/all")  # Respeta tu ruta /get/all
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_obtener_asignacion_por_id_exitosa(client):
    jugador_id, equipo_id = _crear_dependencias_jugador_equipo(client)

    payload = {"puntaje": 0, "jugador_id": jugador_id, "equipo_id": equipo_id}
    crear_res = client.post("/JugadorEquipo/create", json=payload)
    relacion_id = crear_res.json()["id"]

    response = client.get(
        f"/JugadorEquipo/get/byId/{relacion_id}"
    )  # Respeta tu ruta /get/byId/{id}
    assert response.status_code == 200
    assert response.json()["id"] == relacion_id


def test_obtener_asignacion_por_id_404(client):
    response = client.get("/JugadorEquipo/get/byId/9999")
    assert response.status_code == 404
    assert "Jugador_Equipo no encontrado" in response.json()["detail"]


# ==============================================================================
# TESTS PARA PATCH /update/{search_id}
# ==============================================================================


def test_actualizar_jugador_equipo_exitoso(client):
    jugador_id, equipo_id = _crear_dependencias_jugador_equipo(client)

    payload_inicial = {"puntaje": 0, "jugador_id": jugador_id, "equipo_id": equipo_id}
    crear_res = client.post("/JugadorEquipo/create", json=payload_inicial)
    relacion_id = crear_res.json()["id"]

    # Modificamos el puntaje del jugador en el equipo
    payload_update = {"puntaje": 25, "jugador_id": jugador_id, "equipo_id": equipo_id}
    response = client.patch(f"/JugadorEquipo/update/{relacion_id}", json=payload_update)

    assert response.status_code == 200
    assert response.json()["puntaje"] == 25


def test_actualizar_jugador_equipo_fallido_no_existe(client):
    payload_update = {"puntaje": 100, "jugador_id": 1, "equipo_id": 1}
    response = client.patch("/JugadorEquipo/update/9999", json=payload_update)
    assert response.status_code == 400


# ==============================================================================
# TESTS PARA DELETE /separar/{search_id}
# ==============================================================================


def test_separar_jugador_equipo_exitoso(client):
    jugador_id, equipo_id = _crear_dependencias_jugador_equipo(client)

    payload = {"puntaje": 0, "jugador_id": jugador_id, "equipo_id": equipo_id}
    crear_res = client.post("/JugadorEquipo/create", json=payload)
    relacion_id = crear_res.json()["id"]

    # Eliminamos la relación con tu ruta /separar/
    response = client.delete(f"/JugadorEquipo/separar/{relacion_id}")
    assert response.status_code == 200
    assert response.json() is True

    # Comprobamos que de el 404 correspondiente al buscarlo de nuevo
    chequeo = client.get(f"/JugadorEquipo/get/byId/{relacion_id}")
    assert chequeo.status_code == 404


def test_separar_jugador_equipo_fallido_no_existe(client):
    response = client.delete("/JugadorEquipo/separar/9999")
    assert response.status_code == 400
