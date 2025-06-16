#!/bin/bash -x
source scripts/common.sh
if [ "${INCREMENT}" == "major" ]; then
	NEW_VERSION=$(${SEMVER} -i ${INCREMENT} ${OLD_VERSION})
elif [ "${INCREMENT}" == "minor" ]; then
	NEW_VERSION=$(${SEMVER} -i ${INCREMENT} ${OLD_VERSION})
else
	NEW_VERSION=$(${SEMVER} -i ${OLD_VERSION})
	INCREMENT="default"
fi
echo -e "Version: ${OLD_VERSION} will undergo ${INCREMENT} increment to ${NEW_VERSION}"
echo ${NEW_VERSION} > ${RUN_DIR}/VERSION
git add ${RUN_DIR}/VERSION
git tag -a ${NEW_VERSION}  -m "${COMMIT_MESSAGE}"
