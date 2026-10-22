from pathlib import Path
from docx import Document
from core.registry import converter

@converter(".txt", ".docx")
def txt_to_docx(source: Path, output_dir: Path) -> Path:
    target = output_dir / f"{source.stem}.docx"
    doc = Document()
    with open(source, mode="r", encoding="utf-8") as f:
        for line in f:
            doc.add_paragraph(line.rstrip("\n"))
    doc.save(target)
    return target