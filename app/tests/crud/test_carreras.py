# tests/test_carreras.py


def test_crear_carrera_exitoso(client):
    # Enviar datos correctos
    payload = {"nombre": "Ingeniería Civil Informática"}
    response = client.post("/carrera/create", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Ingeniería Civil Informática"
    assert "id" in data


def test_obtener_carrera_error_404(client):
    # Buscar un ID que no existe en la BD vacía de SQLite
    response = client.get("/carrera/get/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Carrera no encontrada"


def test_obtener_todas_las_carreras(client):
    # Primero creamos una carrera para tener algo que listar
    client.post("/carrera/create", json={"nombre": "Medicina"})

    response = client.get("/carrera/get/all")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["nombre"] == "Medicina"


def test_obtener_carrera_por_id_exitoso(client):
    carrera_resp = client.post("/carrera/create", json={"nombre": "Derecho"})
    carrera_id = carrera_resp.json()["id"]

    response = client.get(f"/carrera/get/{carrera_id}")
    assert response.status_code == 200
    assert response.json()["nombre"] == "Derecho"


def test_actualizar_carrera_exitoso(client):
    carrera_resp = client.post("/carrera/create", json={"nombre": "Psicología"})
    carrera_id = carrera_resp.json()["id"]

    payload_update = {"nombre": "Psicología Modificada"}
    response = client.put(f"/carrera/update/{carrera_id}", json=payload_update)

    assert response.status_code == 200
    assert response.json()["nombre"] == "Psicología Modificada"


def test_eliminar_carrera_exitoso(client):
    carrera_resp = client.post("/carrera/create", json={"nombre": "Arquitectura"})
    carrera_id = carrera_resp.json()["id"]

    # Eliminar
    delete_response = client.delete(f"/carrera/delete/{carrera_id}")
    assert delete_response.status_code == 200

    # Verificar que ya no existe
    get_response = client.get(f"/carrera/get/{carrera_id}")
    assert get_response.status_code == 404
