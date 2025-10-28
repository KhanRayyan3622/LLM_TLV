#!/bin/bash

# This script restores the working directory to the state captured in the given history directory.

# Usage: restore_from_history.sh <history-number>
# Run from a conversion directory containing /history/<history-number>
# E.g., ./scripts/restore_from_history.sh 2

set -euo pipefail

cnt="$1"
if [[ $cnt == "latest" ]]; then
  cnt=$(readlink history/latest)
fi
cnt=$((10#$cnt))  # Force decimal interpretation and remove leading zeros.
padded_cnt=$(printf "%03d" "$cnt")
HISTORY_DIR="history/$padded_cnt"   # Append leading zeros.
if [[ ! -d "$HISTORY_DIR" ]]; then
  echo "ERROR: History directory $HISTORY_DIR not found."
  exit 1
fi

# Checkpoint current *.* in `unsuccessful/` before restoring.
rm -rf unsuccessful
mkdir -p unsuccessful
cp -f ./*.* unsuccessful/ 2>/dev/null || true

# Copy the saved files back to the working directory in a state where rerunning fev.sh
# should produce the same results.
# It is our policy that feved.tlv is read-only.
chmod 600 "$HISTORY_DIR/feved.tlv" 2>/dev/null || true
cp -f "$HISTORY_DIR/feved.tlv" "./feved.tlv"
chmod 400 "./feved.tlv"
cp -f "$HISTORY_DIR/wip.tlv" "./wip.tlv"
cp -f "$HISTORY_DIR/status.json" "./status.json"
shopt -s nullglob
for file in $HISTORY_DIR/fev*.eqy; do
  cp "$file" .
done
shopt -u nullglob

# Remove local files to ensure fresh fev.sh.
rm match_lines.eqy 2>/dev/null || true
rm wip*.sv 2>/dev/null || true
# Update latest link to point to the previous history directory.
if [[ $cnt != "0" ]]; then
  ln -sf "$(printf "%03d" $((cnt - 1)))" "history/latest"
else
  rm -f history/latest 2>/dev/null || true
fi
# Delete history directories after and including the given one.
# Strip leading zeros from history directory number.
while [[ -d history/$padded_cnt ]]; do
  echo "Removing history directory: history/${padded_cnt}"
  rm -rf history/$padded_cnt
  cnt=$((cnt + 1))
  padded_cnt=$(printf "%03d" "$cnt")
done

# Run fev.sh, which *should* pass incremental FEV and create a new history directory, to reproduce the results.
$fev_log=./fev.sh.log
./scripts/fev.sh > $fev_log 2>&1
status=$?
if [[ ! -e "$HISTORY_DIR" ]]; then
  echo
  echo "ERROR: ./scripts/fev.sh failed with status $status and did not recreate $HISTORY_DIR. Log:"
  echo
  cat $fev_log
  exit 1
fi
