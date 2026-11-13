import contextlib
import csv
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from check_audit import archive
from label_sensitivity import read_key


class ReceiptTests(unittest.TestCase):
    def test_snapshot_preserves_bytes_and_refuses_overwrite(self):
        key, sheet = read_key()
        with tempfile.TemporaryDirectory() as td:
            src, dest = Path(td) / 'synthetic.csv', Path(td) / 'snapshot'
            with src.open('w', newline='') as f:
                w = csv.DictWriter(f, fieldnames=['sheet_id','audit_id','auditor','verdict','step','note'])
                w.writeheader()
                for k in key:
                    w.writerow(dict(sheet_id=sheet, audit_id=k['audit_id'], auditor='SYNTHETIC_TEST_ONLY',
                                    verdict='unsure', step='', note='Synthetic, not a real judgment.\n"Quoted" note.'))
            with contextlib.redirect_stdout(io.StringIO()):
                result = archive(src, dest, 'ai-assisted', 'SYNTHETIC TEST DATA ONLY')
            self.assertEqual((dest / 'responses.csv').read_bytes(), src.read_bytes())
            self.assertEqual(result['response_sha256'], hashlib.sha256(src.read_bytes()).hexdigest())
            self.assertEqual(result['counts'], {'unsure':42})
            self.assertEqual(json.loads((dest / 'receipt.json').read_text())['review_mode_declared'], 'ai-assisted')
            with self.assertRaises(FileExistsError):
                archive(src, dest, 'ai-assisted', 'SYNTHETIC TEST DATA ONLY')
