# Advanced Usage

This guide covers more advanced use cases for ProventraCore.

## Custom Analyzers

You can create custom analyzers by implementing the `TextAnalyzer` interface:

```python
from proventra_core import TextAnalyzer
from typing import Dict, Any

class KeywordAnalyzer(TextAnalyzer):
    def __init__(self, keywords=None):
        self.keywords = keywords or ["hack", "ignore", "system"]
        self._max_tokens = 1024
        
    def analyze(self, text: str) -> Dict[str, Any]:
        # Check if any keyword is in the text
        unsafe = any(keyword in text.lower() for keyword in self.keywords)
        
        return {
            "unsafe": unsafe,
            "matched_keywords": [word for word in self.keywords if word in text.lower()]
        }
        
    @property
    def max_tokens(self) -> int:
        return self._max_tokens
        
    @property
    def chunk_overlap(self) -> int:
        return 50
```

## Custom Sanitizers

You can implement your own sanitization logic:

```python
from proventra_core import TextSanitizer
from proventra_core.sanitizers.results import SanitizationResult

class ReplacementSanitizer(TextSanitizer):
    def __init__(self, replacements=None):
        self.replacements = replacements or {
            "hack": "[REMOVED]",
            "ignore": "[REMOVED]",
            "system": "[REMOVED]"
        }
        
    def sanitize(self, text: str) -> SanitizationResult:
        sanitized_text = text
        for word, replacement in self.replacements.items():
            sanitized_text = sanitized_text.replace(word, replacement)
            
        return SanitizationResult(
            sanitized=sanitized_text,
            modified=(sanitized_text != text)
        )
```