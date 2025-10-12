#!/bin/bash

IMAGE_NAME="innpulse360-api"
CONTAINER_NAME="innpulse360-container"

echo "Limpiando contenedores e imagenes anteriores..."
if [ $(docker ps -q -f name=$CONTAINER_NAME) ]; then
    docker stop $CONTAINER_NAME
fi
if [ $(docker ps -aq -f status=exited -f name=$CONTAINER_NAME) ]; then
    docker rm $CONTAINER_NAME
fi
if [ $(docker images -q $IMAGE_NAME) ]; then
    docker rmi $IMAGE_NAME
fi

docker build -t $IMAGE_NAME .
echo "Iniciando contenedor..."
docker run -d --name $CONTAINER_NAME -p 8000:8000 $IMAGE_NAME
docker logs --follow $CONTAINER_NAME


