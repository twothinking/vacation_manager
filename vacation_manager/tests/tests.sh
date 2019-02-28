#!/usr/bin/env sh

set -eu
unset CDPATH
cd "$( dirname "$0" )/.."

main() {
	log "INFO: Running tests ..."
    coverage run -m pytest
    log "INFO: Coverage"
    coverage report
    log "INFO: Running pylint ..."
    pylint --rcfile tests/.pylintrc vacation_manager
    log "INFO: Running pycodestyle ..."
    pycodestyle --max-line-length=150 --ignore=E402 vacation_manager
}

log() {
    printf "\n%s\n" "$@" >&2
}


main "$@"
