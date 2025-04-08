# ProventraCore Benchmark

This module provides benchmarking functionality for evaluating the ProventraCore library's effectiveness in detecting and mitigating prompt injection attacks.

## Features

- Comprehensive evaluation of detection accuracy
- Measurement of sanitization effectiveness
- Performance metrics (processing time)
- Analysis by attack category and difficulty level
- Visualization of results with plots
- Detailed JSON reports

## Requirements

- ProventraCore library
- A trained classifier model
- Access to an LLM API (Google, OpenAI, Anthropic, or Mistral)
- Additional Python packages: matplotlib, pandas, scikit-learn

## Installation

Install the required dependencies:

```bash
# Install uv (if not already installed)
pip install uv

# Create a virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On Unix/MacOS
# or
.venv\Scripts\activate  # On Windows

# Install dependencies with uv
uv pip install -e ".[all,dev]"
```

## Usage

Run the benchmark with a classifier model and LLM provider:

```bash
cd examples/benchmark
python run_benchmark.py --model_path "classifier/model" --unsafe_labe "unsafe" --provider "google" --model_name "gemini-2.0-flash"

## protectai example
python run_benchmark.py --model_path "protectai/deberta-v3-base-prompt-injection-v2" --unsafe_label "INJECTION"  --provider "google" --model_name "gemini-2.0-flash"     

## arch-guar example
python run_benchmark.py --model_path "katanemolabs/Arch-Guard" --unsafe_label "JAILBREAK"  --provider "google" --model_name "gemini-2.0-flash"     
```

### Command Line Arguments

- `--model_path`: Path to the transformer model for text classification (required)
- `--provider`: LLM provider for sanitization (default: "google")
- `--model_name`: Specific model name for sanitization
- `--temperature`: Temperature for LLM generation (default: 0.1)
- `--max_tokens`: Maximum tokens for LLM generation (default: 4096)
- `--output_dir`: Directory to save benchmark results (default: "./benchmark_results")
- `--unsafe_label`: Label used by the classifier to identify unsafe content (default: "unsafe")
- `--api_key`: API key for LLM provider (if not in environment variables)

## Output

The benchmark creates a timestamped directory with the following:

- `benchmark_config.json`: Configuration used for the benchmark
- `detailed_results.json`: Detailed results for each test case
- `summary_report.json`: Summary metrics and statistics
- Various plots:
  - `confusion_matrix.png`: True/false positives and negatives
  - `roc_curve.png`: ROC curve for detection performance
  - `accuracy_by_category.png`: Detection accuracy by attack category
  - `accuracy_by_difficulty.png`: Detection accuracy by difficulty level
  - `processing_time_distribution.png`: Distribution of processing times

## Extending the Test Data

To add more test cases, modify the `data/test_data.py` file by adding entries to either `PROMPT_INJECTION_ATTACKS` or `LEGITIMATE_REQUESTS`. 