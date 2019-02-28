#!/usr/bin/env sh

set -eu
unset CDPATH
cd "$( dirname "$0" )/.."

main() {
	log "INFO: Running tests ..."
    pytest
    # rm -f tests/running_pytest
    # log "INFO: Reporting coverage ..."
    
    # local COVERAGE_ARGS="--skip-covered --omit=reaper/eeg_reaper_gui.py"
    # coverage report --show-missing $COVERAGE_ARGS
    # coverage html $COVERAGE_ARGS

    log "INFO: Running pylint ..."
    pylint --rcfile tests/.pylintrc vacation_manager
    log "INFO: Running pycodestyle ..."
    pycodestyle --max-line-length=150 --ignore=E402 vacation_manager
}

log() {
    printf "\n%s\n" "$@" >&2
}


main "$@"
