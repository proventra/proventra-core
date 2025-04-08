from dataclasses import dataclass
from typing import Optional

from ..sanitizers.results import SanitizationResult


@dataclass
class AnalysisResult:
    """Result of safety analysis containing binary classification and risk score."""

    unsafe: bool
    risk_score: float


@dataclass
class FullAnalysisResult(AnalysisResult):
    """Combined result of analysis and (optional) sanitization."""

    sanitized: Optional[str] = None
    sanitization_details: Optional[SanitizationResult] = None
