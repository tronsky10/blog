from model.user import User
from app.app import app, db
import pytest
python
# tests/test_app.py


@pytest.fixture(scope='module')
def test_client():
    # Configurar la aplicación para pruebas
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///test_database.db'
    })

    # Crear el cliente de pruebas
    testing_client = app.test_client()

    # Contexto de aplicación
    ctx = app.app_context()
    ctx.push()

    # Crear las tablas de la base de datos
    db.create_all()

    yield testing_client  # esto es lo que se utilizará en las pruebas

    db.drop_all()
    ctx.pop()


def test_home_page(test_client):
    """
    DADO un cliente Flask
    CUANDO la ruta '/' es solicitada (GET)
    ENTONCES revisa que la respuesta sea válida (200 OK)
    """
    response = test_client.get('/')
    assert response.status_code == 200
    # Asumiendo que 'Lista de Usuarios' es parte del contenido esperado
    assert b'Lista de Usuarios' in response.data

# Aquí se pueden agregar más pruebas, como la sumisión de formularios
