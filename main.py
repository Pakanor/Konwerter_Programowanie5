from pathlib import Path
from core.registry import ConversionRequest, execute, available_targets
import converters


def main():
    samples_dir = Path("data_sample")
    out_dir = Path("output")
    out_dir.mkdir(exist_ok=True)

    print("=== TEST WSZYSTKICH KIERUNKÓW KONWERSJI ===\n")

    print("[GRUPA A] Dane strukturalne")
    csv_path = samples_dir / "test.csv"
    print(f"Dostępne cele dla {csv_path.name}: {available_targets(csv_path)}")
    try:
        req = ConversionRequest(csv_path, ".json", out_dir)
        res = execute(req)
        print(f"[SUKCES] Konwersja CSV -> JSON: {res}")
    except Exception as e:
        print(f"[BŁĄD] CSV -> JSON: {e}")

    try:
        json_path = out_dir / "test.json"
        req = ConversionRequest(json_path, ".csv", out_dir)
        res = execute(req)
        print(f"[SUKCES] Konwersja JSON -> CSV: {res}")
    except Exception as e:
        print(f"[BŁĄD] JSON -> CSV: {e}")
    print()

    print("[GRUPA B] Tekst i dokumenty")
    txt_path = samples_dir / "test.txt"
    print(f"Dostępne cele dla {txt_path.name}: {available_targets(txt_path)}")
    try:
        req = ConversionRequest(txt_path, ".docx", out_dir)
        res = execute(req)
        print(f"[SUKCES] Konwersja TXT -> DOCX: {res}")
    except Exception as e:
        print(f"[BŁĄD] TXT -> DOCX: {e}")

    try:
        docx_path = out_dir / "test.docx"
        if docx_path.exists():
            print(f"Dostępne cele dla {docx_path.name}: {available_targets(docx_path)}")
            for target in [".pdf", ".txt"]:
                try:
                    req = ConversionRequest(docx_path, target, out_dir)
                    res = execute(req)
                    print(f"[SUKCES] Konwersja DOCX -> {target}: {res}")
                except Exception as e:
                    print(f"[BŁĄD] DOCX -> {target}: {e}")
        else:
            print("[INFO] Brak pliku test.docx do dalszych konwersji z DOCX")
    except Exception as e:
        print(f"[BŁĄD] {e}")
    print()

    print("[GRUPA C] Formaty biurowe (ODT/PDF)")
    try:
        odt_path = out_dir / "test.odt"
        if not odt_path.exists():
            docx_path = out_dir / "test.docx"
            if docx_path.exists():
                try:
                    import subprocess
                    import shutil
                    libreoffice_cmd = shutil.which("libreoffice") or shutil.which("soffice")
                    if libreoffice_cmd:
                        cmd = [libreoffice_cmd, "--headless", "--convert-to", "odt", "--outdir", str(out_dir), str(docx_path)]
                        subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                        print("[INFO] Utworzono test.odt z test.docx")
                except Exception as e:
                    print(f"[INFO] Nie udało się utworzyć test.odt: {e}")
        
        if odt_path.exists():
            print(f"Dostępne cele dla {odt_path.name}: {available_targets(odt_path)}")
            for target in [".pdf", ".txt"]:
                try:
                    req = ConversionRequest(odt_path, target, out_dir)
                    res = execute(req)
                    print(f"[SUKCES] Konwersja ODT -> {target}: {res}")
                except Exception as e:
                    print(f"[BŁĄD] ODT -> {target}: {e}")
        else:
            print("[INFO] Brak pliku test.odt - pomijam konwersje ODT")
    except Exception as e:
        print(f"[BŁĄD] {e}")
    print()

    # Testy błędów
    print("[TESTY BŁĘDÓW]")
    try:
        print("Testowanie kontrolowanego błędu dla uszkodzonego pliku JSON:")
        invalid_path = samples_dir / "invalid.json"
        req = ConversionRequest(invalid_path, ".csv", out_dir)
        execute(req)
    except Exception as e:
        print(f"[PRZECHWYCZONO OCZEKIWANY BŁĄD]: {e}")

    print("\n=== ZAKOŃCZONO WSZYSTKIE TESTY ===")


if __name__ == "__main__":
    main()
