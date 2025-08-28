# Usage
```sh
docker run --rm -it -p YOUR_PORT:80 ghcr.io/Atomic-IT/DataManager-Python-Tools
```

API Documentation URL:
- http://YOUR_IP:YOUR_PORT/docs

# Local build

## Build Docker
```sh
docker build -t dm-tools -f Dockerfile
```

## Run locally built image
```sh
docker run -p 1080:80 -it --rm dm-tools
```
