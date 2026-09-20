class ReasoningEngine:
    def decompose(self, task: str) -> list[str]: return [task]
    def compare(self, options: list[str]) -> dict: return {"options": options, "conclusion": "Comparison requires configured evidence."}
    def solve(self, task: str) -> dict: return {"task": task, "conclusion": "No reasoning model is configured."}
