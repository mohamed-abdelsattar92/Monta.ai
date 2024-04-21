# Monta AI BE Task

## Required Installation Steps

- Install Poetry by following this [guide](https://formulae.brew.sh/formula/poetry)
- Install pyenv by following this [guide](https://github.com/pyenv/pyenv?tab=readme-ov-file#getting-pyenv)
- Install python 3.12 by using the following command
``` pyenv install 3.12 ```

- Navigate to `montaai` parent directory and run the following commands

```shell
poetry env use ~/.pyenv/versions/<PYTHON_VERSION>/bin/python --> <PYTHON_VERSION> should be 3.12.<SOMETHING>
poetry install 
```

## How To Run App Locally

- Run the following command to load the environment variables
``` source env.sh ```
  - `env.sh` file will be given upon request to needed parties.
- Navigate to `montaai` parent directory and run the following command to start a poetry shell

```shell
poetry shell
```

- Navigate to `montaai/montaai` directory where `app.py` file is found and Run the following command to run the flask server
``` flask run ```
- Now in your browser navigate to `localhost:5000` and voila you're in!

## How to Run Tests

- Run the following command while in the `montaai` parent directory
``` pytest tests/views ```

## How to Interact with the Application

### Endpoints

All in all this app has 5 endpoints that you can interact with listed below:

1. [POST] `/v1/login`
1. [POST, GET] `/v1/conversation`
1. [POST] `/v1/conversation/<uuid:conversation_id>/message`
1. [GET] `/v1/conversations`

### Demo

1. First use the login endpoint to login with your username and password.
   1. The returned token will be your authorization token thorough out the application and you'll need to send this as a Bearer token with any request to other endpoints.
   1. Curl: usernames can be one of `admin`, `user1`, `user2` and password will always be `admin`.
   1. Application can handle multiple users meaning you can login with `admin` create some conversations and have a chat with the API and then login with `user1` and create other conversations and both users will have their own history and conversations.
  
  ```bash
  curl --location 'http://ec2-34-219-107-153.us-west-2.compute.amazonaws.com/login' \
--header 'Content-Type: application/json' \
--data '{
    "username": "admin",
    "password": "admin"
}'
```

1. Create a new conversation using the [POST] `/v1/conversation` endpoint:
   1. Curl

```bash
curl --location --request POST 'http://ec2-34-219-107-153.us-west-2.compute.amazonaws.com/conversation' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMzcxOTg3NiwianRpIjoiOThlNjc5MTgtNGM1My00YmIxLWFkMTktYTUwN2FiNjlhMzdjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNzEzNzE5ODc2LCJjc3JmIjoiYzA4ZDA5MTAtMThhNy00ZDhkLTk5NGUtMTBkNTZkMGJkYTkyIiwiZXhwIjoxNzEzNzIxNjc2fQ.uTMDj31vW8rw2Y_PXeJNIb3eJlSG4PAuSNt3ykELgWI'
```

it'll return a conversation id you'll be using with [POST] `/v1/conversation/<uuid:conversation_id>/message` endpoint.

1. Send a message using [POST] `/v1/conversation/<uuid:conversation_id>/message` endpoint 
   1. Curl: You'll need to change authorization token with what has been returned from the `/v1/login` endpoint.

```bash
curl --location 'http://ec2-34-219-107-153.us-west-2.compute.amazonaws.com/conversation/e5b315bf-d34a-4a94-93e0-126f224b39f2/message' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMzcxOTg3NiwianRpIjoiOThlNjc5MTgtNGM1My00YmIxLWFkMTktYTUwN2FiNjlhMzdjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNzEzNzE5ODc2LCJjc3JmIjoiYzA4ZDA5MTAtMThhNy00ZDhkLTk5NGUtMTBkNTZkMGJkYTkyIiwiZXhwIjoxNzEzNzIxNjc2fQ.uTMDj31vW8rw2Y_PXeJNIb3eJlSG4PAuSNt3ykELgWI' \
--data '{
    "message": "Hello"
}'
```

1. Any message you'll send with the same `conversation_id` will take into consideration the context and history of the conversation so far.

### Application Online Hosted Link

[App](http://ec2-34-219-107-153.us-west-2.compute.amazonaws.com/), where you can interact with the app without local installations.
