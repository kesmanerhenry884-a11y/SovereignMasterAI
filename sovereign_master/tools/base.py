from abc import ABC, abstractmethod
class BaseTool(ABC):
    name = "tool"; description = ""; permissions = ()
    def validate(self, payload): return True
    @abstractmethod
    def execute(self, payload): raise NotImplementedError
