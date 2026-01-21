import json
import os

def save_json(data, filename="report.json"):
    os.makedirs("results", exist_ok=True)

    filepath = os.path.join("results", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return filepath
