from abc import ABC, abstractmethod
from typing import Any, Dict


class TextAnalyzer(ABC):
    @abstractmethod
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyze text for prompt injection attacks.

        Args:
            text: The text to analyze

        Returns:
            Dict containing at minimum:
            - unsafe: bool - True if text contains prompt injection, False if safe

            Can be extended with additional properties in the future without breaking API
        """
        pass

    @property
    @abstractmethod
    def max_tokens(self) -> int:
        """Maximum number of tokens to analyze in a single chunk."""
        pass
