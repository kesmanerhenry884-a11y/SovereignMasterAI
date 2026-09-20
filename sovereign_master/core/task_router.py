class TaskRouter:
    CATEGORIES = ("general", "reasoning", "math", "coding", "research", "translation", "language", "documents", "data", "vision", "voice", "spiritual", "education")
    KEYWORDS = {
        "math": ("calculate", "math", "equation", "calcul", "mathématique"),
        "coding": ("code", "python", "bug", "program", "api", "fonction"),
        "research": ("research", "source", "recherche", "compare", "actualité"),
        "translation": ("translate", "traduire", "translation", "traduis"),
        "spiritual": ("bible", "prayer", "prière", "god", "dieu", "spiritual", "proph"),
        "education": ("learn", "explain", "apprendre", "explique", "cours"),
        "documents": ("document", "pdf", "résume", "resume"),
        "data": ("data", "csv", "statistics", "statistique"),
        "reasoning": ("why", "solve", "logic", "pourquoi", "résous"),
    }
    def register(self, category: str, keywords: tuple[str, ...]):
        self.CATEGORIES = tuple(dict.fromkeys((*self.CATEGORIES, category)))
        self.KEYWORDS[category] = keywords
    def classify(self, message: str) -> str:
        text = message.lower()
        for category, words in self.KEYWORDS.items():
            if any(word in text for word in words): return category
        return "general"
