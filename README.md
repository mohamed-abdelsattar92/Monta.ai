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

## How To Run App

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

1. [POST] `/login`
1. [POST, GET] `/conversation`
1. [POST] `/send_message/<uuid:conversation_id>`
1. [GET] `/history`

### Demo

1. First use the login endpoint to login with the body structured as follows: ```{"username": "admin", "password": "admin"}```
   1. The returned token will be your authorization token thorough out the application and you'll need to send this as a Bearer token with any request to other endpoints.
1. Create a new conversation using the [POST] `/conversation` endpoint, it'll return a conversation id you'll be using with [POST] `/send_message/<uuid:conversation_id>` endpoint.
1. Send a message using [POST] `/send_message/<uuid:conversation_id>` endpoint where the body is structured as follows:```
  {
    "input": "<YOUR_MESSAGE>"
  }```.
1. Any message you'll send with the same `conversation_id` will take into consideration the context and history of the conversation so far.
