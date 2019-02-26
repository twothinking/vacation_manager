#!/usr/bin/env sh

set -eu
unset CDPATH
cd "$( dirname "$0" )/.."

main() {
    log "INFO: Lint aeao93/vacation_manager:testing image ..."
    pylint --rcfile tests/.pylintrc vacation_manager
    log "INFO: PyCodeStyle aeao93/vacation_manager:testing image ..."
    pycodestyle --max-line-length=150 --ignore=E402 vacation_manager
}

log() {
    printf "\n%s\n" "$@" >&2
}


main "$@"
