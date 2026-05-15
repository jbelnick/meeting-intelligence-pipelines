from __future__ import annotations

from dataclasses import dataclass, field
import re

from .transcript import iter_sentences_with_speaker, parse_turns


DECISION_TERMS = ("agreed", "approved", "confirmed", "decided", "selected", "will use")
RISK_TERMS = ("blocked", "blocker", "concern", "dependency", "missing", "risk", "waiting")
QUESTION_TERMS = ("clarify", "confirm whether", "open question", "need to know")
DATE_PATTERN = re.compile(
    r"\b(today|tomorrow|next week|this week|monday|tuesday|wednesday|thursday|friday|"
    r"january|february|march|april|may|june|july|august|september|october|november|december|"
    r"q[1-4]|\d{1,2}/\d{1,2}(?:/\d{2,4})?)\b",
    re.IGNORECASE,
)
ACTION_PATTERN = re.compile(
    r"\b(?P<owner>[A-Z][A-Za-z]+)\s+(?:will|needs to|should|to)\s+(?P<task>[^.?!]+)",
)
FOLLOW_UP_PATTERN = re.compile(r"\b(?:follow-up|follow up|action item)\s+is\s+to\s+(?P<task>[^.?!]+)", re.IGNORECASE)


@dataclass(frozen=True, slots=True)
class ActionItem:
    owner: str
    task: str
    date: str = ""


@dataclass(slots=True)
class MeetingNotes:
    title: str
    summary: str
    key_points: list[str] = field(default_factory=list)
    decisions: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)
    action_items: list[ActionItem] = field(default_factory=list)

    def to_markdown(self) -> str:
        lines = [f"# {self.title}", "", "## Summary", self.summary, ""]
        lines.extend(_render_list("## Key Points", self.key_points))
        lines.extend(_render_list("## Decisions", self.decisions or ["None identified."]))
        lines.extend(_render_list("## Risks And Blockers", self.risks or ["None identified."]))
        lines.extend(_render_actions(self.action_items))
        lines.extend(_render_list("## Open Questions", self.open_questions or ["None identified."]))
        return "\n".join(lines).strip() + "\n"


def summarize_meeting_transcript(transcript: str, title: str | None = None) -> MeetingNotes:
    turns = parse_turns(transcript)
    if not turns:
        raise ValueError("transcript is empty")

    sentence_rows = list(iter_sentences_with_speaker(turns))
    all_sentences = [sentence for _, sentence in sentence_rows]
    title_value = title or _title_from_sentences(all_sentences)
    key_points = _unique(_high_signal_sentences(all_sentences))[:7]
    decisions = _unique([s for s in all_sentences if _contains_any(s, DECISION_TERMS)])[:5]
    risks = _unique([s for s in all_sentences if _contains_any(s, RISK_TERMS)])[:5]
    open_questions = _unique([s for s in all_sentences if "?" in s or _contains_any(s, QUESTION_TERMS)])[:5]
    actions = _extract_actions(sentence_rows)
    summary = _build_summary(key_points, decisions, risks)

    return MeetingNotes(
        title=title_value,
        summary=summary,
        key_points=key_points,
        decisions=decisions,
        risks=risks,
        open_questions=open_questions,
        action_items=actions,
    )


def _build_summary(key_points: list[str], decisions: list[str], risks: list[str]) -> str:
    parts: list[str] = []
    if key_points:
        parts.append(key_points[0].rstrip(".") + ".")
    if decisions:
        parts.append("The clearest decision was: " + decisions[0].rstrip(".") + ".")
    if risks:
        parts.append("The main delivery risk was: " + risks[0].rstrip(".") + ".")
    if len(parts) < 2 and len(key_points) > 1:
        parts.append(key_points[1].rstrip(".") + ".")
    return " ".join(parts)


def _contains_any(sentence: str, terms: tuple[str, ...]) -> bool:
    lower = sentence.casefold()
    return any(term in lower for term in terms)


def _extract_actions(sentence_rows: list[tuple[str, str]]) -> list[ActionItem]:
    items: list[ActionItem] = []
    for speaker, sentence in sentence_rows:
        match = ACTION_PATTERN.search(sentence)
        if match:
            owner = match.group("owner")
            task = match.group("task").strip()
        elif follow_up := FOLLOW_UP_PATTERN.search(sentence):
            owner = speaker if speaker != "Speaker" else "Unassigned"
            task = follow_up.group("task").strip()
        else:
            continue

        date_match = DATE_PATTERN.search(sentence)
        date = date_match.group(0) if date_match else ""
        item = ActionItem(owner=owner, task=_trim_task(task), date=date)
        if item not in items:
            items.append(item)
    return items[:8]


def _high_signal_sentences(sentences: list[str]) -> list[str]:
    scored: list[tuple[int, str]] = []
    for sentence in sentences:
        score = 0
        if re.search(r"\b[A-Z][A-Za-z0-9_-]{2,}\b", sentence):
            score += 1
        if re.search(r"\d", sentence):
            score += 1
        if _contains_any(sentence, DECISION_TERMS + RISK_TERMS):
            score += 2
        if any(term in sentence.casefold() for term in ("owner", "date", "metric", "launch", "review", "handoff")):
            score += 1
        if score:
            scored.append((score, sentence.strip()))
    scored.sort(key=lambda row: (-row[0], sentences.index(row[1])))
    return [sentence for _, sentence in scored]


def _title_from_sentences(sentences: list[str]) -> str:
    for sentence in sentences:
        words = re.findall(r"[A-Za-z0-9-]+", sentence)
        if len(words) >= 4:
            return " ".join(words[:8]).title()
    return "Meeting Notes"


def _trim_task(task: str) -> str:
    cleaned = re.sub(r"\s+", " ", task).strip(" -")
    return cleaned[:1].upper() + cleaned[1:] if cleaned else "Follow up"


def _render_list(heading: str, items: list[str]) -> list[str]:
    lines = [heading]
    lines.extend(f"- {item}" for item in items)
    lines.append("")
    return lines


def _render_actions(items: list[ActionItem]) -> list[str]:
    lines = ["## Next Steps"]
    if not items:
        lines.extend(["None identified.", ""])
        return lines
    lines.extend(["| Owner | Action Item | Date |", "| --- | --- | --- |"])
    for item in items:
        lines.append(f"| {item.owner} | {item.task} | {item.date or 'Unspecified'} |")
    lines.append("")
    return lines


def _unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        key = item.casefold()
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result
