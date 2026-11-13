"""Verify or package the saved research replies. Uses only the standard library.

The archive contains only files listed in data/RESPONSE_FILES.sha256 and that
manifest. It excludes credentials, local provenance, logs, and literature caches.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
from pathlib import Path, PurePosixPath
import tarfile
import tempfile


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/RESPONSE_FILES.sha256"


def entries():
    rows = []
    seen = set()
    for line in MANIFEST.read_text().splitlines():
        digest, name = line.split("  ", 1)
        rel = PurePosixPath(name)
        if (len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest)
                or rel.is_absolute() or ".." in rel.parts or name in seen
                or rel.parts[0] not in {"data", "results"}):
            raise ValueError(f"Invalid manifest entry: {name}")
        seen.add(name)
        rows.append((digest, name))
    return rows


def verify(rows):
    failures = []
    total = 0
    for expected, name in rows:
        path = ROOT / name
        if not path.is_file() or path.is_symlink():
            failures.append(f"missing or symlink: {name}")
            continue
        h = hashlib.sha256()
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                h.update(block)
                total += len(block)
        if h.hexdigest() != expected:
            failures.append(f"checksum mismatch: {name}")
    if failures:
        raise SystemExit("Data verification failed:\n" + "\n".join(failures)
                         + "\nRestore the companion archive at the project root.")
    print(f"Verified {len(rows)} files ({total:,} bytes).")


def pack(rows, output):
    if output.exists():
        raise SystemExit(f"Refusing to overwrite {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    names = [name for _, name in rows] + [MANIFEST.relative_to(ROOT).as_posix()]
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=output.parent, prefix=".responses-", delete=False) as raw:
            temporary = Path(raw.name)
            with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
                with tarfile.open(fileobj=compressed, mode="w|", format=tarfile.PAX_FORMAT) as archive:
                    for name in names:
                        path = ROOT / name
                        info = archive.gettarinfo(str(path), arcname=name)
                        info.uid = info.gid = 0
                        info.uname = info.gname = ""
                        info.mtime = 0
                        info.mode = 0o644
                        info.pax_headers = {}
                        with path.open("rb") as source:
                            archive.addfile(info, source)
        temporary.rename(output)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    print(f"Created {output} ({output.stat().st_size:,} bytes).")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("action", choices=["verify", "pack"])
    ap.add_argument("--output", type=Path, default=ROOT / ".local/releases/critic-responses.tar.gz")
    args = ap.parse_args()
    rows = entries()
    verify(rows)
    if args.action == "pack":
        pack(rows, args.output.resolve())


if __name__ == "__main__":
    main()
