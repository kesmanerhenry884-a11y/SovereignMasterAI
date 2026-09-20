class ModelRegistry:
    def __init__(self): self.providers = {}
    def register(self, provider): self.providers[provider.name] = provider
    def default(self): return next(iter(self.providers.values()), None)
    def health(self): return {name: provider.health() for name, provider in self.providers.items()}
