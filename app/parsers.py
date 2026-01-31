from __future__ import annotations

import mimetypes
from pathlib import Path
from zipfile import ZipFile


PDF_SIGNATURE = b"%PDF-"
ZIP_SIGNATURE = b"PK\x03\x04"


def detect_type(path: str, mime: str | None = None) -> str:
    """Detect file type by mime, signature, and extension."""
    guessed_mime, _ = mimetypes.guess_type(path)
    mime_value = mime or guessed_mime or ""

    if mime_value in {"application/pdf"}:
        return "pdf"
    if mime_value in {
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }:
        return "docx"
    if mime_value in {"text/plain", "text/markdown"}:
        return "text"
    if mime_value in {"text/csv", "application/vnd.ms-excel"}:
        return "tabular"
    if mime_value in {
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }:
        return "tabular"

    signature = _read_signature(path)
    if signature.startswith(PDF_SIGNATURE):
        return "pdf"
    if signature.startswith(ZIP_SIGNATURE):
        zip_type = _detect_zip_type(path)
        if zip_type:
            return zip_type

    ext = Path(path).suffix.lower()
    if ext == ".pdf":
        return "pdf"
    if ext == ".docx":
        return "docx"
    if ext in {".txt", ".md"}:
        return "text"
    if ext in {".xlsx", ".csv"}:
        return "tabular"
    return "unknown"


def extract_text(path: str, ftype: str) -> str:
    if ftype == "pdf":
        return extract_pdf(path)
    if ftype == "docx":
        return extract_docx(path)
    if ftype == "text":
        return Path(path).read_text(encoding="utf-8", errors="ignore")
    if ftype == "tabular":
        return extract_table(path)
    raise ValueError(f"Unsupported type: {ftype}")


def extract_pdf(path: str) -> str:
    import fitz

    doc = fitz.open(path)
    return "\n".join(page.get_text("text") for page in doc)


def extract_docx(path: str) -> str:
    from docx import Document

    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)


def extract_table(path: str) -> str:
    import pandas as pd

    p = Path(path)
    if p.suffix.lower() == ".csv":
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path)

    head = df.head(50).to_markdown(index=False)
    stats = df.describe(include="all").to_markdown()
    return f"[HEAD]\n{head}\n\n[STATS]\n{stats}"


def _read_signature(path: str, max_bytes: int = 8) -> bytes:
    with open(path, "rb") as handle:
        return handle.read(max_bytes)


def _detect_zip_type(path: str) -> str | None:
    with ZipFile(path) as zip_file:
        names = {name.lower() for name in zip_file.namelist()}
    if any(name.startswith("word/") for name in names):
        return "docx"
    if any(name.startswith("xl/") for name in names):
        return "tabular"
    return None
