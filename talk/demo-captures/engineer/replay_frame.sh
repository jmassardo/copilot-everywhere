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
    FAILED*|*AssertionError*)
      printf '\033[1;31m%s\033[0m\n' "$line"
      ;;
    *confirmed*|*passed*|*'All checks passed!'*)
      printf '\033[1;32m%s\033[0m\n' "$line"
      ;;
    *)
      printf '%s\n' "$line"
      ;;
  esac
done < "$1"

printf '\n\033[90mRecorded rehearsal • %s persona\033[0m\n' "${3:-Engineer}"
