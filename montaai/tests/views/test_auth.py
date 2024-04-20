import pytest
from flask.testing import FlaskClient
from montaai.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_login_success(client: FlaskClient):
    response = client.post("/login", json={"username": "admin", "password": "admin"})
    assert response.status_code == 200
    assert "access_token" in response.get_json()


def test_login_failure(client: FlaskClient):
    response = client.post(
        "/login", json={"username": "admin", "password": "wrong_password"}
    )
    assert response.status_code == 401
    assert response.get_json() == {"msg": "Invalid username or password"}
