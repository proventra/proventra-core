# Deployment

This guide explains how to deploy ProventraCore in different environments.

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
