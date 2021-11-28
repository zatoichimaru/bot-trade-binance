#!/bin/bash
_is_sourced() {
  # https://unix.stackexchange.com/a/215279
  [ "${#FUNCNAME[@]}" -ge 2 ] &&
    [ "${FUNCNAME[0]}" = '_is_sourced' ] &&
    [ "${FUNCNAME[1]}" = 'source' ]
}

# logging functions
docker_log() {
  local type="$1"
  shift
  printf '%s [%s] [Entrypoint]: %s\n' "$(date -u +\"%Y-%m-%dT%H:%M:%SZ\")" "$type" "$*"
}

docker_note() {
  docker_log Note "$@"
}

# Build application distribution
docker_note "[MAILER-PEDING-REPORTS-SENDING] Starting ${APP_ENV} server..."

if [ "${APP_ENV}" = 'production' ] || [ "${APP_ENV}" = 'staging' ]; then
  cd src
  python3 main.py
elif [ "${APP_ENV}" = 'test' ]; then
  pass
else
  python3 main.py
fi

if ! _is_sourced; then
  # complete params
  exec "$@"
fi