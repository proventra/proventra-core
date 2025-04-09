from typing import Any, Dict, Optional

from langchain.text_splitter import TokenTextSplitter
from transformers import pipeline

from .base import TextAnalyzer


class TransformersAnalyzer(TextAnalyzer):
    # Fixed chunk overlap for text splitting
    CHUNK_OVERLAP = 50

    def __init__(
        self,
        model_name: str = "proventra/mdeberta-v3-base-prompt-injection",
        unsafe_label: str = "INJECTION",
        max_analysis_tokens: Optional[int] = None,
        threshold: float = 0.5,
    ):
        """
        Initialize the analyzer.

        Args:
            model_name: HuggingFace model name for classification (default: proventra/mdeberta-v3-base-prompt-injection)
            unsafe_label: Label used to identify unsafe content (default: INJECTION)
            max_analysis_tokens: Optional override for maximum tokens per chunk
            threshold: Risk score threshold for unsafe classification (0 to 1)
        """
        super().__init__(threshold)
        self.classifier = pipeline("text-classification", model=model_name)
        self.unsafe_label = unsafe_label

        # Get max sequence length from model config
        try:
            model_max_length = self.classifier.model.config.max_position_embeddings
            print(f"Detected model max sequence length: {model_max_length}")
            self._max_tokens = max_analysis_tokens or model_max_length
        except AttributeError:
            print(
                f"Could not detect model max sequence length, using default or provided value: {max_analysis_tokens or 1024}"
            )
            self._max_tokens = max_analysis_tokens or 1024

        self._text_splitter = TokenTextSplitter(
            chunk_size=self._max_tokens,
            chunk_overlap=self.CHUNK_OVERLAP,
            encoding_name="cl100k_base",
        )
        print(
            f"Analyzer initialized. Max analysis tokens per chunk: {self._max_tokens}"
        )

    @property
    def max_tokens(self) -> int:
        return self._max_tokens

    @property
    def chunk_overlap(self) -> int:
        return self.CHUNK_OVERLAP

    def _analyze_single_chunk(self, chunk: str) -> tuple[bool, float]:
        """Analyzes a single chunk of text and returns if it's unsafe and the risk score."""
        try:
            result = self.classifier(chunk)[0]
            is_unsafe = bool(result["label"] == self.unsafe_label)
            confidence = result["score"]

            # Calculate risk score:
            # - For unsafe predictions: higher confidence means higher risk
            # - For safe predictions: lower confidence means higher risk
            # - Low confidence predictions (< 0.5) are considered more risky
            if is_unsafe:
                # Unsafe with high confidence -> high risk (0.5 to 1.0)
                # Unsafe with low confidence -> medium risk (0.5 to 0.75)
                score = 0.5 + (confidence / 2)
            else:
                # Safe with high confidence -> low risk (0.0 to 0.25)
                # Safe with low confidence -> medium risk (0.25 to 0.5)
                score = 0.5 - (confidence / 2)

            return is_unsafe, score
        except Exception as e:
            print(f"Error in model inference for chunk: {str(e)}")
            return True, 1.0  # Treat inference errors as maximum risk

    def analyze(self, text: str) -> Dict[str, Any]:
        """Analyzes text, splitting into chunks if it exceeds max_tokens."""
        chunks = self._text_splitter.split_text(text)

        if len(chunks) == 1:
            # If only one chunk (or less than max tokens), analyze directly
            is_unsafe, score = self._analyze_single_chunk(chunks[0])
            return {"unsafe": score >= self.threshold, "risk_score": round(score, 3)}
        else:
            print(
                f"Input text too long, splitting into {len(chunks)} chunks for analysis."
            )
            results = [self._analyze_single_chunk(chunk) for chunk in chunks]

            # Take the maximum risk score across all chunks
            max_score = round(max(score for _, score in results), 3)
            print(f"Chunk analysis results: Risk score={max_score}")
            return {"unsafe": max_score >= self.threshold, "risk_score": max_score}
