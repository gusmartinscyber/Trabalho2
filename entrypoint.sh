#!/bin/sh
set -e

cd /app
mkdir -p /app/data

export INVENTARIO_JSON_PATH="${INVENTARIO_JSON_PATH:-/app/data/inventario.json}"

while true; do
  python -m src.main || true
  sleep 2
done
