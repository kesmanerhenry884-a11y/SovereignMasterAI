from dataclasses import asdict
from typing import Any

from .provider import GenerationResult


# ... existing imports and class body are intentionally represented by the
# concrete implementation below so legacy string providers and modern result
# providers can coexist.
from .context import RequestContext
