from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class UploadRecord:
    id: str
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(slots=True)
class FileRecord:
    id: str
    upload_id: str
    filename: str
    mime: str | None
    sha256: str
    storage_uri: str
    status: str = "PENDING"


@dataclass(slots=True)
class SummaryRecord:
    id: str
    file_id: str
    summary_text: str
    key_points: dict[str, Any]
    model: str
    created_at: datetime = field(default_factory=datetime.utcnow)
