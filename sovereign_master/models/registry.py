import os
from .provider import BaseModelProvider, ProviderFactory
class ModelRegistry:
    def __init__(self, providers=None):
        self.providers = providers or {}
        if not self.providers: self.register(ProviderFactory.create_from_environment())
    def register(self, provider: BaseModelProvider): self.providers[provider.name] = provider
    def get(self, name=None):
        name = name or os.getenv("MODEL_PROVIDER", "")
        return self.providers.get(name) or next(iter(self.providers.values()), None)
    def health(self): return {name: provider.health() for name, provider in self.providers.items()}
    def metadata(self): return {name: provider.metadata() for name, provider in self.providers.items()}
