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
