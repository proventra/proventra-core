# Core Components

ProventraCore is organized into several modules, each with specific responsibilities.

## Analyzers

The `analyzers` module contains components responsible for analyzing text for safety risks.

### TransformersAnalyzer

The main implementation uses HuggingFace transformer models for text classification. By default, it uses our specialized model trained for autonomous agents.

```python
from proventra_core import TransformersAnalyzer

# Default setup (recommended for most cases)
analyzer = TransformersAnalyzer()  # Uses proventra/mdeberta-v3-base-prompt-injection

# Custom setup (all parameters optional)
custom_analyzer = TransformersAnalyzer(
    model_name="other/model",  # Default: proventra/mdeberta-v3-base-prompt-injection
    unsafe_label="OTHER_LABEL",  # Default: INJECTION
    threshold=0.7,  # Default: 0.5
    max_analysis_tokens=1024  # Optional: override max tokens per chunk
)
```

The analyzer automatically:
- Detects the model's maximum token length
- Splits long text into chunks
- Analyzes each chunk for safety risks
- Returns safety classification

## Sanitizers

The `sanitizers` module contains components for sanitizing unsafe text.

### LLMSanitizer

Uses large language models to sanitize unsafe content. By default, it uses Google's Gemini model.

```python
from proventra_core import LLMSanitizer

# Default setup (recommended for most cases)
# Note: Make sure to set GOOGLE_API_KEY in your environment variables
sanitizer = LLMSanitizer()  # Uses Google Gemini

# Custom setup (all parameters optional except api_key when not in env)
custom_sanitizer = LLMSanitizer(
    provider="openai",  # Default: google
    model_name="gpt-4",  # Default: provider's best model
    temperature=0.1,  # Default: 0.1
    max_tokens=4096,  # Default: 4096
    api_key="your-api-key"  # Optional if set in environment
)
```

API keys can be provided in two ways:
1. Set the appropriate environment variable:
   - Google: `GOOGLE_API_KEY`
   - OpenAI: `OPENAI_API_KEY`
   - Anthropic: `ANTHROPIC_API_KEY`
   - Mistral: `MISTRAL_API_KEY`
2. Pass directly via the `api_key` parameter

When using the default configuration (Google Gemini), make sure to set `GOOGLE_API_KEY` in your environment variables.

## Services

The `services` module combines analyzers and sanitizers.

### GuardService

The main service that coordinates text analysis and sanitization:

```python
from proventra_core import GuardService

guard = GuardService(analyzer, sanitizer)

# Analyze only
analysis = guard.analyze("Some text")
print(f"Unsafe: {analysis.unsafe}")

# Analyze and sanitize
result = guard.analyze_and_sanitize("Some text")
```