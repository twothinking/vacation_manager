#!/usr/bin/env sh

set -eu
unset CDPATH
cd "$( dirname "$0" )/../.."

main() {
    log "INFO: Building aeao93/vacation_manager:testing image ..."
    pylint --rcfile web/tests/.pylintrc web
}

log() {
    printf "\n%s\n" "$@" >&2
}


main "$@"
