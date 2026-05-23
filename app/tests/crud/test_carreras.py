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
