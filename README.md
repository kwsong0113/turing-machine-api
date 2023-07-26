# turing-machine-api

## Poetry

```shell
# Development
poetry install
# Production
poetry install --only main
```

## Docker

### Development

```shell
# Create and start container on local Docker environment
docker-compose --project-directory . \
-f deploy/docker-compose.base.yml \
-f deploy/docker-compose.dev.yml \
up -d --build   
```

### Production
```shell
# Use context to target remote Docker host
docker context use production

# Deploy on remote Docker host
docker-compose --project-directory . \
-f deploy/docker-compose.base.yml \
-f deploy/docker-compose.prod.yml \
up -d --build    
 
```