# Core Components

ProventraCore is organized into several modules, each with specific responsibilities.

## Analyzers

The `analyzers` module contains components responsible for analyzing text for safety risks.

### TransformersAnalyzer

The main implementation uses HuggingFace transformer models for text classification:

```python
from proventra_core import TransformersAnalyzer

analyzer = TransformersAnalyzer(
    model_name="path/to/model",
    unsafe_label="unsafe"
)
```

The analyzer automatically:
- Detects the model's maximum token length
- Splits long text into chunks
- Analyzes each chunk
- Considers the text unsafe if any chunk is unsafe

## Sanitizers

The `sanitizers` module contains components for sanitizing unsafe text.

### LLMSanitizer

Uses large language models to sanitize unsafe content:

```python
from proventra_core import LLMSanitizer

# Using API key from environment variable (e.g. GOOGLE_API_KEY)
sanitizer = LLMSanitizer(
    provider="google",      # "openai", "anthropic", "mistral"
    model_name="gemini-2.0-flash",
    temperature=0.1,
    max_tokens=4096
)

# Or passing API key directly
sanitizer = LLMSanitizer(
    provider="google",
    model_name="gemini-2.0-flash",
    temperature=0.1,
    max_tokens=4096,
    api_key="your-api-key"  # Directly pass your API key
)
```

Each provider requires its own API key:
- Google: Set `GOOGLE_API_KEY` or pass via `api_key`
- OpenAI: Set `OPENAI_API_KEY` or pass via `api_key`
- Anthropic: Set `ANTHROPIC_API_KEY` or pass via `api_key`
- Mistral: Set `MISTRAL_API_KEY` or pass via `api_key`

## Services

The `services` module combines analyzers and sanitizers.

### GuardService

The main service that coordinates text analysis and sanitization:

```python
from proventra_core import GuardService

guard = GuardService(analyzer, sanitizer)

# Analyze only
analysis = guard.analyze("Some text")

# Analyze and sanitize
result = guard.analyze_and_sanitize("Some text")
```