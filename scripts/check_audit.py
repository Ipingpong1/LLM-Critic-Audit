"""Validate and preserve a completed audit without revealing the selection key."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import label_sensitivity as ls


def archive(source, destination, review_mode, exposure_note):
    source, destination = Path(source), Path(destination)
    key, sheet = ls.read_key()
    reviewer, answers = ls.read_audit(source, key, sheet)
    data = source.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    html = (ls.ROOT / 'audit/audit_sheet.html').read_text()
    payload = re.search(r'<script id="data" type="application/json">(.*?)</script>', html, re.S).group(1)
    receipt = dict(sheet_id=sheet, reviewer=reviewer, judgments=len(answers),
                   counts=dict(Counter(a['verdict'] for a in answers.values())),
                   review_mode_declared=review_mode, exposure_and_tools_declared=exposure_note,
                   independence_not_verified_by_software=True,
                   source_file=source.name, response_sha256=digest,
                   blind_payload_sha256=hashlib.sha256(payload.encode()).hexdigest(),
                   captured_at=datetime.now(timezone.utc).isoformat(),
                   status='Completed first-pass response snapshot; not an adjudicated gold standard')
    destination.mkdir(parents=True, exist_ok=False)
    (destination / 'responses.csv').write_bytes(data)
    (destination / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))
    return receipt


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('responses', type=Path)
    ap.add_argument('--out-dir', type=Path, required=True)
    ap.add_argument('--review-mode', choices=['independent-human', 'ai-assisted', 'adjudicated'], required=True)
    ap.add_argument('--exposure-note', required=True, help='Reviewer declaration: prior label/model exposure and tools used')
    a = ap.parse_args()
    archive(a.responses, a.out_dir, a.review_mode, a.exposure_note)
