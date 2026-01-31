from __future__ import annotations

import hashlib
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, UploadFile

from app.models import FileRecord, UploadRecord
from app.repository import build_repository
from app.tasks import enqueue_processing


app = FastAPI()
repository = build_repository()

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


@app.post("/uploads")
async def create_upload(files: list[UploadFile] = File(...)) -> dict[str, object]:
    upload_id = str(uuid4())
    repository.add_upload(UploadRecord(id=upload_id))

    saved_files: list[FileRecord] = []
    for file in files:
        content = await file.read()
        digest = sha256_bytes(content)
        safe_name = file.filename or "unnamed"
        save_path = UPLOAD_DIR / f"{upload_id}__{digest}__{safe_name}"

        with open(save_path, "wb") as handle:
            handle.write(content)

        file_id = str(uuid4())
        record = FileRecord(
            id=file_id,
            upload_id=upload_id,
            filename=safe_name,
            mime=file.content_type,
            sha256=digest,
            storage_uri=str(save_path),
        )
        saved_files.append(record)

        enqueue_processing(file_id=file_id, path=str(save_path), mime=file.content_type)

    repository.add_files(saved_files)

    return {
        "upload_id": upload_id,
        "files": [
            {
                "file_id": record.id,
                "path": record.storage_uri,
                "filename": record.filename,
                "status": record.status,
            }
            for record in saved_files
        ],
    }
