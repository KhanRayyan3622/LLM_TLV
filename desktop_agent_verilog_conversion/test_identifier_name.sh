#!/bin/sh
# Exit status encodes violated rules (bitwise OR):
#  bit 0 (1): Rule 1 violated — only lowercase a-z, digits 0-9, and underscores allowed
#  bit 1 (2): Rule 2 violated — tokens (sep by '_') must be [a-z]+[0-9]* with no empty tokens
#  bit 2 (4): Rule 3 violated — first token must begin with at least two letters
# No output is produced; use the exit code.
#
# Usage: test_identifier_name.sh <identifier-name>

name=$1
status=0

# Rule 1: lower-case ASCII word chars only (^[a-z0-9_]+$)
if ! printf '%s\n' "$name" | sed -n '/^[a-z0-9_]\{1,\}$/ {q 0}; q 1'; then
  status=$((status | 1))
fi

# Rule 2: tokens are [a-z]+[0-9]* joined by single '_' (no empty tokens)
if ! printf '%s\n' "$name" | sed -n '/^[a-z]\{1,\}[0-9]*\(_[a-z]\{1,\}[0-9]*\)*$/ {q 0}; q 1'; then
  status=$((status | 2))
fi

# Rule 3: name must begin with >=2 letters
if ! printf '%s\n' "$name" | sed -n '/^[a-z]\{2\}/ {q 0}; q 1'; then
  status=$((status | 4))
fi

exit "$status"
