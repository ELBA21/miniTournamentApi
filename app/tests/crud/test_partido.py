import pytest


# ==============================================================================
# HELPER FIXTURE O FUNCIÓN AUXILIAR
# ==============================================================================
def _crear_fase_real(client) -> int:
    """Helper que crea toda la jerarquía de dependencias para darnos un fase_id real"""
    # 1. Torneo
    t_res = client.post(
        "/torneo/create", json={"nombre": "Torneo Partidos", "fecha": "2026-05-24"}
    )
    t_id = t_res.json()["id"]

    # 2. Categoría
    c_res = client.post("/Categoria/create", json={"tipo": "Categoría Partidos"})
    c_id = c_res.json()["id"]

    # 3. TorneoCategoria
    tc_res = client.post(
        "/TorneoCategoria/create", json={"torneo_id": t_id, "categoria_id": c_id}
    )
    tc_id = tc_res.json()["id"]

    # 4. Fase
    fase_res = client.post(
        "/Fase/create",
        json={"nombre": "Playoffs", "orden": 1, "torneo_categoria_id": tc_id},
    )
    return fase_res.json()["id"]


# ==============================================================================
# TESTS PARA POST /create
# ==============================================================================


def test_crear_partido_exitoso(client):
    fase_id = _crear_fase_real(client)

    payload = {
        "fase_id": fase_id,
        "partido_siguiente_id": None,  # Primer partido no tiene uno siguiente necesariamente
    }
    response = client.post("/Partido/create", json=payload)

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["fase_id"] == fase_id
    assert json_data["partido_siguiente_id"] is None
    assert "id" in json_data


def test_crear_partido_con_partido_siguiente(client):
    fase_id = _crear_fase_real(client)

    # 1. Creamos el partido que irá después (la final, por ejemplo)
    res_final = client.post(
        "/Partido/create", json={"fase_id": fase_id, "partido_siguiente_id": None}
    )
    final_id = res_final.json()["id"]

    # 2. Creamos el partido actual (la semifinal) apuntando a la final
    payload = {"fase_id": fase_id, "partido_siguiente_id": final_id}
    response = client.post("/Partido/create", json=payload)

    assert response.status_code == 200
    assert response.json()["partido_siguiente_id"] == final_id


def test_crear_partido_fallido_data_invalida(client):
    payload = {
        "fase_id": "se-supone-que-soy-un-int",
        "partido_siguiente_id": "yo-igual",
    }
    response = client.post("/Partido/create", json=payload)
    assert response.status_code == 422


# ==============================================================================
# TESTS PARA GET /get/all y GET /get/{search_id}
# ==============================================================================


def test_obtener_todos_los_partidos(client):
    response = client.get("/Partido/get/all")  # Ojo con tu ruta /get/all
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_obtener_partido_por_id_exitoso(client):
    fase_id = _crear_fase_real(client)
    crear_res = client.post(
        "/Partido/create", json={"fase_id": fase_id, "partido_siguiente_id": None}
    )
    partido_id = crear_res.json()["id"]

    response = client.get(f"/Partido/get/{partido_id}")  # Ojo con tu ruta /get/{id}
    assert response.status_code == 200
    assert response.json()["id"] == partido_id


def test_obtener_partido_por_id_404(client):
    response = client.get("/Partido/get/9999")
    assert response.status_code == 404
    assert "Partido no encontrado" in response.json()["detail"]


# ==============================================================================
# TESTS PARA PATCH /update/{search_id}
# ==============================================================================


def test_actualizar_partido_exitoso(client):
    fase_id = _crear_fase_real(client)

    # Creamos partido inicial
    crear_res = client.post(
        "/Partido/create", json={"fase_id": fase_id, "partido_siguiente_id": None}
    )
    partido_id = crear_res.json()["id"]

    # Creamos otro partido para simular que ahora sí tiene un partido siguiente
    res_siguiente = client.post(
        "/Partido/create", json={"fase_id": fase_id, "partido_siguiente_id": None}
    )
    sig_id = res_siguiente.json()["id"]

    # Actualizamos
    payload_update = {"fase_id": fase_id, "partido_siguiente_id": sig_id}
    response = client.patch(f"/Partido/update/{partido_id}", json=payload_update)

    assert response.status_code == 200
    assert response.json()["partido_siguiente_id"] == sig_id


def test_actualizar_partido_fallido_no_existe(client):
    payload_update = {"fase_id": 1, "partid_siguiente_id": None}
    response = client.patch("/Partido/update/9999", json=payload_update)
    assert response.status_code == 400


# ==============================================================================
# TESTS PARA DELETE /delete/{search_id}
# ==============================================================================


def test_eliminar_partido_exitoso(client):
    fase_id = _crear_fase_real(client)
    crear_res = client.post(
        "/Partido/create", json={"fase_id": fase_id, "partido_siguiente_id": None}
    )
    partido_id = crear_res.json()["id"]

    response = client.delete(f"/Partido/delete/{partido_id}")
    assert response.status_code == 200
    assert response.json() is True

    # Verificamos desparición
    chequeo = client.get(f"/Partido/get/{partido_id}")
    assert chequeo.status_code == 404


def test_eliminar_partido_fallido_no_existe(client):
    response = client.delete("/Partido/delete/9999")
    assert response.status_code == 400
