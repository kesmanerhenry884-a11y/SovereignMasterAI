from dataclasses import dataclass
from typing import Any
@dataclass
class KnowledgeRecord:
    source: str
    content: str
    domain: str="general"
    reliability: float=0.0
    metadata: dict[str,Any]|None=None
class KnowledgeEngine:
    def __init__(self): self.records=[]
    def add(self, record): self.records.append(record)
    def retrieve(self, query): return [r for r in self.records if query.lower() in r.content.lower()]
