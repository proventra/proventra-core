# ProventraCore

A Python library for detecting and preventing prompt injection attacks in LLM applications.

## Features

- Text safety classification using transformer models
- Content sanitization using LLMs
- Modular architecture with clear interfaces
- Flexible configuration options

## Requirements

- Python 3.11 or higher
- For GPU acceleration: PyTorch with CUDA support

## Installation

```bash
# Basic installation
pip install proventra-core

# With specific LLM provider
pip install proventra-core[google]

# With multiple providers
pip install proventra-core[openai,anthropic]

# With all providers
pip install proventra-core[all]

# For development
pip install proventra-core[all,dev]
```

## Quick Start

```python
from proventra_core import GuardService, TransformersAnalyzer, LLMSanitizer

# Initialize components
analyzer = TransformersAnalyzer(
    model_name="path/to/classification/model",
    unsafe_label="unsafe"
)

sanitizer = LLMSanitizer(
    provider="google",
    model_name="gemini-2.0-flash",
    temperature=0.1,
    max_tokens=4096
    api_key="your-llm-provider-api-key"
)

# Create service
guard = GuardService(analyzer, sanitizer)

# Analyze text
analysis = guard.analyze("Some potentially unsafe text")
print(f"Unsafe: {analysis.unsafe}")
print(f"Unsafe: {analysis.risk_score}")

# Analyze and sanitize
result = guard.analyze_and_sanitize("Some potentially unsafe text")
if result.unsafe:
    print("Text contains prompt injection")
    if result.sanitized:
        print(f"Sanitized version: {result.sanitized}")
else:
    print("Text is safe")
```

## Hosted API

For quick implementation without setup, use our hosted API service at [https://api.proventra-ai.com/docs](https://api.proventra-ai.com/docs).

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

You can use the benchmark to figure out which configuration works best for you. See the [benchmark documentation](benchmark/README.md).

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
