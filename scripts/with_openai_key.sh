#!/bin/sh
# Run one command with OPENAI_API_KEY loaded from the macOS Keychain.
# The key lives only in that command's environment: it is never printed or written to a file.
#   scripts/with_openai_key.sh .venv/bin/python -m pilot.run --base-url https://api.openai.com/v1 --api-key-env OPENAI_API_KEY ...
# Keychain entry (created by the user): openai-codex-api-key
if [ -n "${OPENAI_API_KEY:-}" ]; then
  export OPENAI_API_KEY
  exec "$@"
fi
command -v security >/dev/null 2>&1 || {
  echo "Set OPENAI_API_KEY in the environment (Keychain fallback requires macOS)." >&2
  exit 1
}
OPENAI_API_KEY="$(security find-generic-password -a "$USER" -s "${OPENAI_KEYCHAIN_SERVICE:-openai-codex-api-key}" -w 2>/dev/null)" || {
  echo "with_openai_key.sh: no Keychain entry 'openai-codex-api-key' for $USER" >&2
  exit 1
}
export OPENAI_API_KEY
exec "$@"
