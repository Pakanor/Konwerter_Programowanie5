from pathlib import Path
from core.registry import ConversionRequest, execute, available_targets
import converters  
def main():
    samples_dir = Path("data_sample")
    out_dir = Path("output")
    out_dir.mkdir(exist_ok=True)

    print("=== TESTY LABORATORIUM 2 ===")

    csv_path = samples_dir / "test.csv"
    print(f"Dostępne cele dla {csv_path.name}: {available_targets(csv_path)}")

    try:
        req = ConversionRequest(csv_path, ".json", out_dir)
        res = execute(req)
        print(f"[SUKCES] Konwersja CSV -> JSON: {res}")
    except Exception as e:
        print(f"[BŁĄD] {e}")

    try:
        json_path = out_dir / "test.json"
        req = ConversionRequest(json_path, ".csv", out_dir)
        res = execute(req)
        print(f"[SUKCES] Konwersja JSON -> CSV: {res}")
    except Exception as e:
        print(f"[BŁĄD] {e}")

    try:
        txt_path = samples_dir / "test.txt"
        req = ConversionRequest(txt_path, ".docx", out_dir)
        res = execute(req)
        print(f"[SUKCES] Konwersja TXT -> DOCX: {res}")
    except Exception as e:
        print(f"[BŁĄD] {e}")

    try:
        print("\nTestowanie kontrolowanego błędu dla uszkodzonego pliku JSON:")
        invalid_path = samples_dir / "invalid.json"
        req = ConversionRequest(invalid_path, ".csv", out_dir)
        execute(req)
    except Exception as e:
        print(f"[PRZECHWYCZONO OCZEKIWANY BŁĄD]: {e}")

if __name__ == "__main__":
    main()