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
- Analyzes each chunk for safety risks
- Returns safety classification

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
print(f"Unsafe: {analysis.unsafe}")

# Analyze and sanitize
result = guard.analyze_and_sanitize("Some text")
```

## Advanced Features

### Risk Score Analysis

The analyzer can provide detailed risk scores and custom thresholds:

```python
# Initialize with custom threshold
analyzer = TransformersAnalyzer(
    model_name="path/to/model",
    unsafe_label="unsafe",
    threshold=0.7  # Risk score threshold (0 to 1)
)

# Get risk scores in analysis
analysis = guard.analyze("Some text")
print(f"Unsafe: {analysis.unsafe}")
print(f"Risk Score: {analysis.risk_score}")  # 0.0 to 1.0
```

The analyzer:
- Calculates risk scores (0 to 1) for each chunk
- Considers text unsafe if risk score ≥ threshold
- Returns both safety classification and risk score

### Custom System Prompts

The sanitizer can be customized with your own system prompt:

```python
sanitizer = LLMSanitizer(
    provider="google",
    model_name="gemini-2.0-flash",
    temperature=0.1,
    max_tokens=4096,
    system_prompt="""Your custom system prompt that instructs the LLM
    how to sanitize the text. Must return JSON with:
    - success: boolean
    - sanitized_text: string | null
    - reason: string"""
)
```