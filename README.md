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
### DevOps
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

## GitHub Actions Workflows
### Continuous Deployment
- Workflow: `./github/workflows/deploy.yml`
- Automate Dockerized application deployment on the `main` branch push 
- Steps
  1. Set up environment variables, SSH credentials
  2. Create a Docker context for remote Docker host on the AWS EC2 instance
  3. Start containers using Docker Compose
  4. Followed by a post-deployment health check (in a seperate job)


### Server Health Check
- Workflow: `./github/workflows/health.yml`
- Perform regular health checks on a live production server
- Run hourly and on specific workflow completion
- Or can manually run the workflow
- Steps
  1. Send a GET request to the API endpoint `/health`
  2. Evaluate the HTTP response code

### Restarting a Production Server
- Workflow: `./github/workflows/restart.yml`
- Manually run the workflow to restart remote docker containers
- Can optionally clean up volumes attached to containers
