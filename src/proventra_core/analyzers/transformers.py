from typing import Any, Dict, Optional

from langchain.text_splitter import TokenTextSplitter
from transformers import pipeline

from .base import TextAnalyzer


class TransformersAnalyzer(TextAnalyzer):
    # Fixed chunk overlap for text splitting
    CHUNK_OVERLAP = 50

    def __init__(
        self,
        model_name: str,
        unsafe_label: str = "unsafe",
        max_analysis_tokens: Optional[int] = None,
    ):
        """
        Initialize the analyzer.

        Args:
            model_name: HuggingFace model name for classification
            unsafe_label: Label used to identify unsafe content
            max_analysis_tokens: Optional override for maximum tokens per chunk
        """
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

    def _analyze_single_chunk(self, chunk: str) -> bool:
        """Analyzes a single chunk of text and returns if it's unsafe."""
        try:
            result = self.classifier(chunk)[0]
            is_unsafe = bool(result["label"] == self.unsafe_label)
            return is_unsafe
        except Exception as e:
            print(f"Error in model inference for chunk: {str(e)}")
            return True  # Treat inference errors as unsafe

    def analyze(self, text: str) -> Dict[str, Any]:
        """Analyzes text, splitting into chunks if it exceeds max_tokens."""
        chunks = self._text_splitter.split_text(text)

        if len(chunks) == 1:
            # If only one chunk (or less than max tokens), analyze directly
            is_unsafe = self._analyze_single_chunk(chunks[0])
            return {"unsafe": is_unsafe}
        else:
            print(
                f"Input text too long, splitting into {len(chunks)} chunks for analysis."
            )
            results = [self._analyze_single_chunk(chunk) for chunk in chunks]

            # If any chunk is unsafe, the whole text is unsafe
            overall_unsafe = any(results)
            print(f"Chunk analysis results: Unsafe={overall_unsafe}")
            return {"unsafe": overall_unsafe}
