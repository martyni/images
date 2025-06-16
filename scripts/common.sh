if [[ -z $(which unbuffer) ]]; then
    echo Running in a pipeline Colour not set
    PIPELINE=1
else
    echo Running locally setting Colour Variables
    GREEN='\033[0;32m'
    RED='\033[0;31m'
    YELLOW='\033[0;33m'
    NO_COLOUR='\033[0m'
fi

RUN_DIR=$(realpath $(dirname $0))
BUILD_EXIT_FILE=/tmp/build_exit_code
BUILD_OUTPUT=/tmp/build_output
DOCKER_FLAGS=$(cat ${RUN_DIR}/DOCKER_FLAGS)
DOCKER_REPO=$(cat ${RUN_DIR}/DOCKER_REPO)
NAME=$(cat ${RUN_DIR}/NAME)
FULL_NAME="${DOCKER_REPO}/$(cat ${RUN_DIR}/NAME)"
VERSION=$(cat ${RUN_DIR}/VERSION)
DESCRIPTION=$(cat ${RUN_DIR}/DESCRIPTION)
DOMAIN=$(cat ${RUN_DIR}/DOMAIN)
COMMAND="docker run ${DOCKER_FLAGS} ${NAME}:${VERSION}"
CONTAINER=$(docker run ${DOCKER_FLAGS} ${DOCKER_REPO}/${NAME}:${VERSION}|| (echo "fail to start container\n" >>${OUTPUT}))
CURRENT_TEST=None
OUT=/tmp/output
OLD_VERSION=$(cat ${RUN_DIR}/VERSION)
INCREMENT=$(git rev-parse --abbrev-ref HEAD | awk -F "/" '{ print $1}')
SEMVER="/usr/bin/semver"
COMMIT_MESSAGE=$(git log -1 --pretty=%B)
