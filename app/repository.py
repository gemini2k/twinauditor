from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from app.models import FileRecord, SummaryRecord, UploadRecord


class InMemoryRepository:
    """Simple in-memory repository to mimic DB interactions."""

    def __init__(self) -> None:
        self.uploads: dict[str, UploadRecord] = {}
        self.files: dict[str, FileRecord] = {}
        self.summaries: dict[str, SummaryRecord] = {}

    def add_upload(self, upload: UploadRecord) -> None:
        self.uploads[upload.id] = upload

    def add_files(self, files: Iterable[FileRecord]) -> None:
        for record in files:
            self.files[record.id] = record

    def update_file_status(self, file_id: str, status: str) -> None:
        record = self.files[file_id]
        self.files[file_id] = FileRecord(
            id=record.id,
            upload_id=record.upload_id,
            filename=record.filename,
            mime=record.mime,
            sha256=record.sha256,
            storage_uri=record.storage_uri,
            status=status,
        )

    def add_summary(self, summary: SummaryRecord) -> None:
        self.summaries[summary.id] = summary

    def list_files_by_upload(self, upload_id: str) -> list[FileRecord]:
        return [record for record in self.files.values() if record.upload_id == upload_id]

    def get_summary(self, summary_id: str) -> SummaryRecord:
        return self.summaries[summary_id]


def build_repository() -> InMemoryRepository:
    return InMemoryRepository()
