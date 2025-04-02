import os
from typing import List

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from proventra_core import GuardService, LLMSanitizer, TransformersAnalyzer

# Load environment variables from .env file, override existing ones
load_dotenv(override=True)

router = APIRouter()


class AnalyzeRequest(BaseModel):
    text: str


class BatchAnalyzeRequest(BaseModel):
    texts: List[str]


class RunPodRequest(BaseModel):
    input: dict


# Get configuration from environment
MODEL_NAME = os.getenv("CLASSIFICATION_MODEL_NAME")
if not MODEL_NAME:
    raise ValueError("CLASSIFICATION_MODEL_NAME environment variable must be set")

MODEL_UNSAFE_LABEL = os.getenv("CLASSIFICATION_MODEL_UNSAFE_LABEL", "unsafe")

# Get LLM configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "google")
print("Using LLM provider: {LLM_PROVIDER}")

LLM_MODEL_NAME = os.getenv(
    "LLM_MODEL_NAME", None
)  # Use provider's default if not specified
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))

# Get token limits
MAX_SANITIZATION_TOKENS = int(os.getenv("MAX_SANITIZATION_TOKENS", "4096"))

# Initialize the service once
service = GuardService(
    analyzer=TransformersAnalyzer(
        model_name=MODEL_NAME, unsafe_label=MODEL_UNSAFE_LABEL
    ),
    sanitizer=LLMSanitizer(
        provider=LLM_PROVIDER,
        model_name=LLM_MODEL_NAME,
        temperature=LLM_TEMPERATURE,
        max_tokens=MAX_SANITIZATION_TOKENS,
    ),
)


@router.get("/health")
async def health_check():
    return {"status": "healthy"}


@router.post("/analyze")
async def analyze_text(request: AnalyzeRequest):
    """
    Analyzes text for safety without sanitization.
    """
    try:
        result = service.analyze(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/batch")
async def analyze_texts(request: BatchAnalyzeRequest):
    """
    Analyzes multiple texts for safety without sanitization.
    """
    try:
        results = [service.analyze(text) for text in request.texts]
        return {"results": [{"unsafe": r.unsafe} for r in results]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-sanitize")
async def analyze_and_sanitize_text(request: AnalyzeRequest):
    """
    Analyzes text for safety and sanitizes it if unsafe.
    Returns the sanitized version if available and safe.
    """
    try:
        result = service.analyze_and_sanitize(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sanitize")
async def sanitize_text(request: AnalyzeRequest):
    """
    Only sanitizes the text without analysis, returning the full SanitizationResult.
    """
    try:
        # service.sanitize now returns a SanitizationResult object
        sanitization_result = service.sanitize(request.text)
        # Return the full result object, FastAPI will serialize it
        return sanitization_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/runpod-style-analyze-sanitize")
async def runpod_style_analyze_sanitize(request: RunPodRequest):
    """
    Mimics the RunPod API style taking in object with input and sanitize boolean.
    Returns an object wrapped in "output" key.
    """
    try:
        text = request.input.get("text")
        if not text:
            raise HTTPException(status_code=422, detail="No text provided for analysis")

        sanitize = request.input.get("sanitize", False)
        print("Sanitizing: {sanitize}")
        print("Text: {text}")

        if sanitize:
            result = service.analyze_and_sanitize(text)
            return {
                "output": {
                    "unsafe": result.unsafe,
                    "sanitized": result.sanitized,
                    "sanitization_details": {
                        "success": result.sanitization_details.success
                        if result.sanitization_details
                        else None,
                        "reason": result.sanitization_details.reason
                        if result.sanitization_details
                        else None,
                    }
                    if result.sanitization_details
                    else None,
                }
            }
        else:
            result = service.analyze(text)
            return {"output": {"unsafe": result.unsafe}}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
