from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from .meeting_notes import summarize_meeting_transcript


@dataclass(frozen=True, slots=True)
class EvaluationCase:
    case_id: str
    transcript: str
    required_terms: list[str]
    forbidden_terms: list[str]
    required_sections: list[str]


@dataclass(frozen=True, slots=True)
class PromptVariant:
    label: str
    description: str


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    case_id: str
    variant: str
    score: float
    passed: int
    total: int
    failures: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ExperimentReport:
    baseline_variant: str
    winning_variant: str
    validation_delta: float
    regressions: int
    results: list[EvaluationResult]

    def to_dict(self) -> dict[str, Any]:
        return {
            "baselineVariant": self.baseline_variant,
            "winningVariant": self.winning_variant,
            "validationDelta": self.validation_delta,
            "regressions": self.regressions,
            "results": [
                {
                    "caseId": result.case_id,
                    "variant": result.variant,
                    "score": result.score,
                    "passed": result.passed,
                    "total": result.total,
                    "failures": result.failures,
                }
                for result in self.results
            ],
        }

    def to_markdown(self) -> str:
        lines = [
            "# AutoResearch Demo Report",
            "",
            f"- Baseline variant: `{self.baseline_variant}`",
            f"- Winning variant: `{self.winning_variant}`",
            f"- Validation delta: `{self.validation_delta:.3f}`",
            f"- Regressions: `{self.regressions}`",
            "",
            "## Results",
            "",
            "| Case | Variant | Score | Failures |",
            "| --- | --- | ---: | --- |",
        ]
        for result in self.results:
            failures = "; ".join(result.failures) if result.failures else "none"
            lines.append(f"| {result.case_id} | {result.variant} | {result.score:.3f} | {failures} |")
        return "\n".join(lines).strip() + "\n"


DEFAULT_VARIANTS = [
    PromptVariant("baseline", "Generic meeting summary prompt."),
    PromptVariant("detail-ownership-guard", "Preserve owners, dates, blockers, exact objects, and uncertainty."),
    PromptVariant("compact-executive", "Short executive recap with fewer operational details."),
]


def load_cases(path: Path) -> list[EvaluationCase]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [
        EvaluationCase(
            case_id=item["caseId"],
            transcript=item["transcript"],
            required_terms=list(item["requiredTerms"]),
            forbidden_terms=list(item["forbiddenTerms"]),
            required_sections=list(item["requiredSections"]),
        )
        for item in raw
    ]


def run_prompt_research(cases: list[EvaluationCase], variants: list[PromptVariant] | None = None) -> ExperimentReport:
    variants = variants or DEFAULT_VARIANTS
    results: list[EvaluationResult] = []

    for case in cases:
        for variant in variants:
            output = render_with_variant(case.transcript, variant)
            results.append(score_output(case, variant.label, output))

    baseline = _mean_score(results, "baseline")
    by_variant = {variant.label: _mean_score(results, variant.label) for variant in variants}
    winning_variant = max(by_variant, key=lambda label: by_variant[label])
    regressions = _count_regressions(results, baseline_label="baseline", candidate_label=winning_variant)

    return ExperimentReport(
        baseline_variant="baseline",
        winning_variant=winning_variant,
        validation_delta=round(by_variant[winning_variant] - baseline, 3),
        regressions=regressions,
        results=results,
    )


def render_with_variant(transcript: str, variant: PromptVariant) -> str:
    if variant.label == "baseline":
        return _baseline_summary()
    if variant.label == "compact-executive":
        notes = summarize_meeting_transcript(transcript, title="Executive Recap")
        return "\n".join(["# Executive Recap", "", "## Summary", notes.summary])
    notes = summarize_meeting_transcript(transcript, title="Operational Meeting Notes")
    return notes.to_markdown()


def score_output(case: EvaluationCase, variant: str, output: str) -> EvaluationResult:
    checks: list[tuple[bool, str]] = []
    lower = output.casefold()

    for term in case.required_terms:
        checks.append((term.casefold() in lower, f"missing required term: {term}"))
    for term in case.forbidden_terms:
        checks.append((term.casefold() not in lower, f"contains forbidden term: {term}"))
    for section in case.required_sections:
        checks.append((section.casefold() in lower, f"missing section: {section}"))

    passed = sum(1 for ok, _ in checks if ok)
    total = len(checks)
    failures = [reason for ok, reason in checks if not ok]
    score = passed / total if total else 1.0
    return EvaluationResult(case.case_id, variant, round(score, 3), passed, total, failures)


def write_report(report: ExperimentReport, json_path: Path, markdown_path: Path | None = None) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2) + "\n", encoding="utf-8")
    if markdown_path:
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_path.write_text(report.to_markdown(), encoding="utf-8")


def _baseline_summary() -> str:
    return "\n".join(
        [
            "# Meeting Summary",
            "",
            "## Summary",
            "The group discussed project progress and next steps.",
            "",
            "## Key Points",
            "- The team reviewed the work and will follow up later.",
            "",
            "## Next Steps",
            "| Owner | Action Item | Date |",
            "| --- | --- | --- |",
            "| Team | Follow up on open items | Unspecified |",
        ]
    )


def _mean_score(results: list[EvaluationResult], label: str) -> float:
    scores = [result.score for result in results if result.variant == label]
    return sum(scores) / len(scores) if scores else 0.0


def _count_regressions(results: list[EvaluationResult], baseline_label: str, candidate_label: str) -> int:
    by_case: dict[str, dict[str, float]] = {}
    for result in results:
        by_case.setdefault(result.case_id, {})[result.variant] = result.score
    return sum(
        1
        for values in by_case.values()
        if values.get(candidate_label, 0.0) < values.get(baseline_label, 0.0)
    )
