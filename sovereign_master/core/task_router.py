from dataclasses import dataclass


@dataclass(frozen=True)
class TaskRoute:
    name: str
    priority: int
    requires_model: bool = True
    requires_retrieval: bool = False
    requires_media: bool = False


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
        "spiritual": ("spiritual", "spirituel", "prophet", "prophète", "prophecy"),
        "vision": ("vision", "camera", "caméra", "image", "photo", "picture"),
        "voice": ("voice", "audio", "speech", "mic", "microphone", "vwa"),
        "education": ("learn", "teach", "education", "apprendre", "enseigne"),
    }

    def register(self, category: str, words: tuple[str, ...] | list[str]) -> None:
        self.keywords[category] = tuple(words)

    def classify(self, message: str) -> str:
        text = (message or "").casefold()
        for category, words in self.keywords.items():
            if any(word.casefold() in text for word in words):
                return category
        return "general"

    def route(self, message: str) -> TaskRoute:
        text = (message or "").casefold()
        if any(word in text for word in ("image", "photo", "picture", "video", "camera", "caméra", "foto", "vidéo", "imaj")):
            return TaskRoute("media", 90, requires_media=True)
        if any(word in text for word in ("research", "source", "sources", "recherche", "verify", "vérifie", "latest", "actuel")):
            return TaskRoute("research", 80, requires_retrieval=True)
        if any(word in text for word in ("document", "pdf", "knowledge", "connaissance", "fichier")):
            return TaskRoute("knowledge", 70, requires_retrieval=True)
        return TaskRoute(self.classify(message), 50)
