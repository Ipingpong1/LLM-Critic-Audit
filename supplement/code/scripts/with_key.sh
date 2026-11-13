#!/bin/sh
# Run one command with ANTHROPIC_API_KEY loaded from the macOS Keychain.
# The key lives only in that command's environment: it is never printed or written to a file.
#   scripts/with_key.sh .venv/bin/python pilot/run.py --backend anthropic ...
# Keychain entry (created by the user): security add-generic-password -U -a "$USER" -s anthropic-api-key -w
if [ -n "${ANTHROPIC_API_KEY:-}" ]; then
  export ANTHROPIC_API_KEY
  exec "$@"
fi
command -v security >/dev/null 2>&1 || {
  echo "Set ANTHROPIC_API_KEY in the environment (Keychain fallback requires macOS)." >&2
  exit 1
}
ANTHROPIC_API_KEY="$(security find-generic-password -a "$USER" -s "${ANTHROPIC_KEYCHAIN_SERVICE:-anthropic-api-key}" -w 2>/dev/null)" || {
  echo "with_key.sh: no Keychain entry 'anthropic-api-key' for $USER" >&2
  exit 1
}
export ANTHROPIC_API_KEY
exec "$@"
