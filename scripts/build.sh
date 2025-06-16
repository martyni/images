#!/bin/bash -x
source scripts/common.sh

if [[ ${PIPELINE} ]]; then
   #Capture docker exit status or fail with status 1 if build fails
   docker build -t ${NAME}:${VERSION} . 2>&1 | tee ${BUILD_OUTPUT} && awk -F 'exit code: ' '/exit code/{print $2}' ${BUILD_OUTPUT} > ${BUILD_EXIT_FILE} || exit 1
else
   #Retain colour in docker build and capture exit status or fail with status 1 if build fails
   unbuffer docker build -t ${NAME}:${VERSION} . 2>&1 | tee ${BUILD_OUTPUT} && awk -F 'exit code: ' '/exit code/{print $2}' ${BUILD_OUTPUT} > ${BUILD_EXIT_FILE} || exit 1
fi

echo -e ${COMMAND}
echo exiting $(cat ${BUILD_EXIT_FILE})




/bin/cat <<EOM > ${RUN_DIR}/${NAME}.service
[Unit]
Description=${DESCRIPTION}
After=network.target
StartLimitIntervalSec=0
[Service]
Type=simple
Restart=always
RestartSec=1
User=${USER}
ExecStart=authbind $(which gunicorn) --certfile=/tmp/$DOMAIN.crt --keyfile=/tmp/$DOMAIN.key --bind 0.0.0.0:443 ${NAME}.app:app
[Install]
WantedBy=multi-user.target
EOM
exit $(cat ${BUILD_EXIT_FILE})
