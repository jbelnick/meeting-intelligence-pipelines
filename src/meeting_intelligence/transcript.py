from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable


SPEAKER_LINE = re.compile(r"^(?P<speaker>[A-Za-z][A-Za-z0-9 ._-]{0,40}):\s*(?P<text>.+)$")
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


@dataclass(frozen=True, slots=True)
class TranscriptTurn:
    speaker: str
    text: str


def normalize_text(text: str) -> str:
    return re.sub(r"[ \t]+", " ", text.replace("\r\n", "\n")).strip()


def parse_turns(transcript: str) -> list[TranscriptTurn]:
    normalized = normalize_text(transcript)
    if not normalized:
        return []

    turns: list[TranscriptTurn] = []
    current_speaker = "Speaker"
    current_lines: list[str] = []

    for raw_line in normalized.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = SPEAKER_LINE.match(line)
        if match:
            if current_lines:
                turns.append(TranscriptTurn(current_speaker, " ".join(current_lines)))
            current_speaker = match.group("speaker").strip()
            current_lines = [match.group("text").strip()]
        elif current_lines:
            current_lines.append(line)
        else:
            current_lines = [line]

    if current_lines:
        turns.append(TranscriptTurn(current_speaker, " ".join(current_lines)))
    return turns


def sentences(text: str) -> list[str]:
    normalized = normalize_text(text)
    if not normalized:
        return []
    return [part.strip() for part in SENTENCE_SPLIT.split(normalized) if part.strip()]


def iter_sentences_with_speaker(turns: Iterable[TranscriptTurn]) -> Iterable[tuple[str, str]]:
    for turn in turns:
        for sentence in sentences(turn.text):
            yield turn.speaker, sentence


def chunk_text(text: str, max_chars: int = 900) -> list[str]:
    if max_chars < 200:
        raise ValueError("max_chars must be at least 200")

    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", normalize_text(text)) if part.strip()]
    units = paragraphs or sentences(text)

    for unit in units:
        if len(unit) > max_chars:
            if current:
                chunks.append("\n\n".join(current))
                current = []
                current_len = 0
            for index in range(0, len(unit), max_chars):
                part = unit[index : index + max_chars].strip()
                if part:
                    chunks.append(part)
            continue

        added = len(unit) if not current else len(unit) + 2
        if current and current_len + added > max_chars:
            chunks.append("\n\n".join(current))
            current = [unit]
            current_len = len(unit)
        else:
            current.append(unit)
            current_len += added

    if current:
        chunks.append("\n\n".join(current))
    return chunks
