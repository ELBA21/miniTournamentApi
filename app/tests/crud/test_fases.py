import pytest


# ==============================================================================
# HELPER FIXTURE O FUNCIÓN AUXILIAR
# ==============================================================================
def _crear_torneo_categoria_real(client) -> int:
    """Helper para crear toda la cadena de dependencias y obtener un torneo_categoria_id real"""
    # 1. Crear Torneo
    torneo_res = client.post(
        "/torneo/create", json={"nombre": "Torneo Fases", "fecha": "2026-05-24"}
    )
    torneo_id = torneo_res.json()["id"]

    # 2. Crear Categoría
    categoria_res = client.post("/Categoria/create", json={"tipo": "Categoría Fases"})
    categoria_id = categoria_res.json()["id"]

    # 3. Vincularlos en TorneoCategoria
    tc_res = client.post(
        "/TorneoCategoria/create",
        json={"torneo_id": torneo_id, "categoria_id": categoria_id},
    )
    return tc_res.json()["id"]


# ==============================================================================
# TESTS PARA POST /create
# ==============================================================================


def test_crear_fase_exitoso(client):
    tc_id = _crear_torneo_categoria_real(client)

    payload = {"nombre": "Fase de Grupos", "orden": 1, "torneo_categoria_id": tc_id}
    response = client.post("/Fase/create", json=payload)

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["nombre"] == "Fase de Grupos"
    assert json_data["orden"] == 1
    assert json_data["torneo_categoria_id"] == tc_id
    assert "id" in json_data


def test_crear_fase_fallido_data_invalida(client):
    # Forzamos un error de validación en FastAPI enviando tipos incorrectos
    payload = {
        "nombre": "Fase Invalida",
        "orden": "no-soy-un-numero",
        "torneo_categoria_id": "tampoco",
    }
    response = client.post("/Fase/create", json=payload)
    assert response.status_code == 422


# ==============================================================================
# TESTS PARA GET /all y GET /{search_id}
# ==============================================================================


def test_obtener_todas_las_fases(client):
    response = client.get("/Fase/all")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_obtener_fase_por_id_exitoso(client):
    tc_id = _crear_torneo_categoria_real(client)

    # Creamos una fase
    payload = {"nombre": "Cuartos de Final", "orden": 2, "torneo_categoria_id": tc_id}
    crear_res = client.post("/Fase/create", json=payload)
    fase_id = crear_res.json()["id"]

    # La buscamos
    response = client.get(f"/Fase/{fase_id}")
    assert response.status_code == 200
    assert response.json()["nombre"] == "Cuartos de Final"


def test_obtener_fase_por_id_404(client):
    response = client.get("/Fase/9999")

    # Tu router maneja el LookupError devolviendo un 404 explícito
    assert response.status_code == 404
    assert "Fase no encontrado" in response.json()["detail"]


# ==============================================================================
# TESTS PARA PATCH /update/{search_id}
# ==============================================================================


def test_actualizar_fase_exitoso(client):
    tc_id = _crear_torneo_categoria_real(client)

    # Creamos la fase inicial
    payload_inicial = {"nombre": "Semifinal", "orden": 3, "torneo_categoria_id": tc_id}
    crear_res = client.post("/Fase/create", json=payload_inicial)
    fase_id = crear_res.json()["id"]

    # La modificamos con PATCH
    payload_update = {
        "nombre": "Semifinal Vuelta",
        "orden": 4,
        "torneo_categoria_id": tc_id,
    }
    response = client.patch(f"/Fase/update/{fase_id}", json=payload_update)

    assert response.status_code == 200
    assert response.json()["nombre"] == "Semifinal Vuelta"
    assert response.json()["orden"] == 4


def test_actualizar_fase_fallido_no_existe(client):
    payload_update = {"nombre": "Inexistente", "orden": 1, "torneo_categoria_id": 1}
    response = client.patch("/Fase/update/9999", json=payload_update)

    # Tu router atrapa el error general y responde con un 400
    assert response.status_code == 400


# ==============================================================================
# TESTS PARA DELETE /delete/{search_id}
# ==============================================================================


def test_eliminar_fase_exitoso(client):
    tc_id = _crear_torneo_categoria_real(client)

    # Creamos una fase para borrar
    payload = {"nombre": "Fase Eliminable", "orden": 5, "torneo_categoria_id": tc_id}
    crear_res = client.post("/Fase/create", json=payload)
    fase_id = crear_res.json()["id"]

    # La borramos
    response = client.delete(f"/Fase/delete/{fase_id}")
    assert response.status_code == 200
    assert response.json() is True

    # Verificamos que al intentar buscarla de nuevo de el 404 correspondiente
    chequeo = client.get(f"/Fase/{fase_id}")
    assert chequeo.status_code == 404


def test_eliminar_fase_fallido_no_existe(client):
    response = client.delete("/Fase/delete/9999")

    # Tu router maneja la excepción devolviendo un 400
    assert response.status_code == 400
