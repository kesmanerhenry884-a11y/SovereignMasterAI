from dataclasses import dataclass, field

@dataclass
class TaskPlan:
    category: str
    modules: list[str] = field(default_factory=list)
    steps: list[str] = field(default_factory=list)

class Planner:
    def create(self, category: str, mode: str = "general") -> TaskPlan:
        modules = ["language"]
        if category == "reasoning": modules += ["reasoning", "verification"]
        elif category == "spiritual" or mode == "spiritual": modules += ["spiritual", "verification"]
        elif category == "math": modules += ["reasoning", "verification"]
        elif category in {"coding", "research", "documents", "data"}: modules += [category, "verification"]
        return TaskPlan(category, modules, ["classify", "execute", "verify", "respond"])
