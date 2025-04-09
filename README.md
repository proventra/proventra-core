<div align="center">
  <img alt="logo" src="./static/logo-square.png" width="100"/>
</div>

<h1 align="center"> Proventra-core</h1>

A Python library for detecting and preventing prompt injection attacks in LLM applications.

## Features

- Text safety classification using transformer models
- Content sanitization using LLMs
- Modular architecture with clear interfaces
- Flexible configuration options

## Requirements

- Python 3.11 or higher

## Installation

```bash
# Basic installation
pip install proventra-core[google]

# With different LLM provider
pip install proventra-core[openai]

# With multiple providers
pip install proventra-core[openai,anthropic]

# With all providers
pip install proventra-core[all]

# For development
pip install proventra-core[all,dev]
```

## Quick Start

### Default Setup (Recommended for Most Cases)

```python
from proventra_core import GuardService, TransformersAnalyzer, LLMSanitizer

# Initialize with default components
# Note: Make sure to set GOOGLE_API_KEY in your environment variables
analyzer = TransformersAnalyzer()  # Uses proventra/mdeberta-v3-base-promp-injection model
sanitizer = LLMSanitizer()  # Uses Google Gemini-2.0-flash
guard = GuardService(analyzer, sanitizer)

# Analyze text
analysis = guard.analyze("Some potentially unsafe text")
print(f"Unsafe: {analysis.unsafe}")
print(f"Risk Score: {analysis.risk_score}")

# Analyze and sanitize
result = guard.analyze_and_sanitize("Some potentially unsafe text")
if result.unsafe:
    print("Text contains prompt injection")
    if result.sanitized:
        print(f"Sanitized version: {result.sanitized}")
else:
    print("Text is safe")
```

### Setup with custom models

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

# Create service with custom components
guard = GuardService(analyzer, sanitizer)
```

### Environment Variables

For the default setup, you only need:
```bash
GOOGLE_API_KEY=your-google-api-key
```

For custom setups, you might need:
```bash
# Optional - defaults to our specialized model
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

## Hosted API

For quick implementation without setup or the need to host a classifier model (yes, the library runs a classifier model localy), use our hosted API service at [https://api.proventra-ai.com/docs](https://api.proventra-ai.com/docs).

## Core Components

The library is organized into the following modules:

1. **Models** (`proventra_core.models`)
   - Base interfaces (`TextAnalyzer`, `TextSanitizer`)
   - Result models (`AnalysisResult`, `SanitizationResult`, `FullAnalysisResult`)

2. **Analyzers** (`proventra_core.analyzers`)
   - `TransformersAnalyzer` - HuggingFace-based text safety analysis

3. **Sanitizers** (`proventra_core.sanitizers`)
   - `LLMSanitizer` - LLM-based text sanitization

4. **Providers** (`proventra_core.providers`)
   - LLM provider factory and configuration
   - Supports: Google, OpenAI, Anthropic, Mistral

5. **Services** (`proventra_core.services`)
   - `GuardService` - Main service combining analysis and sanitization

## Advanced Usage

### Custom Analyzer

```python
from proventra_core import TextAnalyzer, GuardService
from typing import Dict, Any

class CustomAnalyzer(TextAnalyzer):
    def __init__(self, threshold=0.5):
        self.threshold = threshold
        self.risk_scores = {
            "hack": 0.9,
            "ignore": 0.8,
            "system": 0.7
        }
        
    def analyze(self, text: str) -> Dict[str, Any]:
        # Your custom analysis logic
        text_lower = text.lower()
        matched_keywords = [word for word in self.risk_scores.keys() if word in text_lower]
        
        # Calculate overall risk score based on highest risk word found
        risk_score = 0.2  # Default low risk
        if matched_keywords:
            risk_score = max(self.risk_scores[word] for word in matched_keywords)
            
        return {
            "unsafe": risk_score > treshold,
            "risk_score": risk_score,
            "matched_keywords": matched_keywords,
            "word_risks": {word: self.risk_scores[word] for word in matched_keywords}
        }
        
    @property
    def max_tokens(self):
        return 1024
        
    @property
    def chunk_overlap(self):
        return 128

# Use with existing service
guard = GuardService(CustomAnalyzer(threshold=0.7), existing_sanitizer)
```

## Benchmarking

You can use the benchmark to figure out which configuration works best for you. See [benchmark documentation](benchmark/README.md).
We recommend using our [proventra/mdeberta-v3-base-prompt-injection](https://huggingface.co/proventra/mdeberta-v3-base-prompt-injection) model, which was specificaly trained with autonomous agents in mind.

## Deployment Examples

The repository includes examples for deploying the library:

### FastAPI Server

```bash
cd examples/api
pip install -e "../../[api,all]"
uvicorn main:app --reload
```

### RunPod Serverless

```bash
cd examples/runpod
pip install -e "../../[runpod,all]"
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License
