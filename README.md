# Turing Machine Game API

API for building an interactive Turing Machine game

[![Server Health Check](https://github.com/kwsong0113/turing-machine-api/actions/workflows/health.yml/badge.svg)](https://github.com/kwsong0113/turing-machine-api/actions/workflows/health.yml)

---

**Documentation**: [Swagger UI](http://43.200.120.78/docs) / [Redoc](http://43.200.120.78/redoc)

---
## Built With
### Server
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
### Database
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
<br/>
### Devops / Deployment
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)

## Getting Started
### Installation
```shell
# Development
poetry install
# Production
poetry install --only main
```
### Run Locally
```shell
# Create and start container on local Docker environment
docker-compose --project-directory . \
-f deploy/docker-compose.base.yml \
-f deploy/docker-compose.dev.yml \
up -d --build   
```
### Deployment
```shell
# Use context to target remote Docker host
docker context use production

# Deploy on remote Docker host
docker-compose --project-directory . \
-f deploy/docker-compose.base.yml \
-f deploy/docker-compose.prod.yml \
up -d --build    
 
```

