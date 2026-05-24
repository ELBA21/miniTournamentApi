import pytest


# ==============================================================================
# HELPER FIXTURE O FUNCIÓN AUXILIAR
# ==============================================================================
def _crear_dependencias_fk(client):
    """Helper para crear un Torneo y una Categoría reales antes de vincularlos"""
    # 1. Crear Torneo
    torneo_res = client.post(
        "/torneo/create", json={"nombre": "Torneo Base", "fecha": "2026-05-24"}
    )
    torneo_id = torneo_res.json()["id"]

    # 2. Crear Categoría (Ojo con la mayúscula en /Categoria)
    categoria_res = client.post("/Categoria/create", json={"tipo": "Categoría Base"})
    categoria_id = categoria_res.json()["id"]

    return torneo_id, categoria_id


# ==============================================================================
# TESTS PARA POST /create
# ==============================================================================


def test_crear_torneo_categoria_exitoso(client):
    # Creamos primero los registros padres en la BD
    torneo_id, categoria_id = _crear_dependencias_fk(client)

    payload = {"torneo_id": torneo_id, "categoria_id": categoria_id}
    response = client.post("/TorneoCategoria/create", json=payload)

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["torneo_id"] == torneo_id
    assert json_data["categoria_id"] == categoria_id
    assert "id" in json_data


def test_crear_torneo_categoria_fallido_data_invalida(client):
    # Enviamos strings en vez de enteros para forzar la falla de validación
    payload = {"torneo_id": "no-soy-un-id", "categoria_id": "tampoco-soy-un-id"}
    response = client.post("/TorneoCategoria/create", json=payload)

    # FastAPI/Pydantic frena esto inmediatamente con un 422 Unprocessable Entity
    assert response.status_code == 422


# ==============================================================================
# TESTS PARA GET /all y GET /{search_id}
# ==============================================================================


def test_obtener_todos_los_tc(client):
    response = client.get("/TorneoCategoria/all")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_obtener_tc_por_id_exitoso(client):
    # Creamos la escena
    torneo_id, categoria_id = _crear_dependencias_fk(client)
    crear_res = client.post(
        "/TorneoCategoria/create",
        json={"torneo_id": torneo_id, "categoria_id": categoria_id},
    )
    tc_id = crear_res.json()["id"]

    # Buscamos por ID
    response = client.get(f"/TorneoCategoria/{tc_id}")
    assert response.status_code == 200
    assert response.json()["id"] == tc_id


def test_obtener_tc_por_id_404(client):
    response = client.get("/TorneoCategoria/9999")

    # Tu router en este endpoint lanza un 404 explícito en el LookupError
    assert response.status_code == 404
    assert "Torneo_Categoria no encontrado" in response.json()["detail"]


# ==============================================================================
# TESTS PARA DELETE /desvincular/{search_id}
# ==============================================================================


def test_desvincular_torneo_categoria_exitoso(client):
    # Creamos una relación
    torneo_id, categoria_id = _crear_dependencias_fk(client)
    crear_res = client.post(
        "/TorneoCategoria/create",
        json={"torneo_id": torneo_id, "categoria_id": categoria_id},
    )
    tc_id = crear_res.json()["id"]

    # Desvinculamos (Borramos)
    response = client.delete(f"/TorneoCategoria/desvincular/{tc_id}")
    assert response.status_code == 200
    assert response.json() is True

    # Comprobamos que efectivamente ya no exista
    chequeo = client.get(f"/TorneoCategoria/{tc_id}")
    assert chequeo.status_code == 404


def test_desvincular_torneo_categoria_fallido_no_existe(client):
    # Intentamos desvincular una relación que no existe
    response = client.delete("/TorneoCategoria/desvincular/9999")

    # Tu router atrapa la falla con una excepción general y responde 400
    assert response.status_code == 400
