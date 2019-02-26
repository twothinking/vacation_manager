#!/usr/bin/env sh

set -eu
unset CDPATH
cd "$( dirname "$0" )/../.."

main() {
	log "INFO: Building aeao93/vacation_manager:testing image ..."
	docker build -t aeao93/vacation_manager:testing .
	
    log "INFO: Starting test container"
    docker run --rm -it aeao93/vacation_manager:testing web/tests/test.sh
}

log() {
    printf "\n%s\n" "$@" >&2
}

main "$@"
