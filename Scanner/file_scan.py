from pathlib import Path
import hashlib
from datetime import datetime

ALLOWED_BASES = [
    Path("./scan_data").resolve(),
    Path(".").resolve()  # katalog projektu
]

PATTERNS = [b"PRIVATE KEY", b"password", b"api_key"]
MAX_FILES = 200
MAX_SIZE = 5 * 1024 * 1024  # 5 MB

def now():
    return datetime.utcnow().isoformat() + "Z"

def is_allowed_path(folder: Path):
    folder = folder.resolve()
    return any(base in folder.parents or folder == base for base in ALLOWED_BASES)

def hash_file(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def file_scan(folder):
    folder = Path(folder).resolve()

    if not folder.exists() or not folder.is_dir():
        return {"error": "Katalog nie istnieje"}

    if not is_allowed_path(folder):
        return {"error": "Brak uprawnień do skanowania tej ścieżki"}

    files = []

    for i, f in enumerate(folder.rglob("*")):
        if i >= MAX_FILES:
            break

        if f.is_file() and f.stat().st_size <= MAX_SIZE:
            try:
                content = f.read_bytes()[:4000]
            except Exception:
                continue

            suspicious = [p.decode() for p in PATTERNS if p in content]

            files.append({
                "file": str(f.relative_to(folder)),
                "sha256": hash_file(f),
                "suspicious": suspicious
            })

    return {
        "timestamp": now(),
        "path": str(folder),
        "files_scanned": len(files),
        "files": files
    }
