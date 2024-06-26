import pytest
from flask.testing import FlaskClient
from montaai.app import app
from uuid import uuid4
from flask_jwt_extended import (
    create_access_token,
)
from montaai.helpers import chat_history
from collections import namedtuple


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def get_test_access_token():
    with app.app_context():
        access_token = create_access_token(identity="test_user")
        return access_token


def create_test_conversation():
    conversation_id = str(uuid4())
    user_id = "test_user"
    chat_history[user_id] = {}
    chat_history[user_id][conversation_id] = []
    return conversation_id


def test_create_new_conversation(client: FlaskClient):
    access_token = get_test_access_token()
    response = client.post(
        "/v1/conversation", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert "New conversation created with id:" in response.get_json()["message"]


def test_get_conversation_success(client: FlaskClient):
    access_token = get_test_access_token()
    conversation_id = create_test_conversation()
    response = client.get(
        f"/v1/conversation/{conversation_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert {f"{conversation_id}": []} == response.get_json()


def test_get_conversation_failure(client: FlaskClient):
    access_token = get_test_access_token()
    non_existent_id = uuid4()
    response = client.get(
        f"/v1/conversation/{non_existent_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.get_json() == {"error": "Conversation not found"}


def test_send_message_success(client: FlaskClient, mocker):
    access_token = get_test_access_token()
    conversation_id = create_test_conversation()

    # Define a method to create the namedtuple
    def create_namedtuple():
        # Define the namedtuple types
        Message = namedtuple("Message", ["role", "content"])
        Choice = namedtuple("Choice", ["message"])
        Completions = namedtuple("Completions", ["choices"])

        # Create the namedtuple instances
        message = Message(role="assistant", content="Hello, world!")
        choice = Choice(message=message)
        choices = [choice]

        # Create the Completions namedtuple
        completions = Completions(choices=choices)

        return completions

    # Mock the openai.OpenAI().chat.completions.create function
    mock_create = mocker.patch(
        "montaai.views.conversation.openai_client.chat.completions.create"
    )
    mock_create.return_value = create_namedtuple()

    response = client.post(
        f"/v1/conversation/{conversation_id}/message",
        json={"message": "Hello, world!"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert "Hello, world!" == response.get_json()["response"]


def test_send_message_failure(client: FlaskClient):
    access_token = get_test_access_token()
    non_existent_id = uuid4()
    response = client.post(
        f"/v1/conversation/{non_existent_id}/message",
        json={"message": ", world!"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.get_json() == {"error": "Please enter the correct conversation id!"}


def test_history(client: FlaskClient):
    access_token = get_test_access_token()
    response = client.get(
        "/v1/conversations", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert "conversations" in response.get_json()
