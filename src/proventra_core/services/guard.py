from ..analyzers.base import TextAnalyzer
from ..analyzers.results import AnalysisResult, FullAnalysisResult
from ..sanitizers.base import TextSanitizer
from ..sanitizers.results import SanitizationResult


class GuardService:
    def __init__(self, analyzer: TextAnalyzer, sanitizer: TextSanitizer):
        self.analyzer = analyzer
        self.sanitizer = sanitizer

    def analyze(self, text: str) -> AnalysisResult:
        """
        Analyzes text for safety without sanitization.
        """
        result = self.analyzer.analyze(text)
        return AnalysisResult(unsafe=result["unsafe"])

    def sanitize(self, text: str) -> SanitizationResult:
        """
        Only sanitizes the text without analysis, returning a structured result.
        """
        return self.sanitizer.sanitize(text)

    def analyze_and_sanitize(self, text: str) -> FullAnalysisResult:
        """
        Analyzes text for safety and sanitizes if needed.
        Returns complete analysis results including sanitization details and
        the final sanitized version if available and safe.
        """
        # First analysis
        analysis_result = self.analyze(text)
        is_unsafe = analysis_result.unsafe

        # If safe, return initial analysis only, no sanitization details needed
        if not is_unsafe:
            return FullAnalysisResult(
                unsafe=is_unsafe, sanitized=None, sanitization_details=None
            )

        # If unsafe, attempt to sanitize
        sanitization_result = self.sanitize(text)

        # If sanitization failed or didn't produce text
        if not sanitization_result.success or not sanitization_result.sanitized_text:
            print(
                f"Sanitization failed or produced no text. Reason: {sanitization_result.reason}"
            )
            # Return original analysis, include failed sanitization details
            return FullAnalysisResult(
                unsafe=is_unsafe,
                sanitized=None,
                sanitization_details=sanitization_result,
            )

        # Analyze sanitized text
        sanitized_analysis = self.analyze(sanitization_result.sanitized_text)
        sanitized_is_unsafe = sanitized_analysis.unsafe

        # If sanitized text is still unsafe
        if sanitized_is_unsafe:
            print("Sanitization succeeded but result is still unsafe.")
            # Return original analysis, include the sanitization attempt details, but don't provide the unsafe sanitized text
            return FullAnalysisResult(
                unsafe=is_unsafe,
                sanitized=None,  # Don't return the unsafe sanitized text
                sanitization_details=sanitization_result,  # Include details of the attempt
            )

        # Sanitization succeeded and result is safe
        # Return original analysis, include successful sanitization details, and the safe sanitized text
        return FullAnalysisResult(
            unsafe=is_unsafe,
            sanitized=sanitization_result.sanitized_text,
            sanitization_details=sanitization_result,
        )
