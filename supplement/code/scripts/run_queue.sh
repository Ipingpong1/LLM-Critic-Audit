#!/bin/bash
# Run pilot jobs one after another against a local Ollama server, inside a time window
# (e.g. overnight on the Mac). Run from anywhere:
#
#   DEADLINE="2026-11-03 07:40" HARD_STOP="2026-11-03 07:50" scripts/run_queue.sh scripts/overnight_batch1.txt
#
# Each job line: <estimated minutes> <ollama model> <label> <conditions>; blank lines and # comments are skipped.
# A job is skipped if its estimate would run past DEADLINE, and a job still running at HARD_STOP is
# stopped. Runs are resumable, so rerunning a job later picks up where it left off. Results go to
# results/pilot/<label>.jsonl, so new conditions join the model's existing file.
set -u
cd "$(dirname "$0")/.."
to_epoch() { date -j -f "%Y-%m-%d %H:%M" "$1" +%s; }
deadline=$(to_epoch "${DEADLINE:?set DEADLINE, e.g. 2026-11-03 07:40}")
hard_stop=$(to_epoch "${HARD_STOP:-$DEADLINE}")
EXTRA_BODY=${EXTRA_BODY:-'{"reasoning_effort": "none"}'}

grep -vE '^[[:space:]]*(#|$)' "$1" | while read -r est model label conds; do
  if (( $(date +%s) + est * 60 > deadline )); then
    echo "$(date +%H:%M) skip  $label $conds (needs ~$est min)"
    continue
  fi
  echo "$(date +%H:%M) start $label $conds"
  .venv/bin/python -m pilot.run --model "$model" --label "$label" --conditions "$conds" \
    --extra-body "$EXTRA_BODY" --logprobs --log-every 200 \
    --out "results/pilot/${label//[^A-Za-z0-9._-]/_}.jsonl" < /dev/null &
  pid=$!
  while kill -0 "$pid" 2>/dev/null; do
    if (( $(date +%s) > hard_stop )); then
      echo "$(date +%H:%M) hard stop: $label"
      kill "$pid"
    fi
    sleep 15
  done
  wait "$pid"
  echo "$(date +%H:%M) end   $label (exit $?)"
done
