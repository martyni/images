GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NO_COLOUR='\033[0m'
CURRENT_TEST=None
RUN_DIR=$(dirname $0)

if [ ${RUN_DIR} == '.' ]
  then
    RUN_DIR=$(pwd)
fi
