"""Basic tests for the proventra_core package."""


def test_import():
    """Test that the package can be imported."""
    import proventra_core

    assert proventra_core.__version__ == "0.0.1"


def test_models_import():
    """Test that the models can be imported."""
    from proventra_core import TextAnalyzer, TextSanitizer

    assert TextAnalyzer
    assert TextSanitizer
