from __future__ import annotations

from dataclasses import dataclass, field

from .meeting_notes import summarize_meeting_transcript
from .transcript import chunk_text


@dataclass(frozen=True, slots=True)
class ChunkNote:
    chunk_index: int
    overview: str
    key_points: list[str]
    takeaways: list[str]


@dataclass(slots=True)
class VideoSummary:
    title: str
    chunk_count: int
    overview: str
    key_points: list[str] = field(default_factory=list)
    takeaways: list[str] = field(default_factory=list)

    def to_markdown(self) -> str:
        lines = [f"# Video Summary: {self.title}", "", "## Overview", self.overview, ""]
        lines.append("## Key Points")
        lines.extend(f"- {item}" for item in self.key_points)
        lines.append("")
        lines.append("## Takeaways")
        lines.extend(f"- {item}" for item in (self.takeaways or ["No explicit action items identified."]))
        lines.append("")
        lines.append("## Processing Metadata")
        lines.append(f"- Transcript chunks processed: {self.chunk_count}")
        return "\n".join(lines).strip() + "\n"


def summarize_video_transcript(transcript: str, title: str = "Untitled Source", max_chars: int = 900) -> VideoSummary:
    chunks = chunk_text(transcript, max_chars=max_chars)
    if not chunks:
        raise ValueError("transcript is empty")

    notes = [_summarize_chunk(index + 1, chunk) for index, chunk in enumerate(chunks)]
    key_points = _dedupe(point for note in notes for point in note.key_points)[:10]
    takeaways = _dedupe(item for note in notes for item in note.takeaways)[:6]
    overview = " ".join(note.overview for note in notes[:2]).strip()

    return VideoSummary(
        title=title,
        chunk_count=len(chunks),
        overview=overview,
        key_points=key_points,
        takeaways=takeaways,
    )


def _summarize_chunk(index: int, chunk: str) -> ChunkNote:
    notes = summarize_meeting_transcript(chunk, title=f"Chunk {index}")
    overview = notes.summary
    takeaways = [
        item.task if item.owner in {"Host", "Speaker", "Unassigned"} else f"{item.owner}: {item.task}"
        for item in notes.action_items
    ]
    if not takeaways and notes.decisions:
        takeaways = notes.decisions[:2]
    return ChunkNote(
        chunk_index=index,
        overview=overview,
        key_points=notes.key_points,
        takeaways=takeaways,
    )


def _dedupe(items: object) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        text = str(item).strip()
        key = text.casefold()
        if text and key not in seen:
            seen.add(key)
            result.append(text)
    return result
