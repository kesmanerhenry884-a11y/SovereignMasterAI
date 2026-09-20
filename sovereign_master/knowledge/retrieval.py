class Retrieval:
    def search(self, items, query): return [item for item in items if query.lower() in item.content.lower()]
