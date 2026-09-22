"""Planner and task routing primitives used by the orchestration engine."""
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class TaskRoute:
    name: str
    priority: int
    requires_model: bool = True
    requires_retrieval: bool = False
    requires_media: bool = False


@dataclass
class TaskPlan:
    category: str
    modules: list[str] = field(default_factory=list)
    steps: list[str] = field(default_factory=list)
    route: Any = None


ExecutionPlan = TaskPlan


class TaskRouter:
    categories = (
        "general", "reasoning", "math", "coding", "research", "translation",
        "language", "documents", "data", "vision", "voice", "spiritual", "education",
        "media", "knowledge",
    )

    keywords = {
        "math": ("calculate", "math", "equation", "calcul"),
        "coding": ("code", "python", "bug", "api", "program"),
        "research": ("research", "source", "sources", "recherche", "verify", "vérifie", "latest", "actuel"),
        "translation": ("translate", "traduire", "traduis"),
        "documents": ("document", "pdf", "fichier", "file"),
        "spiritual": ("spiritual", "spirituel", "prophet", "prophète", "prophecy", "vision"),
        "vision": ("vision", "camera", "caméra", "image", "photo", "picture"),
        "voice": ("voice", "audio", "speech", "mic", "microphone"),
        "education": ("learn", "teach", "education", "apprendre", "enseigne"),
    }

    def register(self, category: str, words: tuple[str, ...] | list[str]) -> None:
        self.keywords[category] = tuple(words)

    def classify(self, message: str) -> str:
        text = (message or "").lower()
        for category, words in self.keywords.items():
            if any(word in text for word in words):
                return category
        return "general"

    def route(self, message: str) -> TaskRoute:
        text = (message or "").lower()
        if any(word in text for word in ("image", "photo", "picture", "video", "camera", "caméra", "foto", "vidéo")):
            return TaskRoute("media", 90, requires_media=True)
        if any(word in text for word in ("research", "source", "sources", "recherche", "verify", "vérifie", "latest", "actuel")):
            return TaskRoute("research", 80, requires_retrieval=True)
        if any(word in text for word in ("document", "pdf", "knowledge", "connaissance", "fichier")):
            return TaskRoute("knowledge", 70, requires_retrieval=True)
        category = self.classify(message)
        return TaskRoute(category, 50)


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
