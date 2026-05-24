import pytest
from datetime import date

# ==============================================================================
# TESTS PARA POST /create
# ==============================================================================


def test_crear_torneo_exitoso(client):
    payload = {
        "nombre": "Torneo de Invierno Inacap",
        "fecha": "2026-06-15",  # Formato string ISO que Pydantic convierte a date
    }
    response = client.post("/torneo/create", json=payload)

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["nombre"] == "Torneo de Invierno Inacap"
    assert json_data["fecha"] == "2026-06-15"
    assert "id" in json_data


def test_crear_torneo_fallido_data_invalida(client):
    # Intentar enviar una fecha que no es una fecha válida
    payload = {"nombre": "Torneo Fake", "fecha": "esto-no-es-una-fecha"}
    response = client.post("/torneo/create", json=payload)

    # FastAPI/Pydantic frena esto antes de llegar al CRUD con un 422 Unprocessable Entity
    assert response.status_code == 422


# ==============================================================================
# TESTS PARA GET /all y GET /{search_id}
# ==============================================================================


def test_obtener_todos_los_torneos(client):
    response = client.get("/torneo/all")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_obtener_torneo_por_id_exitoso(client):
    # Creamos uno primero para garantizar que exista
    payload = {"nombre": "Torneo Flash", "fecha": "2026-05-24"}
    crear_res = client.post("/torneo/create", json=payload)
    torneo_id = crear_res.json()["id"]

    # Lo buscamos
    response = client.get(f"/torneo/{torneo_id}")

    assert response.status_code == 200
    assert response.json()["nombre"] == "Torneo Flash"


def test_obtener_torneo_por_id_404(client):
    # Buscamos un ID que no existe
    response = client.get("/torneo/9999")

    assert response.status_code == 404
    # Valida el mensaje de error dinámico de nuestro CRUDBase ("Torneo no encontrado")
    assert "Torneo no encontrado" in response.json()["detail"]


# ==============================================================================
# TESTS PARA PATCH /update/{search_id}
# ==============================================================================


def test_actualizar_torneo_exitoso(client):
    # Creamos el torneo original
    payload_inicial = {"nombre": "Torneo Inicial", "fecha": "2026-07-01"}
    crear_res = client.post("/torneo/create", json=payload_inicial)
    torneo_id = crear_res.json()["id"]

    # Lo modificamos (enviando datos nuevos)
    payload_update = {"nombre": "Torneo Modificado", "fecha": "2026-08-01"}
    response = client.patch(f"/torneo/update/{torneo_id}", json=payload_update)

    assert response.status_code == 200
    assert response.json()["nombre"] == "Torneo Modificado"
    assert response.json()["fecha"] == "2026-08-01"


def test_actualizar_torneo_fallido_no_existe(client):
    # Intentamos actualizar un ID fantasma
    payload_update = {"nombre": "Cualquier cosa", "fecha": "2026-05-24"}
    response = client.patch("/torneo/update/9999", json=payload_update)

    # Como internamente el update llama a get_by_id, el LookupError saltará y tu router responderá 400
    assert response.status_code == 400


# ==============================================================================
# TESTS PARA DELETE /delete/{search_id}
# ==============================================================================


def test_eliminar_torneo_exitoso(client):
    # Creamos uno para borrarlo
    payload = {"nombre": "Torneo Corto", "fecha": "2026-05-24"}
    crear_res = client.post("/torneo/create", json=payload)
    torneo_id = crear_res.json()["id"]

    # Lo borramos
    response = client.delete(f"/torneo/delete/{torneo_id}")

    assert response.status_code == 200
    assert response.json() is True  # Nuestro CRUDBase devuelve True si borró con éxito

    # Verificamos que realmente ya no exista
    chequeo = client.get(f"/torneo/{torneo_id}")
    assert chequeo.status_code == 404


def test_eliminar_torneo_fallido_no_existe(client):
    # Intentamos borrar un ID inexistente
    response = client.delete("/torneo/delete/9999")

    # El crud fallará al no encontrarlo, levantando una excepción que el router atrapa como 400
    assert response.status_code == 400
