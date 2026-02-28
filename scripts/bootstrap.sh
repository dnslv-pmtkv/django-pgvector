#!/bin/bash
set -e

POSTGRES_USERNAME="djpgv"
DATABASE_NAME="djpgv"

usage() {
  cat <<EOF
Usage: $(basename "$0") [options]

Options:
  -u USERNAME   Postgres username (default: djpgv)
  -d DATABASE   Database name (default: djpgv)
  -h            Show this help message
EOF
}

while getopts ":u:d:h" opt; do
  case "$opt" in
  u)
    POSTGRES_USERNAME="$OPTARG"
    ;;
  d)
    DATABASE_NAME="$OPTARG"
    ;;
  h)
    usage
    exit 0
    ;;
  \?)
    echo "Invalid option: -$OPTARG" >&2
    usage
    exit 1
    ;;
  :)
    echo "Option -$OPTARG requires an argument." >&2
    usage
    exit 1
    ;;
  esac
done

echo "Using postgres user: $POSTGRES_USERNAME"
echo "Using database name: $DATABASE_NAME"

dropdb --if-exists "$DATABASE_NAME"
createdb -O "$POSTGRES_USERNAME" "$DATABASE_NAME"

python manage.py migrate
