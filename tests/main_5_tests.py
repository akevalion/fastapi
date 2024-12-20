import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sqlite3
from fastapi.testclient import TestClient
from app.main_5 import app
import tempfile
import pytest


# Fixture para crear y limpiar la base de datos para cada prueba
@pytest.fixture(scope="function")
def client():

    temp_file = tempfile.NamedTemporaryFile(delete=True)
    connection = sqlite3.connect(temp_file.name)

    cursor = connection.cursor()
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        number INTEGER NOT NULL,
        date TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'waiting'
    )
    ''')
    connection.commit()

    # Sobrescribir la conexión de la aplicación para usar la base de datos en memoria
    def override_db_connection():
        return connection

    app.dependency_overrides[sqlite3.connect] = override_db_connection

    # Crear el cliente de pruebas
    client = TestClient(app)

    yield client  # Proveer el cliente para la prueba
    cursor.close()
    # Limpiar al final de la prueba
    cursor.close()
    connection.close()
    if not os.path.exists(temp_file.name):
        print("El archivo temporal fue eliminado correctamente.")
    else:
        print("El archivo temporal aún existe.")


    return connection


# Test para crear un ticket
def test_create_ticket(client):
    response = client.post("/create_ticket/")
    assert response.status_code == 200
    data = response.json()
    assert data["number"] == 1
    assert data["status"] == "waiting"


# Test para obtener tickets en espera
def test_get_tickets(client):
    client.post("/create_ticket/")  # Crear el primer ticket
    client.post("/create_ticket/")  # Crear el segundo ticket
    response = client.get("/tickets/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # Deben estar dos tickets en espera
    assert data[0]["number"] == 1
    assert data[1]["number"] == 2


# Test para procesar el siguiente ticket
def test_process_next_ticket(client):
    client.post("/create_ticket/")  # Crear un ticket
    response = client.put("/tickets/next/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "processed"

    # Verificar que no quedan tickets en espera
    response = client.get("/tickets/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0  # No deben quedar tickets en espera
