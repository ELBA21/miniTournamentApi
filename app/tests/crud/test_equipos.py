import pytest

# ==============================================================================
# TESTS PARA POST /create
# ==============================================================================


def test_crear_equipo_exitoso(client):
    payload = {"nombre": "Dream Team Taca-Taca"}
    response = client.post("/Equipo/create", json=payload)

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["nombre"] == "Dream Team Taca-Taca"
    assert "id" in json_data


def test_crear_equipo_fallido_data_invalida(client):
    # Intentamos mandar un tipo incorrecto en el campo 'nombre'
    payload = {"nombre": ["No", "soy", "un", "string"]}
    response = client.post("/Equipo/create", json=payload)

    # FastAPI/Pydantic frena esto inmediatamente con un 422 Unprocessable Entity
    assert response.status_code == 422


# ==============================================================================
# TESTS PARA GET /get/all y GET /get/{search_id}
# ==============================================================================


def test_obtener_todos_los_equipos(client):
    response = client.get("/Equipo/get/all")  # Respeta tu ruta /get/all

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_obtener_equipo_por_id_exitoso(client):
    # Creamos un equipo primero
    payload = {"nombre": "Real Taca"}
    crear_res = client.post("/Equipo/create", json=payload)
    equipo_id = crear_res.json()["id"]

    # Lo buscamos usando tu ruta con /get/
    response = client.get(f"/Equipo/get/{equipo_id}")

    assert response.status_code == 200
    assert response.json()["nombre"] == "Real Taca"


def test_obtener_equipo_por_id_404(client):
    response = client.get("/Equipo/get/9999")

    # Tu router en este endpoint lanza un 404 explícito en el LookupError
    assert response.status_code == 404
    assert "Equipo no encontrado" in response.json()["detail"]


# ==============================================================================
# TESTS PARA PATCH /update/{search_id}
# ==============================================================================


def test_actualizar_equipo_exitoso(client):
    # Creamos el equipo original
    payload_inicial = {"nombre": "Equipo A"}
    crear_res = client.post("/Equipo/create", json=payload_inicial)
    equipo_id = crear_res.json()["id"]

    # Lo modificamos con PATCH
    payload_update = {"nombre": "Equipo A Modificado"}
    response = client.patch(f"/Equipo/update/{equipo_id}", json=payload_update)

    assert response.status_code == 200
    assert response.json()["nombre"] == "Equipo A Modificado"


def test_actualizar_equipo_fallido_no_existe(client):
    payload_update = {"nombre": "Cualquier cosa"}
    response = client.patch("/Equipo/update/9999", json=payload_update)

    # Tu router atrapa el error general y responde con un 400
    assert response.status_code == 400


# ==============================================================================
# TESTS PARA DELETE /delete/{search_id}
# ==============================================================================


def test_eliminar_equipo_exitoso(client):
    # Creamos un equipo para borrar
    payload = {"nombre": "Equipo Borrable"}
    crear_res = client.post("/Equipo/create", json=payload)
    equipo_id = crear_res.json()["id"]

    # Lo borramos
    response = client.delete(f"/Equipo/delete/{equipo_id}")
    assert response.status_code == 200
    assert response.json() is True

    # Verificamos que al intentar buscarlo de nuevo de el 404 correspondiente
    chequeo = client.get(f"/Equipo/get/{equipo_id}")
    assert chequeo.status_code == 404


def test_eliminar_equipo_fallido_no_existe(client):
    response = client.delete("/Equipo/delete/9999")

    # Tu router maneja la excepción devolviendo un 400
    assert response.status_code == 400
