class ResearchEngine:
    def __init__(self, provider=None): self.provider=provider
    def search(self, query):
        if not self.provider: return {"available":False,"results":[],"warning":"Aucun fournisseur de recherche configuré."}
        return self.provider.search(query)
