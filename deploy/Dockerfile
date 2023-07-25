FROM python:3.11.4-slim-bullseye as base

RUN pip install poetry==1.5.1

# Configuring poetry
RUN poetry config virtualenvs.create false

WORKDIR /usr/src

# Copying requirements of a project
COPY ../pyproject.toml poetry.lock ./

# Installing requirements
RUN poetry install --no-root

CMD ["/usr/local/bin/python", "-m", "app"]

FROM base as dev

COPY .. .

RUN poetry install

FROM base as prod

COPY ../app ./app

RUN poetry install --only main