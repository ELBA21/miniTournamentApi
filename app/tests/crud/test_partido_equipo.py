import pytest


# ==============================================================================
# HELPER FIXTURE O FUNCIÓN AUXILIAR
# ==============================================================================
def _crear_dependencias_partido_equipo(client):
    """Helper que crea un Equipo y un Partido reales en la BD para poder vincularlos"""
    # 1. Crear Equipo
    equipo_res = client.post("/Equipo/create", json={"nombre": "Taca Taca Masters"})
    equipo_id = equipo_res.json()["id"]

    # 2. Crear la cadena para el Partido (Torneo -> Categoría -> TorneoCategoria -> Fase -> Partido)
    t_res = client.post(
        "/torneo/create", json={"nombre": "Torneo Vinculos", "fecha": "2026-05-24"}
    )
    t_id = t_res.json()["id"]

    c_res = client.post("/Categoria/create", json={"tipo": "Categoría Vinculos"})
    c_id = c_res.json()["id"]

    tc_res = client.post(
        "/TorneoCategoria/create", json={"torneo_id": t_id, "categoria_id": c_id}
    )
    tc_id = tc_res.json()["id"]

    fase_res = client.post(
        "/Fase/create",
        json={"nombre": "Fase Única", "orden": 1, "torneo_categoria_id": tc_id},
    )
    fase_id = fase_res.json()["id"]

    partido_res = client.post(
        "/Partido/create", json={"fase_id": fase_id, "partido_siguiente_id": None}
    )
    partido_id = partido_res.json()["id"]

    return equipo_id, partido_id


# ==============================================================================
# TESTS PARA POST /create
# ==============================================================================


def test_crear_partido_equipo_exitoso(client):
    equipo_id, partido_id = _crear_dependencias_partido_equipo(client)

    payload = {
        "ganador": None,  # Al crearse, el partido aún no se juega
        "equipo_id": equipo_id,
        "partido_id": partido_id,
    }
    response = client.post("/AsignacionPartido/create", json=payload)

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["equipo_id"] == equipo_id
    assert json_data["partido_id"] == partido_id
    assert json_data["ganador"] is None
    assert "id" in json_data


def test_crear_partido_equipo_fallido_data_invalida(client):
    # Forzamos error enviando un tipo incorrecto en un campo FK entero
    payload = {"ganador": True, "equipo_id": "no-un-id", "partido_id": 1}
    response = client.post("/AsignacionPartido/create", json=payload)
    assert response.status_code == 422


# ==============================================================================
# TESTS PARA GET /all
# ==============================================================================


def test_obtener_todos_los_vinculos(client):
    response = client.get("/AsignacionPartido/all")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ==============================================================================
# TESTS PARA PATCH /update/{search_id}
# ==============================================================================


def test_actualizar_partido_equipo_exitoso(client):
    equipo_id, partido_id = _crear_dependencias_partido_equipo(client)

    payload_inicial = {
        "ganador": None,
        "equipo_id": equipo_id,
        "partido_id": partido_id,
    }
    crear_res = client.post("/AsignacionPartido/create", json=payload_inicial)
    vinculo_id = crear_res.json()["id"]

    # Se terminó el partido y este equipo ganó, actualizamos el estado
    payload_update = {"ganador": True, "equipo_id": equipo_id, "partido_id": partido_id}
    response = client.patch(
        f"/AsignacionPartido/update/{vinculo_id}", json=payload_update
    )

    assert response.status_code == 200
    assert response.json()["ganador"] is True


def test_actualizar_partido_equipo_fallido_no_existe(client):
    payload_update = {"ganador": False, "equipo_id": 1, "partido_id": 1}
    response = client.patch("/AsignacionPartido/update/9999", json=payload_update)
    assert response.status_code == 400


# ==============================================================================
# TESTS PARA DELETE /eliminar/{search_id}
# ==============================================================================


def test_eliminar_vinculo_exitoso(client):
    equipo_id, partido_id = _crear_dependencias_partido_equipo(client)

    payload = {"ganador": None, "equipo_id": equipo_id, "partido_id": partido_id}
    crear_res = client.post("/AsignacionPartido/create", json=payload)
    vinculo_id = crear_res.json()["id"]

    # Lo eliminamos usando tu ruta personalizada /eliminar/
    response = client.delete(f"/AsignacionPartido/eliminar/{vinculo_id}")
    assert response.status_code == 200
    assert response.json() is True


def test_eliminar_vinculo_fallido_no_existe(client):
    response = client.delete("/AsignacionPartido/eliminar/9999")
    assert response.status_code == 400
