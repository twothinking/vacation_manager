#!/usr/bin/env sh

set -eu
unset CDPATH
cd "$( dirname "$0" )/.."

main() {

	local REAPER_IMAGE=

	 while [ $# -gt 0 ]; do
        case "$1" in
            -B|--no-build)
                REAPER_IMAGE="aeao93/vacation_manager:testing";;
            --)
                shift; break;;
            *)
                break;;
        esac
        shift
    done

    if [ -z "${REAPER_IMAGE}" ]; then
        log "INFO: Building aeao93/vacation_manager:testing image ..."
        docker build -t aeao93/vacation_manager:testing .
    else
        docker tag "$REAPER_IMAGE" aeao93/vacation_manager:testing
    fi

    log "INFO: Starting test container"
    docker run --rm -it aeao93/vacation_manager:testing tests/tests.sh
}

log() {
    printf "\n%s\n" "$@" >&2
}

main "$@"
