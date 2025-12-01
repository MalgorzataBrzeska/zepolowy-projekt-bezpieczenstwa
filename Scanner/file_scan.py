from pathlib import Path
import hashlib
from datetime import datetime

PATTERNS = [b"PRIVATE KEY", b"password", b"api_key"]

def now():
    return datetime.utcnow().isoformat() + "Z"

def hash_file(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        h.update(f.read())
    return h.hexdigest()

def file_scan(folder):
    folder = Path(folder)
    files = []

    for f in folder.rglob("*"):
        if f.is_file():
            entry = {
                "path": str(f),
                "sha256": hash_file(f),
            }
            content = f.read_bytes()[:4000]
            entry["suspicious"] = [p.decode() for p in PATTERNS if p in content]
            files.append(entry)

    return {
        "timestamp": now(),
        "path": str(folder),
        "files": files,
    }