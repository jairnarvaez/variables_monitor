#!/bin/bash

command -v cloc >/dev/null 2>&1 || { echo "Necesitas instalar cloc (sudo pacman -S cloc)"; exit 1; }
command -v jq >/dev/null 2>&1 || { echo "Necesitas instalar jq (sudo pacman -S jq)"; exit 1; }

cloc --json . | jq -r '
  . as $root
  | . as $langs
  | del(.header, .SUM)
  | to_entries[]
  | [.key, (.value.code), ((.value.code / $root.SUM.code) * 100)]
  | @tsv
' | sort -k3 -nr | awk -F'\t' '{printf "%-15s %8d lines  %6.2f%%\n", $1, $2, $3}'
