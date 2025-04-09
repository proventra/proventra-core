# Getting Started with ProventraCore

This guide will help you get started with ProventraCore.

## Installation

Install using pip:

```bash
# Basic installation
pip install proventra-core

# With specific LLM provider
pip install proventra-core[google]

# With multiple providers
pip install proventra-core[openai,anthropic]

# With all providers
pip install proventra-core[all]
```

## API Keys

Before using the library, you'll need an API key from your chosen LLM provider. You can either:

1. Set it in your environment variables:
```bash
# For Google (required for default setup)
export GOOGLE_API_KEY=your-api-key

# For other providers (optional)
export OPENAI_API_KEY=your-api-key
export ANTHROPIC_API_KEY=your-api-key
export MISTRAL_API_KEY=your-api-key
```

2. Or use a `.env` file in your project root:
```bash
GOOGLE_API_KEY=your-api-key
```

3. Or pass it directly in code (see custom setup below)

## Basic Usage

### Default Setup (Recommended for Most Cases)

```python
from proventra_core import GuardService, TransformersAnalyzer, LLMSanitizer

# Initialize with default components
# Note: Make sure to set GOOGLE_API_KEY in your environment variables
analyzer = TransformersAnalyzer()  # Uses our model
sanitizer = LLMSanitizer()  # Uses Google Gemini
guard = GuardService(analyzer, sanitizer)

# Analyze text for safety
analysis = guard.analyze("Some potentially unsafe text")
print(f"Unsafe: {analysis.unsafe}")
print(f"Risk Score: {analysis.risk_score}")

# Analyze and sanitize text
result = guard.analyze_and_sanitize("Some potentially unsafe text")
if result.unsafe:
    print("Text contains prompt injection")
    if result.sanitized:
        print(f"Sanitized version: {result.sanitized}")
else:
    print("Text is safe")
```

### Custom Setup (For Advanced Use Cases)

```python
from proventra_core import GuardService, TransformersAnalyzer, LLMSanitizer

# Customize analyzer (all parameters optional)
analyzer = TransformersAnalyzer(
    model_name="other/model",  # Default: proventra/mdeberta-v3-base-prompt-injection
    unsafe_label="OTHER_LABEL",  # Default: INJECTION
    threshold=0.7,  # Default: 0.5
    max_analysis_tokens=1024  # Optional: override max tokens per chunk
)

# Customize sanitizer (all parameters optional except api_key when not in env)
sanitizer = LLMSanitizer(
    provider="openai",  # Default: google
    model_name="gpt-4",  # Default: provider's best model
    temperature=0.1,  # Default: 0.1
    max_tokens=4096,  # Default: 4096
    api_key="your-openai-api-key"  # Optional if set in environment
)

# Create guard service with custom components
guard = GuardService(analyzer, sanitizer)
```

## Environment Variables

For the default setup, you only need:
```bash
GOOGLE_API_KEY=your-google-api-key
```

For custom setups, you might need:
```bash
# Optional - defaults to our model
CLASSIFICATION_MODEL_NAME=path/to/model
CLASSIFICATION_MODEL_UNSAFE_LABEL=unsafe

# Optional - defaults to Google Gemini
LLM_PROVIDER=google
LLM_MODEL_NAME=gemini-2.0-flash
LLM_TEMPERATURE=0.1
MAX_SANITIZATION_TOKENS=4096

# Required for the provider you're using
GOOGLE_API_KEY=your-google-api-key
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
MISTRAL_API_KEY=your-mistral-api-key
```

## Hosted API Option

If you prefer not to set up your own instance, you can use our [hosted API](https://api.proventra-ai.com/docs):

```bash
curl -X POST https://api.proventra-ai.com/api/v1/analyze \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "text": "Text to analyze",
    "sanitize": true
  }'
```

Python example:

```python
import requests

response = requests.post(
    "https://api.proventra-ai.com/api/v1/analyze",
    headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_API_KEY"
    },
    json={
        "text": "Text to analyze", 
        "sanitize": true
    }
)

result = response.json()
print(f"Unsafe: {result['unsafe']}")
if result.get('sanitized'):
    print(f"Sanitized: {result['sanitized']}")
```

## Next Steps

- Learn about [Core Components](./components.md)
- Explore [Advanced Usage](./advanced-usage.md)
- See [Deployment Examples](./deployment.md) 