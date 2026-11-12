from pathlib import Path
from docx import Document
from core.registry import converter
import subprocess
import shutil


def _convert_with_libreoffice(source: Path, output_dir: Path, convert_to: str, filter_name: str = None) -> Path:
    libreoffice_cmd = shutil.which("libreoffice") or shutil.which("soffice")
    if not libreoffice_cmd:
        raise RuntimeError("Brak narzędzia LibreOffice. Zainstaluj libreoffice lub soffice.")

    if filter_name:
        command = [
            libreoffice_cmd,
            "--headless",
            "--convert-to",
            f"{convert_to}:{filter_name}",
            "--outdir",
            str(output_dir),
            str(source)
        ]
    else:
        command = [
            libreoffice_cmd,
            "--headless",
            "--convert-to",
            convert_to,
            "--outdir",
            str(output_dir),
            str(source)
        ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        raise RuntimeError("Konwersja przekroczyła limit czasu.")

    if result.returncode != 0:
        raise RuntimeError(f"Konwersja nie powiodła się (kod {result.returncode}): {result.stderr.strip() or result.stdout.strip()}")

    target = output_dir / f"{source.stem}.{convert_to}"
    if not target.exists():
        raise RuntimeError("Narzędzie nie utworzyło oczekiwanego pliku")
    return target


@converter(".txt", ".docx")
def txt_to_docx(source: Path, output_dir: Path) -> Path:
    target = output_dir / f"{source.stem}.docx"
    doc = Document()
    with open(source, mode="r", encoding="utf-8") as f:
        for line in f:
            doc.add_paragraph(line.rstrip("\n"))
    doc.save(target)
    return target


@converter(".docx", ".pdf")
def docx_to_pdf(source: Path, output_dir: Path) -> Path:
    return _convert_with_libreoffice(source, output_dir, "pdf")


@converter(".docx", ".txt")
def docx_to_txt(source: Path, output_dir: Path) -> Path:
    target = output_dir / f"{source.stem}.txt"
    doc = Document(source)
    with open(target, mode="w", encoding="utf-8") as f:
        for para in doc.paragraphs:
            f.write(para.text + "\n")
    return target


@converter(".odt", ".pdf")
def odt_to_pdf(source: Path, output_dir: Path) -> Path:
    return _convert_with_libreoffice(source, output_dir, "pdf")


@converter(".odt", ".txt")
def odt_to_txt(source: Path, output_dir: Path) -> Path:
    return _convert_with_libreoffice(source, output_dir, "txt", "Text")
