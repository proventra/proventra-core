# Getting Started with ProventraCore

This guide will help you get started with ProventraCore

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
# For Google
export GOOGLE_API_KEY=your-api-key

# For OpenAI
export OPENAI_API_KEY=your-api-key

# For Anthropic
export ANTHROPIC_API_KEY=your-api-key

# For Mistral
export MISTRAL_API_KEY=your-api-key
```

2. Or use a `.env` file in your project root:
```bash
GOOGLE_API_KEY=your-api-key
```

3. Or pass it directly in code (see example below)

## Basic Usage

Here's a simple example of how to use ProventraCore:

```python
from proventra_core import GuardService, TransformersAnalyzer, LLMSanitizer

# Initialize analyzer
analyzer = TransformersAnalyzer(
    model_name="path/to/classification/model",
    unsafe_label="unsafe"
)

# Initialize sanitizer
sanitizer = LLMSanitizer(
    provider="google",
    model_name="gemini-2.0-flash",
    temperature=0.1,
    max_tokens=4096,
    api_key="your-api-key"  # Pass your API key directly
)

# Create guard service
guard = GuardService(analyzer, sanitizer)

# Analyze text for safety
analysis = guard.analyze("Some potentially unsafe text")
print(f"Unsafe: {analysis.unsafe}")

# Analyze and sanitize text
result = guard.analyze_and_sanitize("Some potentially unsafe text")
if result.unsafe:
    print("Text contains prompt injection")
    if result.sanitized:
        print(f"Sanitized version: {result.sanitized}")
else:
    print("Text is safe")
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