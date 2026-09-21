from dataclasses import dataclass, field
from typing import Any


@dataclass
class TaskPlan:
    category: str
    modules: list[str] = field(default_factory=list)
    steps: list[str] = field(default_factory=list)
    route: Any = None


# New public name used by the modern orchestration API.
ExecutionPlan = TaskPlan


class Planner:
    def create(self, category: str, mode: str = "general") -> TaskPlan:
        modules = ["language"]
        if category in {"reasoning", "math", "coding"}:
            modules += ["reasoning", "verification"]
        if category in {"research", "knowledge", "documents"}:
            modules += ["research", "knowledge", "verification"]
        if category in {"media", "vision", "voice"}:
            modules += [category, "safety"]
        if mode == "spiritual" or category == "spiritual":
            modules += ["spiritual", "verification"]
        return TaskPlan(category, list(dict.fromkeys(modules)), ["classify", "plan", "execute", "verify", "respond"])

    def create_plan(self, context, route) -> TaskPlan:
        plan = self.create(route.name, context.mode)
        plan.route = route
        return plan
