#!/usr/bin/env bash

set -euo pipefail

clear
if [[ -n "${2:-}" ]]; then
  printf '\033]0;%s\007' "$2"
fi

while IFS= read -r line || [[ -n "$line" ]]; do
  case "$line" in
    '$ '*)
      printf '\033[1;32m%s\033[0m\n' "$line"
      ;;
    FAILED*|*AssertionError*|*BLOCKED*|*UNRESOLVED*)
      printf '\033[1;31m%s\033[0m\n' "$line"
      ;;
    PASS*|*confirmed*|*passed*|*'All checks passed!'*|*SATISFIED*)
      printf '\033[1;32m%s\033[0m\n' "$line"
      ;;
    *)
      printf '%s\n' "$line"
      ;;
  esac
done < "$1"

printf '\n\033[90mFacilitator fallback • synthetic Orders Service lab\033[0m\n'
