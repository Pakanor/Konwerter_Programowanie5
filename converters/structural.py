import csv
import json
from pathlib import Path
from core.registry import converter

@converter(".csv", ".json")
def csv_to_json(source: Path, output_dir: Path) -> Path:
    target = output_dir / f"{source.stem}.json"
    with open(source, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = list(reader)
    with open(target, mode="w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return target

@converter(".json", ".csv")
def json_to_csv(source: Path, output_dir: Path) -> Path:
    target = output_dir / f"{source.stem}.csv"
    with open(source, mode="r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Błąd składni JSON: {e.msg} (linia {e.lineno})")
            
    if not isinstance(data, list) or not data or not isinstance(data[0], dict):
        raise ValueError("Plik JSON musi zawierać niepustą listę obiektów.")

    headers = list(data[0].keys())
    with open(target, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    return target