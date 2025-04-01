# Deployment

This guide explains how to deploy ProventraCore in different environments.

## Environment Variables

While ProventraCore can be configured directly through constructor parameters, you can also use environment variables for convenience:

```bash
# Classification model
CLASSIFICATION_MODEL_NAME=path/to/model
CLASSIFICATION_MODEL_UNSAFE_LABEL=unsafe

# LLM Provider settings
LLM_PROVIDER=google  # Options: google, openai, anthropic, mistral
LLM_MODEL_NAME=gemini-2.0-flash
LLM_TEMPERATURE=0.1

# Token limits
MAX_SANITIZATION_TOKENS=4096

# API Keys (required for LLM providers)
# Use the one matching your LLM_PROVIDER
GOOGLE_API_KEY=your-google-api-key
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
MISTRAL_API_KEY=your-mistral-api-key
```

Save these in a `.env` file in your project root.

## FastAPI Server

The repository includes an example FastAPI server:

1. Install dependencies:
   ```bash
   cd examples/api
   pip install -e "../../[api,all]"
   ```

2. Set up environment:
   ```bash
   # Copy example env file
   cp ../../.env.example .env
   
   # Edit .env and add your API key
   nano .env
   ```

3. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

4. Access the API at `http://localhost:8000`

## RunPod Serverless

Deploy on RunPod serverless platform:

1. Install dependencies:
   ```bash
   cd examples/runpod
   pip install -e "../../[runpod,all]"
   ```

2. Set up your RunPod account and follow their [deployment guidelines](https://docs.runpod.io)
