import pytest


# ==============================================================================
# HELPER FIXTURE O FUNCIÓN AUXILIAR
# ==============================================================================
def _crear_dependencias_puntaje(client):
    """Helper supremo que crea toda la jerarquía cruzada para darnos un partido_equipo_id y seccion_id reales"""
    # 1. Crear la cadena base (Torneo -> Categoría -> TorneoCategoria -> Fase -> Partido)
    t_res = client.post(
        "/torneo/create", json={"nombre": "Torneo Puntajes", "fecha": "2026-05-24"}
    )
    t_id = t_res.json()["id"]

    c_res = client.post("/Categoria/create", json={"tipo": "Categoría Puntajes"})
    c_id = c_res.json()["id"]

    tc_res = client.post(
        "/TorneoCategoria/create", json={"torneo_id": t_id, "categoria_id": c_id}
    )
    tc_id = tc_res.json()["id"]

    fase_res = client.post(
        "/Fase/create",
        json={"nombre": "Fase Finalísima", "orden": 1, "torneo_categoria_id": tc_id},
    )
    fase_id = fase_res.json()["id"]

    partido_res = client.post(
        "/Partido/create", json={"fase_id": fase_id, "partido_siguiente_id": None}
    )
    partido_id = partido_res.json()["id"]

    # 2. Crear un Equipo
    equipo_res = client.post("/Equipo/create", json={"nombre": "Taca Taca Stars"})
    equipo_id = equipo_res.json()["id"]

    # 3. Crear las dos dependencias directas de PuntajeEquipo
    # A) Partido_Equipo (AsignacionPartido)
    pe_res = client.post(
        "/AsignacionPartido/create",
        json={"ganador": None, "equipo_id": equipo_id, "partido_id": partido_id},
    )
    partido_equipo_id = pe_res.json()["id"]

    # B) Seccion
    seccion_res = client.post("/Seccion/create", json={"partido_id": partido_id})
    seccion_id = seccion_res.json()["id"]

    return partido_equipo_id, seccion_id


# ==============================================================================
# TESTS PARA POST /create
# ==============================================================================


def test_crear_puntaje_equipo_exitoso(client):
    partido_equipo_id, seccion_id = _crear_dependencias_puntaje(client)

    payload = {
        "puntaje": 7,  # Metieron 7 goles en esta sección o set
        "partido_equipo_id": partido_equipo_id,
        "seccion_id": seccion_id,
    }
    response = client.post("/PuntajeEquipo/create", json=payload)

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["partido_equipo_id"] == partido_equipo_id
    assert json_data["seccion_id"] == seccion_id
    assert json_data["puntaje"] == 7
    assert "id" in json_data


def test_crear_puntaje_equipo_fallido_data_invalida(client):
    payload = {"puntaje": "no-un-numero", "partido_equipo_id": 1, "seccion_id": 1}
    response = client.post("/PuntajeEquipo/create", json=payload)
    assert response.status_code == 422


# ==============================================================================
# TESTS PARA GET /all y GET /{search_id}
# ==============================================================================


def test_obtener_todos_los_puntajes(client):
    response = client.get("/PuntajeEquipo/all")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_obtener_puntaje_por_id_exitoso(client):
    partido_equipo_id, seccion_id = _crear_dependencias_puntaje(client)

    payload = {
        "puntaje": 5,
        "partido_equipo_id": partido_equipo_id,
        "seccion_id": seccion_id,
    }
    crear_res = client.post("/PuntajeEquipo/create", json=payload)
    puntaje_id = crear_res.json()["id"]

    response = client.get(f"/PuntajeEquipo/{puntaje_id}")
    assert response.status_code == 200
    assert response.json()["id"] == puntaje_id


def test_obtener_puntaje_por_id_404(client):
    response = client.get("/PuntajeEquipo/9999")
    assert response.status_code == 404
    assert "PuntajeEquipo no encontrado" in response.json()["detail"]


# ==============================================================================
# TESTS PARA PATCH /update/{search_id}
# ==============================================================================


def test_actualizar_puntaje_exitoso(client):
    partido_equipo_id, seccion_id = _crear_dependencias_puntaje(client)

    payload_inicial = {
        "puntaje": 2,
        "partido_equipo_id": partido_equipo_id,
        "seccion_id": seccion_id,
    }
    crear_res = client.post("/PuntajeEquipo/create", json=payload_inicial)
    puntaje_id = crear_res.json()["id"]

    # Corregimos el marcador (PATCH)
    payload_update = {
        "puntaje": 3,
        "partido_equipo_id": partido_equipo_id,
        "seccion_id": seccion_id,
    }
    response = client.patch(f"/PuntajeEquipo/update/{puntaje_id}", json=payload_update)

    assert response.status_code == 200
    assert response.json()["puntaje"] == 3


def test_actualizar_puntaje_fallido_no_existe(client):
    payload_update = {"puntaje": 5, "partido_equipo_id": 1, "seccion_id": 1}
    response = client.patch("/PuntajeEquipo/update/9999", json=payload_update)
    assert response.status_code == 400


# ==============================================================================
# TESTS PARA DELETE /delete/{search_id}
# ==============================================================================


def test_eliminar_puntaje_exitoso(client):
    partido_equipo_id, seccion_id = _crear_dependencias_puntaje(client)

    payload = {
        "puntaje": 0,
        "partido_equipo_id": partido_equipo_id,
        "seccion_id": seccion_id,
    }
    crear_res = client.post("/PuntajeEquipo/create", json=payload)
    puntaje_id = crear_res.json()["id"]

    response = client.delete(f"/PuntajeEquipo/delete/{puntaje_id}")
    assert response.status_code == 200
    assert response.json() is True

    # Verificamos desaparición
    chequeo = client.get(f"/PuntajeEquipo/{puntaje_id}")
    assert chequeo.status_code == 404


def test_eliminar_puntaje_fallido_no_existe(client):
    response = client.delete("/PuntajeEquipo/delete/9999")
    assert response.status_code == 400
