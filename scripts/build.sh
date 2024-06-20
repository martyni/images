source $(git rev-parse --show-toplevel)/scripts/common.sh

NAME=$(cat ${RUN_DIR}/NAME)
VERSION=$(cat ${RUN_DIR}/VERSION)
BUILD_EXIT_FILE=/tmp/build_exit_code
BUILD_OUTPUT=/tmp/build_output_${VERSION}

#Retain colour in docker build and capture exit status
unbuffer docker build -t $NAME:$VERSION . 2>&1 | tee $BUILD_OUTPUT && awk -F 'exit code: ' '/exit code/{print $2}' $BUILD_OUTPUT > $BUILD_EXIT_FILE || exit 1

echo docker run $NAME:$VERSION
echo -n exiting $(cat ${BUILD_EXIT_FILE})
exit $(cat $BUILD_EXIT_FILE && rm $BUILD_EXIT_FILE)
