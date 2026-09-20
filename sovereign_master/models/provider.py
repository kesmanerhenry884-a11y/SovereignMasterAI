from abc import ABC, abstractmethod
class BaseModelProvider(ABC):
    name = "base"
    @abstractmethod
    def generate(self, prompt: str, context: dict | None = None) -> str: raise NotImplementedError
    def stream(self, prompt, context=None): yield self.generate(prompt, context)
    def health(self): return {"available": False, "provider": self.name}
