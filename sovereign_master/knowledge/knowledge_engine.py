from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
@dataclass
class Knowledge:
    source: str; content: str; domain: str = "general"; reliability: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: dict[str, Any] = field(default_factory=dict)
class KnowledgeEngine:
    def __init__(self): self.items: list[Knowledge] = []
    def add(self, item: Knowledge): self.items.append(item)
    def search(self, query: str) -> list[Knowledge]: return [i for i in self.items if query.lower() in i.content.lower()]
