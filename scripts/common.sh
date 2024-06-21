if [[ -z $(which unbuffer) ]]; then
    echo Running in a pipeline and don\'t set Colour text variables
    PIPELINE=1
else
    echo Running locally setting Colour Variables
    GREEN='\033[0;32m'
    RED='\033[0;31m'
    YELLOW='\033[0;33m'
    NO_COLOUR='\033[0m'
fi
CURRENT_TEST=None
RUN_DIR=$(dirname $0)
