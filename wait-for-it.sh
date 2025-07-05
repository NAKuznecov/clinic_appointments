#!/bin/bash
set -e

host=$1
port=${2:-5432}
shift 2

until nc -z "$host" "$port"; do
  echo "Waiting for Postgres at ${host}:${port}"
  sleep 1
done

echo "Postgres is available!"
exec "$@"