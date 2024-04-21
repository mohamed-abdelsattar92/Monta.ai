import pytest
from flask.testing import FlaskClient
from montaai.app import app
from datetime import timedelta


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


def test_login_expiration(client: FlaskClient, mocker):
    mock_create_access_token = mocker.patch("montaai.views.auth.create_access_token")
    mock_create_access_token.return_value = "test_token"
    response = client.post("/login", json={"username": "admin", "password": "admin"})
    mock_create_access_token.assert_called_once_with(
        identity="admin", expires_delta=timedelta(minutes=30)
    )
    assert response.status_code == 200
    assert "access_token" in response.get_json()
