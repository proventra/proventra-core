from dataclasses import dataclass
from typing import Optional


@dataclass
class SanitizationResult:
    """Result of sanitization attempt."""

    success: bool
    sanitized_text: Optional[str] = None
    reason: Optional[str] = None
