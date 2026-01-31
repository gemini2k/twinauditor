from __future__ import annotations

import uuid

from app.parsers import detect_type, extract_text
from app.repository import InMemoryRepository
from app.summarizer import summarize_text
from app.models import SummaryRecord


def enqueue_processing(file_id: str, path: str, mime: str | None = None) -> None:
    """Placeholder for enqueuing background processing."""
    _ = file_id, path, mime


def process_file(
    repository: InMemoryRepository,
    file_id: str,
    path: str,
    mime: str | None = None,
) -> dict[str, object]:
    ftype = detect_type(path, mime)
    text = extract_text(path, ftype)
    summary_result = summarize_text(text)

    repository.update_file_status(file_id, "PROCESSED")
    summary = SummaryRecord(
        id=str(uuid.uuid4()),
        file_id=file_id,
        summary_text=summary_result["final_summary"],
        key_points={"chunks": summary_result["chunk_summaries"]},
        model=str(summary_result["model"]),
    )
    repository.add_summary(summary)

    return {
        "file_id": file_id,
        "type": ftype,
        "summary": summary.summary_text,
    }
