from __future__ import annotations

import os

from openai import OpenAI


DEFAULT_MODEL = "gpt-4.1-mini"


def chunk_text(text: str, max_chars: int = 12_000) -> list[str]:
    chunks: list[str] = []
    buffer: list[str] = []
    size = 0

    for paragraph in text.split("\n"):
        paragraph_size = len(paragraph)
        if size + paragraph_size + 1 > max_chars and buffer:
            chunks.append("\n".join(buffer))
            buffer = [paragraph]
            size = paragraph_size
        else:
            buffer.append(paragraph)
            size += paragraph_size + 1

    if buffer:
        chunks.append("\n".join(buffer))

    return chunks


def summarize_text(text: str, model: str = DEFAULT_MODEL) -> dict[str, object]:
    client = _build_client()
    chunks = chunk_text(text)

    chunk_summaries: list[str] = []
    for index, chunk in enumerate(chunks, 1):
        response = client.responses.create(
            model=model,
            input=[
                {
                    "role": "system",
                    "content": "You are a precise analyst. Summarize clearly.",
                },
                {
                    "role": "user",
                    "content": (
                        f"Chunk {index}/{len(chunks)}:\n\n{chunk}\n\n"
                        "- Provide: (1) 5 bullets (2) risks (3) action items"
                    ),
                },
            ],
        )
        chunk_summaries.append(response.output_text)

    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "Combine summaries into one executive summary.",
            },
            {
                "role": "user",
                "content": (
                    "Combine the following chunk summaries into:\n"
                    "A) 10-line executive summary\n"
                    "B) key points JSON (title, bullets[], risks[], actions[])\n\n"
                    + "\n\n".join(chunk_summaries)
                ),
            },
        ],
    )

    final_summary = response.output_text
    return {
        "final_summary": final_summary,
        "chunk_summaries": chunk_summaries,
        "model": model,
    }


def _build_client() -> OpenAI:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is required for summarization.")
    return OpenAI()
