class ToolRegistry:
    def __init__(self): self.tools = {}
    def register(self, tool): self.tools[tool.name] = tool
    def get(self, name): return self.tools.get(name)
    def list(self): return [{"name": t.name, "description": t.description, "permissions": list(t.permissions)} for t in self.tools.values()]
