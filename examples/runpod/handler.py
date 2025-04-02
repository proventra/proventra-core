import os

import runpod
from dotenv import load_dotenv

from proventra_core import GuardService, LLMSanitizer, TransformersAnalyzer

# Load environment variables from .env file, override existing ones
load_dotenv(override=True)


def init_service():
    """Initialize the guard service with our implementations"""
    # Get classification model configuration
    model_name = os.getenv("CLASSIFICATION_MODEL_NAME")
    if not model_name:
        raise ValueError("CLASSIFICATION_MODEL_NAME environment variable must be set")

    # Get LLM configuration
    llm_provider = os.getenv("LLM_PROVIDER", "google")
    llm_model_name = os.getenv(
        "LLM_MODEL_NAME", None
    )  # Use provider's default if not specified
    llm_temperature = float(os.getenv("LLM_TEMPERATURE", "0.1"))

    # Get token limits
    max_sanitization_tokens = int(os.getenv("MAX_SANITIZATION_TOKENS", "4096"))

    analyzer = TransformersAnalyzer(
        model_name=model_name,
        unsafe_label=os.getenv("CLASSIFICATION_MODEL_UNSAFE_LABEL", "unsafe"),
    )

    sanitizer = LLMSanitizer(
        provider=llm_provider,
        model_name=llm_model_name,
        temperature=llm_temperature,
        max_tokens=max_sanitization_tokens,
    )

    return GuardService(analyzer, sanitizer)


def handler(event):
    """Handle incoming requests"""
    global service

    # Initialize service if not already done
    if "service" not in globals():
        service = init_service()

    # Get input parameters
    input_data = event.get("input", {})
    text = input_data.get("text")
    should_sanitize = input_data.get("sanitize", False)  # Default to False

    # Validate input
    if not text:
        return {"error": "No text provided for analysis."}

    try:
        if should_sanitize:
            # Full analysis with sanitization
            result = service.analyze_and_sanitize(text)
            details_dict = None
            if result.sanitization_details:
                details_dict = {
                    "success": result.sanitization_details.success,
                    "reason": result.sanitization_details.reason,
                    # Note: sanitized_text is already top-level if successful
                }

            return {
                "unsafe": result.unsafe,
                "sanitized": result.sanitized,  # The final sanitized text (if safe)
                "sanitization_details": details_dict,  # Include the details object
            }
        else:
            # Analysis only
            result = service.analyze(text)
            return {"unsafe": result.unsafe}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    # Start the serverless worker
    runpod.serverless.start({"handler": handler})
