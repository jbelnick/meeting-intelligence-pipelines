from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class ReplayReport:
    recording_title: str
    channel: str
    source: str
    pipeline_type: str
    delivered_model: str
    evaluation_winner: str
    autoresearch_status: str
    promoted_variant: str
    validation_delta: float

    def to_markdown(self) -> str:
        return "\n".join(
            [
                "# Real Workflow Replay",
                "",
                "## Slack To Native Voice Memo",
                f"- Recording: {self.recording_title}",
                f"- Channel: `{self.channel}`",
                f"- Source: `{self.source}`",
                f"- Pipeline type: `{self.pipeline_type}`",
                f"- Delivered model: `{self.delivered_model}`",
                f"- Evaluation winner: `{self.evaluation_winner}`",
                "",
                "## AutoResearch",
                f"- Status: `{self.autoresearch_status}`",
                f"- Promoted variant: `{self.promoted_variant}`",
                f"- Validation delta: `{self.validation_delta:.3f}`",
                "",
                "## Replay Interpretation",
                "This replay uses sanitized artifacts with production-shaped schemas. It does not call Slack, macOS Voice Memos, local model servers, or private infrastructure.",
            ]
        ).strip() + "\n"


def replay_case_study(artifact_root: Path) -> ReplayReport:
    recording_dir = artifact_root / "voice-memo-recording"
    autoresearch_dir = artifact_root / "autoresearch"
    metadata = _read_json(recording_dir / "metadata.json")
    evaluation = _read_json(recording_dir / "summary-evaluation.json")
    summary = _read_json(autoresearch_dir / "voice-memo-summary-qwen3.6-27b-q5_K_M.summary.json")
    proposal = _read_json(autoresearch_dir / "voice-memo-summary-qwen3.6-27b-q5_K_M.proposal.json")

    winner = evaluation.get("winner", {})
    promotion = summary.get("promotion", {})
    settings = proposal.get("settings", {})

    return ReplayReport(
        recording_title=str(metadata.get("title") or recording_dir.name),
        channel=str(metadata.get("channel") or ""),
        source=str(metadata.get("source") or ""),
        pipeline_type=str(metadata.get("pipelineType") or ""),
        delivered_model=str(metadata.get("summaryModel") or ""),
        evaluation_winner=str(winner.get("model") or ""),
        autoresearch_status=str(summary.get("status") or ""),
        promoted_variant=str(settings.get("label") or ""),
        validation_delta=float(promotion.get("validationDelta") or 0.0),
    )


def _read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data
