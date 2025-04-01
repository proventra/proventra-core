from abc import ABC, abstractmethod

from .results import SanitizationResult


class TextSanitizer(ABC):
    @abstractmethod
    def sanitize(self, text: str) -> SanitizationResult:
        """
        Sanitize text to remove prompt injection attempts.

        Args:
            text: The text to sanitize

        Returns:
            A SanitizationResult containing:
            - success: Whether sanitization was successful
            - sanitized_text: The sanitized text (if successful)
            - reason: Explanation of what was sanitized or why it failed
        """
        pass

    @property
    @abstractmethod
    def max_tokens(self) -> int:
        """Maximum number of tokens that can be sanitized."""
        pass
