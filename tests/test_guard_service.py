"""Tests for the GuardService."""

import pytest

from proventra_core import (
    FullAnalysisResult,
    GuardService,
    SanitizationResult,
    TextAnalyzer,
    TextSanitizer,
)


class MockAnalyzer(TextAnalyzer):
    def __init__(self, unsafe_outputs: list[bool]):
        self.unsafe_outputs = unsafe_outputs
        self.call_count = 0

    def analyze(self, text: str) -> dict[str, bool]:
        """Simulates analysis, returning predefined safety status."""
        if self.call_count >= len(self.unsafe_outputs):
            raise IndexError(
                "MockAnalyzer called more times than expected outputs provided."
            )
        result = {"unsafe": self.unsafe_outputs[self.call_count]}
        self.call_count += 1
        return result

    @property
    def max_tokens(self) -> int:
        """Dummy implementation for abstract property."""
        return 1024  # Return a dummy value


class MockSanitizer(TextSanitizer):
    def __init__(self, result: SanitizationResult):
        self.result = result
        self.call_count = 0

    def sanitize(self, text: str) -> SanitizationResult:
        """Simulates sanitization, returning a predefined result."""
        self.call_count += 1
        return self.result

    @property
    def max_tokens(self) -> int:
        """Dummy implementation for abstract property."""
        return 1024  # Return a dummy value


@pytest.fixture
def mock_analyzer() -> MockAnalyzer:
    # Default behavior can be overridden in tests
    return MockAnalyzer(unsafe_outputs=[False])


@pytest.fixture
def mock_sanitizer() -> MockSanitizer:
    # Default behavior can be overridden in tests
    return MockSanitizer(
        SanitizationResult(success=True, sanitized_text="Sanitized text", reason=None)
    )


@pytest.fixture
def guard_service(
    mock_analyzer: MockAnalyzer, mock_sanitizer: MockSanitizer
) -> GuardService:
    """Provides a GuardService instance with mock dependencies."""
    return GuardService(analyzer=mock_analyzer, sanitizer=mock_sanitizer)


def test_guard_service_initialization(guard_service: GuardService):
    """Test that GuardService can be initialized with mocks."""
    assert isinstance(guard_service, GuardService)
    assert isinstance(guard_service.analyzer, MockAnalyzer)
    assert isinstance(guard_service.sanitizer, MockSanitizer)


def test_analyze_and_sanitize_safe_input(
    guard_service: GuardService, mock_analyzer: MockAnalyzer
):
    """Test analyze_and_sanitize when the initial analysis is safe."""
    mock_analyzer.unsafe_outputs = [False]  # Analyzer reports safe
    prompt = "This is a safe prompt."
    result = guard_service.analyze_and_sanitize(prompt)

    assert isinstance(result, FullAnalysisResult)
    assert not result.unsafe
    assert result.sanitized is None
    assert result.sanitization_details is None
    assert mock_analyzer.call_count == 1  # Only initial analysis should occur


def test_analyze_and_sanitize_unsafe_input_sanitization_fails(
    guard_service: GuardService,
    mock_analyzer: MockAnalyzer,
    mock_sanitizer: MockSanitizer,
):
    """Test analyze_and_sanitize when input is unsafe and sanitization fails."""
    mock_analyzer.unsafe_outputs = [True]  # Initial analysis: unsafe
    failed_sanitization = SanitizationResult(
        success=False, sanitized_text=None, reason="Failed"
    )
    mock_sanitizer.result = failed_sanitization

    prompt = "Unsafe prompt here."
    result = guard_service.analyze_and_sanitize(prompt)

    assert isinstance(result, FullAnalysisResult)
    assert result.unsafe  # Original prompt was unsafe
    assert result.sanitized is None  # Sanitization failed
    assert result.sanitization_details == failed_sanitization
    assert mock_analyzer.call_count == 1  # Only initial analysis
    assert mock_sanitizer.call_count == 1  # Sanitizer was called


def test_analyze_and_sanitize_unsafe_input_sanitized_still_unsafe(
    guard_service: GuardService,
    mock_analyzer: MockAnalyzer,
    mock_sanitizer: MockSanitizer,
):
    """Test analyze_and_sanitize when sanitized output is still unsafe."""
    mock_analyzer.unsafe_outputs = [True, True]  # Initial: unsafe, Sanitized: unsafe
    successful_sanitization = SanitizationResult(
        success=True, sanitized_text="Still unsafe sanitized text", reason=None
    )
    mock_sanitizer.result = successful_sanitization

    prompt = "Very unsafe prompt."
    result = guard_service.analyze_and_sanitize(prompt)

    assert isinstance(result, FullAnalysisResult)
    assert result.unsafe  # Original prompt was unsafe
    assert result.sanitized is None  # Sanitized text was unsafe, so not returned
    assert result.sanitization_details == successful_sanitization
    assert mock_analyzer.call_count == 2  # Initial + sanitized analysis
    assert mock_sanitizer.call_count == 1  # Sanitizer was called


def test_analyze_and_sanitize_unsafe_input_sanitized_is_safe(
    guard_service: GuardService,
    mock_analyzer: MockAnalyzer,
    mock_sanitizer: MockSanitizer,
):
    """Test analyze_and_sanitize when sanitized output is safe."""
    mock_analyzer.unsafe_outputs = [True, False]  # Initial: unsafe, Sanitized: safe
    safe_sanitized_text = "This is now safe."
    successful_sanitization = SanitizationResult(
        success=True, sanitized_text=safe_sanitized_text, reason=None
    )
    mock_sanitizer.result = successful_sanitization

    prompt = "Malicious prompt that can be fixed."
    result = guard_service.analyze_and_sanitize(prompt)

    assert isinstance(result, FullAnalysisResult)
    assert result.unsafe  # Original prompt was unsafe
    assert result.sanitized == safe_sanitized_text  # Sanitized text is returned
    assert result.sanitization_details == successful_sanitization
    assert mock_analyzer.call_count == 2  # Initial + sanitized analysis
    assert mock_sanitizer.call_count == 1  # Sanitizer was called
