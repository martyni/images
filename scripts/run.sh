#!/bin/bash -x
RUN_DIR=$(dirname $0)
DOCKER_FLAGS=$(cat ${RUN_DIR}/DOCKER_FLAGS)
NAME=$(cat ${RUN_DIR}/NAME)
VERSION=$(cat ${RUN_DIR}/VERSION)
docker run ${DOCKER_FLAGS} ${NAME}:${VERSION} 
