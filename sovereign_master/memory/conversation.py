class ConversationMemory:
    def __init__(self): self.messages = []
    def append(self, role, content): self.messages.append({"role": role, "content": content})
