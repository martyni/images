ORIGINAL_DIR=$(pwd)
ROOT_PROJECT_DIR=$(git rev-parse --show-toplevel)
OUTPUT_FILE=/tmp/output

cd $ROOT_PROJECT_DIR
source $(git rev-parse --show-toplevel)/scripts/common.sh

echo ${YELLOW}Running tests from  ${RUN_DIR}${NO_COLOUR}

python_test () {
  CURRENT_TEST=Python
  echo ${YELLOW} Starting Python Test ${NO_COLOUR}
  pytest
}

linting_test () {
  CURRENT_TEST=Linting
  echo ${YELLOW} Starting Linting Test ${NO_COLOUR}
  pylint $(git ls-files '*.py')
}

build_test () {
  CURRENT_TEST=Build
  echo ${YELLOW} Starting Build Test ${NO_COLOUR} in $(pwd)
  ${RUN_DIR}/build.sh
}

run_test () {
  CURRENT_TEST=Run
  echo ${YELLOW} Starting Run Test ${NO_COLOUR}
  ${RUN_DIR}/run.sh &> $OUTPUT_FILE 
  (grep hi ${OUTPUT_FILE} && echo ${GREEN}Success${NO_COLOUR=} ) || (echo ${RED}Fail${NO_COLOUR} && exit 1)
}

all_tests_pass () {
  echo ${GREEN} All tests passed ${NO_COLOUR}
  cd $ORIGINAL_DIR
  exit 0
}

test_failed () {
  echo ${RED} ${CURRENT_TEST} test failed ${NO_COLOUR}
  cd $ORIGINAL_DIR
  exit 1
}

python_test && linting_test && build_test && run_test  && all_tests_pass || test_failed
