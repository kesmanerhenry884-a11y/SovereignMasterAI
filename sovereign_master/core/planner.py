from dataclasses import dataclass
from typing import Any


@dataclass
class TaskPlan:
    category: str
    modules: list[str]
    steps: list[str]
    route: Any = None


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
        if category == "location":
            modules += ["location", "safety"]
        if mode == "spiritual" or category == "spiritual":
            modules += ["spiritual", "verification"]
        return TaskPlan(
            category=category,
            modules=list(dict.fromkeys(modules)),
            steps=["classify", "plan", "execute", "verify", "respond"],
        )

    def create_plan(self, context, route) -> TaskPlan:
        plan = self.create(route.name, context.mode)
        plan.route = route
        return plan
