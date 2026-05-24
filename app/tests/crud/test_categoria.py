import pytest

# ==============================================================================
# TESTS PARA POST /create
# ==============================================================================


def test_crear_categoria_exitoso(client):
    payload = {"tipo": "Primera División"}
    response = client.post("/Categoria/create", json=payload)

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["tipo"] == "Primera División"
    assert "id" in json_data


def test_crear_categoria_fallido_tipo_invalido(client):
    # Test por si mandas un formato que rompa la estructura (ej: un array en vez de un str)
    payload = {"tipo": ["No", "es", "un", "string"]}
    response = client.post("/Categoria/create", json=payload)

    assert response.status_code == 422


# ==============================================================================
# TESTS PARA GET /all y GET /{categoria_id}
# ==============================================================================


def test_obtener_todas_las_categorias(client):
    response = client.get("/Categoria/all")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_obtener_categoria_por_id_exitoso(client):
    # Creamos una categoría de prueba
    payload = {"tipo": "Senior"}
    crear_res = client.post("/Categoria/create", json=payload)
    categoria_id = crear_res.json()["id"]

    # La buscamos
    response = client.get(f"/Categoria/{categoria_id}")

    assert response.status_code == 200
    assert response.json()["tipo"] == "Senior"


def test_obtener_categoria_por_id_400_not_found(client):
    # Buscamos un ID fantasma
    response = client.get("/Categoria/9999")

    # Tu router atrapa el LookupError y arroja un status_code=400
    assert response.status_code == 400
    assert "Categoria no encontrado" in response.json()["detail"]


# ==============================================================================
# TESTS PARA PUT /update/{categoria_id}
# ==============================================================================


def test_actualizar_categoria_exitoso(client):
    # Creamos la categoría inicial
    payload_inicial = {"tipo": "Junior"}
    crear_res = client.post("/Categoria/create", json=payload_inicial)
    categoria_id = crear_res.json()["id"]

    # La actualizamos usando PUT
    payload_update = {"tipo": "Master"}
    response = client.put(f"/Categoria/update/{categoria_id}", json=payload_update)

    assert response.status_code == 200
    assert response.json()["tipo"] == "Master"


def test_actualizar_categoria_fallido_no_existe(client):
    payload_update = {"tipo": "Inexistente"}
    response = client.put("/Categoria/update/9999", json=payload_update)

    assert response.status_code == 400


# ==============================================================================
# TESTS PARA DELETE /delete/{categoria_id}
# ==============================================================================


def test_eliminar_categoria_exitoso(client):
    # Creamos una para borrar
    payload = {"tipo": "A Borrar"}
    crear_res = client.post("/Categoria/create", json=payload)
    categoria_id = crear_res.json()["id"]

    # La borramos
    response = client.delete(f"/Categoria/delete/{categoria_id}")

    assert response.status_code == 200
    assert response.json() is True

    # Verificamos que al buscarla ya no exista (dará 400 por tu router)
    chequeo = client.get(f"/Categoria/{categoria_id}")
    assert chequeo.status_code == 400


def test_eliminar_categoria_fallido_no_existe(client):
    response = client.delete("/Categoria/delete/9999")

    assert response.status_code == 400
