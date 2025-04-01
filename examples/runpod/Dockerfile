FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy package files
COPY pyproject.toml .
COPY LICENSE .
COPY README.md .
COPY src/ src/
COPY examples/runpod/ runpod/

# Install package with RunPod extras and all LLM providers
RUN pip install -e ".[runpod,all]"

# Start the handler
CMD [ "python", "-u", "runpod/handler.py" ] 