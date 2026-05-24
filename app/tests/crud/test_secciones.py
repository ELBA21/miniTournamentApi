import pytest


# ==============================================================================
# HELPER FIXTURE O FUNCIÓN AUXILIAR
# ==============================================================================
def _crear_partido_real(client) -> int:
    """Helper que crea toda la estructura jerárquica para darnos un partido_id real"""
    # 1. Torneo
    t_res = client.post(
        "/torneo/create", json={"nombre": "Torneo Secciones", "fecha": "2026-05-24"}
    )
    t_id = t_res.json()["id"]

    # 2. Categoría
    c_res = client.post("/Categoria/create", json={"tipo": "Categoría Secciones"})
    c_id = c_res.json()["id"]

    # 3. TorneoCategoria
    tc_res = client.post(
        "/TorneoCategoria/create", json={"torneo_id": t_id, "categoria_id": c_id}
    )
    tc_id = tc_res.json()["id"]

    # 4. Fase
    fase_res = client.post(
        "/Fase/create",
        json={"nombre": "Fase Final", "orden": 1, "torneo_categoria_id": tc_id},
    )
    fase_id = fase_res.json()["id"]

    # 5. Partido
    partido_res = client.post(
        "/Partido/create", json={"fase_id": fase_id, "partido_siguiente_id": None}
    )
    return partido_res.json()["id"]


# ==============================================================================
# TESTS PARA POST /create
# ==============================================================================


def test_crear_seccion_exitosa(client):
    partido_id = _crear_partido_real(client)

    payload = {"partido_id": partido_id}
    response = client.post("/Seccion/create", json=payload)

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["partido_id"] == partido_id
    assert "id" in json_data


def test_crear_seccion_fallida_data_invalida(client):
    # Intentamos mandar un string en vez de un entero en partido_id
    payload = {"partido_id": "id-invalido-string"}
    response = client.post("/Seccion/create", json=payload)
    assert response.status_code == 422


# ==============================================================================
# TESTS PARA GET /all y GET /{search_id}
# ==============================================================================


def test_obtener_todas_las_secciones(client):
    response = client.get("/Seccion/all")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_obtener_seccion_por_id_exitosa(client):
    partido_id = _crear_partido_real(client)

    # Creamos una sección de prueba
    crear_res = client.post("/Seccion/create", json={"partido_id": partido_id})
    seccion_id = crear_res.json()["id"]

    # La buscamos por su ID
    response = client.get(f"/Seccion/{seccion_id}")
    assert response.status_code == 200
    assert response.json()["id"] == seccion_id


def test_obtener_seccion_por_id_404(client):
    response = client.get("/Seccion/9999")
    assert response.status_code == 404
    assert "Seccion no encontrado" in response.json()["detail"]


# ==============================================================================
# TESTS PARA PATCH /update/{search_id}
# ==============================================================================


def test_actualizar_seccion_exitosa(client):
    partido_id_1 = _crear_partido_real(client)
    partido_id_2 = _crear_partido_real(client)

    # Creamos una sección amarrada al primer partido
    crear_res = client.post("/Seccion/create", json={"partido_id": partido_id_1})
    seccion_id = crear_res.json()["id"]

    # La cambiamos de partido mediante PATCH
    payload_update = {"partido_id": partido_id_2}
    response = client.patch(f"/Seccion/update/{seccion_id}", json=payload_update)

    assert response.status_code == 200
    assert response.json()["partido_id"] == partido_id_2


def test_actualizar_seccion_fallida_no_existe(client):
    payload_update = {"partido_id": 1}
    response = client.patch("/Seccion/update/9999", json=payload_update)
    assert response.status_code == 400


# ==============================================================================
# TESTS PARA DELETE /delete/{search_id}
# ==============================================================================


def test_eliminar_seccion_exitosa(client):
    partido_id = _crear_partido_real(client)

    # Creamos una sección para borrar
    crear_res = client.post("/Seccion/create", json={"partido_id": partido_id})
    seccion_id = crear_res.json()["id"]

    # La borramos
    response = client.delete(f"/Seccion/delete/{seccion_id}")
    assert response.status_code == 200
    assert response.json() is True

    # Verificamos que ya no exista
    chequeo = client.get(f"/Seccion/{seccion_id}")
    assert chequeo.status_code == 404


def test_eliminar_seccion_fallida_no_existe(client):
    response = client.delete("/Seccion/delete/9999")
    assert response.status_code == 400
