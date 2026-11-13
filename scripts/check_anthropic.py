"""Free check that the Anthropic key works: looks up model info (no tokens, no cost).

    scripts/with_key.sh .venv/bin/python scripts/check_anthropic.py [model ...]

Prints only model ids and errors' type/status, never the key.
"""
import sys

import anthropic

models = sys.argv[1:] or ["claude-sonnet-5-5", "claude-opus-5-5"]
client = anthropic.Anthropic()
ok = True
for m in models:
    try:
        info = client.models.retrieve(m)
        print(f"ok    {info.id}  ({info.display_name})")
    except anthropic.APIStatusError as e:
        ok = False
        print(f"fail  {m}: {type(e).__name__} (HTTP {e.status_code})")
    except anthropic.APIConnectionError as e:
        ok = False
        print(f"fail  {m}: could not reach the API ({type(e).__name__})")
sys.exit(0 if ok else 1)
