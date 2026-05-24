import pytest
from datetime import date


# ==============================================================================
# HELPER FIXTURE O FUNCIÓN AUXILIAR
# ==============================================================================
def _crear_dependencias_inscripcion(client):
    """Helper que crea un Equipo y un TorneoCategoria real para poder inscribir"""
    # 1. Crear Equipo (asumiendo prefijo /equipo o /Equipo según tu estándar, usamos /Equipo para asegurar)
    equipo_res = client.post(
        "/Equipo/create", json={"nombre": "Taca Taca Kings", "institucion": "Inacap"}
    )
    # Si tu endpoint de equipo está en minúscula, puedes cambiarlo a /equipo/create
    if equipo_res.status_code == 404:
        equipo_res = client.post(
            "/equipo/create",
            json={"nombre": "Taca Taca Kings", "institucion": "Inacap"},
        )
    equipo_id = equipo_res.json()["id"]

    # 2. Crear Torneo
    t_res = client.post(
        "/torneo/create", json={"nombre": "Torneo Clausura", "fecha": "2026-05-24"}
    )
    t_id = t_res.json()["id"]

    # 3. Crear Categoría
    c_res = client.post("/Categoria/create", json={"tipo": "Mixto"})
    c_id = c_res.json()["id"]

    # 4. Crear TorneoCategoria (Tabla intermedia)
    tc_res = client.post(
        "/TorneoCategoria/create", json={"torneo_id": t_id, "categoria_id": c_id}
    )
    tc_id = tc_res.json()["id"]

    return equipo_id, tc_id


# ==============================================================================
# TESTS PARA POST /create
# ==============================================================================


def test_crear_inscripcion_exitosa(client):
    equipo_id, tc_id = _crear_dependencias_inscripcion(client)

    payload = {
        "fecha": "2026-05-24",
        "equipo_id": equipo_id,
        "torneo_categoria_id": tc_id,
    }
    response = client.post("/Inscripcion/create", json=payload)

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["equipo_id"] == equipo_id
    assert json_data["torneo_categoria_id"] == tc_id
    assert "id" in json_data


def test_crear_inscripcion_fallida_data_invalida(client):
    # Enviamos una fecha con formato malo para gatillar el error de Pydantic
    payload = {"fecha": "fecha-invalida", "equipo_id": 1, "torneo_categoria_id": 1}
    response = client.post("/Inscripcion/create", json=payload)
    assert response.status_code == 422


# ==============================================================================
# TESTS PARA GET /all y GET /{search_id}
# ==============================================================================


def test_obtener_todas_las_inscripciones(client):
    response = client.get("/Inscripcion/all")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_obtener_inscripcion_por_id_exitosa(client):
    equipo_id, tc_id = _crear_dependencias_inscripcion(client)

    payload = {
        "fecha": "2026-05-24",
        "equipo_id": equipo_id,
        "torneo_categoria_id": tc_id,
    }
    crear_res = client.post("/Inscripcion/create", json=payload)
    inscripcion_id = crear_res.json()["id"]

    response = client.get(f"/Inscripcion/{inscripcion_id}")
    assert response.status_code == 200
    assert response.json()["id"] == inscripcion_id


def test_obtener_inscripcion_por_id_404(client):
    response = client.get("/Inscripcion/9999")
    assert response.status_code == 404
    assert "Inscripcion no encontrado" in response.json()["detail"]


# ==============================================================================
# TESTS PARA DELETE /anular/{search_id}
# ==============================================================================


def test_anular_inscripcion_exitosa(client):
    equipo_id, tc_id = _crear_dependencias_inscripcion(client)

    payload = {
        "fecha": "2026-05-24",
        "equipo_id": equipo_id,
        "torneo_categoria_id": tc_id,
    }
    crear_res = client.post("/Inscripcion/create", json=payload)
    inscripcion_id = crear_res.json()["id"]

    # Se anula la inscripción usando tu ruta personalizada /anular/
    response = client.delete(f"/Inscripcion/anular/{inscripcion_id}")
    assert response.status_code == 200
    assert response.json() is True

    # Verificamos que ya no exista buscando su ID
    chequeo = client.get(f"/Inscripcion/{inscripcion_id}")
    assert chequeo.status_code == 404


def test_anular_inscripcion_fallida_no_existe(client):
    response = client.delete("/Inscripcion/anular/9999")
    # Tu router atrapa la excepción general y devuelve un 400
    assert response.status_code == 400
