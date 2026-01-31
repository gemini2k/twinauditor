# twinauditor

Minimal reference implementation for the upload → queue → worker summarization pipeline.

## Modules

- `app/main.py`: FastAPI upload API. Saves files, records metadata, and enqueues jobs.
- `app/parsers.py`: File type detection and text extraction.
- `app/summarizer.py`: Chunked map-reduce summarization using the Responses API.
- `app/tasks.py`: Worker pipeline that ties parsing, summarization, and persistence.
- `app/repository.py`: In-memory repository placeholder for DB integration.

## Notes

Replace `enqueue_processing` with Celery/RQ/Arq integration and swap the in-memory repository
with your persistent database layer.
