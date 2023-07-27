FROM python:3.11.4-slim-bullseye as base

RUN pip install poetry==1.5.1

# Configuring poetry
RUN poetry config virtualenvs.create false

WORKDIR /usr/src

# Copying requirements of a project
COPY pyproject.toml poetry.lock alembic.ini ./

# Installing requirements
RUN poetry install --no-root

ENTRYPOINT ["./deploy/entrypoint.sh"]

FROM base as dev

COPY . .

RUN chmod +x ./deploy/entrypoint.sh

RUN poetry install

FROM base as prod

COPY ./app ./app
COPY ./migrations ./migrations
COPY ./deploy/entrypoint.sh ./deploy/entrypoint.sh

RUN chmod +x ./deploy/entrypoint.sh

RUN poetry install --only main
