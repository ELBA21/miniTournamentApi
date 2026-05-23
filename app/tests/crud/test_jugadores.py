from datetime import date


def test_crear_jugador_exitoso(client):
    # 1. Crear la carrera previa
    carrera_response = client.post(
        "/carrera/create", json={"nombre": "Ingeniería en Software"}
    )
    assert carrera_response.status_code == 200
    carrera_id = carrera_response.json()["id"]

    # 2. Crear el jugador usando el prefijo correcto /Jugador/create
    payload = {
        "nombre": "Benja",
        "puntaje": 10,
        "generacion": str(date.today()),
        "carrera_id": carrera_id,
    }

    response = client.post("/Jugador/create", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Benja"
    assert data["carrera_id"] == carrera_id


def test_obtener_todos_los_jugadores(client):
    # Crear carrera previa
    carrera_resp = client.post("/carrera/create", json={"nombre": "Diseño"})
    assert carrera_resp.status_code == 200
    carrera_id = carrera_resp.json()["id"]

    # Crear jugador previo usando /Jugador/create
    client.post(
        "/Jugador/create",
        json={
            "nombre": "Diego",
            "puntaje": 0,
            "generacion": "2026-03-01",
            "carrera_id": carrera_id,
        },
    )

    # Obtener todos usando /Jugador/get/all
    response = client.get("/Jugador/get/all")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1


def test_obtener_jugador_por_id_exitoso(client):
    # 1. Infraestructura mínima (Carrera + Jugador)
    carrera_resp = client.post("/carrera/create", json={"nombre": "Ici"})
    c_id = carrera_resp.json()["id"]

    jugador_resp = client.post(
        "/Jugador/create",
        json={
            "nombre": "Tomas",
            "puntaje": 5,
            "generacion": "2026-01-01",
            "carrera_id": c_id,
        },
    )
    j_id = jugador_resp.json()["id"]

    # 2. Testear el GET dinámico (Ojo con las mayúsculas en tu router `/get/{search_id}`)
    response = client.get(f"/Jugador/get/{j_id}")
    assert response.status_code == 200
    assert response.json()["nombre"] == "Tomas"


def test_actualizar_jugador_exitoso(client):
    carrera_resp = client.post("/carrera/create", json={"nombre": "Ici"})
    c_id = carrera_resp.json()["id"]

    jugador_resp = client.post(
        "/Jugador/create",
        json={
            "nombre": "Lucas",
            "puntaje": 20,
            "generacion": "2026-01-01",
            "carrera_id": c_id,
        },
    )
    j_id = jugador_resp.json()["id"]

    # 3. Testear el PATCH (Se envía solo lo que cambia, gracias a exclude_unset=True)
    payload_update = {"nombre": "Lucas Modificado", "puntaje": 50}
    response = client.patch(f"/Jugador/update/{j_id}", json=payload_update)

    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Lucas Modificado"
    assert data["puntaje"] == 50


def test_eliminar_jugador_exitoso(client):
    carrera_resp = client.post("/carrera/create", json={"nombre": "Ici"})
    c_id = carrera_resp.json()["id"]

    jugador_resp = client.post(
        "/Jugador/create",
        json={
            "nombre": "Borrame",
            "puntaje": 0,
            "generacion": "2026-01-01",
            "carrera_id": c_id,
        },
    )
    j_id = jugador_resp.json()["id"]

    # 4. Testear el DELETE
    delete_response = client.delete(f"/Jugador/delete/{j_id}")
    assert delete_response.status_code == 200

    # 5. Contra-prueba: Si intento buscarlo de nuevo, debería dar 404
    get_response = client.get(f"/Jugador/get/{j_id}")
    assert get_response.status_code == 404
