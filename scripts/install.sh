#!/bin/bash -x
source scripts/common.sh
sudo cp ${RUN_DIR}/${NAME}.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ${NAME}
sudo systemctl restart ${NAME}
