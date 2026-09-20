from dataclasses import dataclass, field
@dataclass
class TaskPlan:
    category: str
    modules: list[str] = field(default_factory=list)
    steps: list[str] = field(default_factory=list)
class Planner:
    def create(self, category, mode="general"):
        modules=["language"]
        if category in {"reasoning","math"}: modules += ["reasoning","verification"]
        if category == "research": modules += ["research","knowledge","verification"]
        if mode == "spiritual" or category == "spiritual": modules += ["spiritual","verification"]
        return TaskPlan(category, list(dict.fromkeys(modules)), ["classify","plan","execute","verify","respond"])
