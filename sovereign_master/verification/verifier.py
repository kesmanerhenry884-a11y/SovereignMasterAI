class VerificationEngine:
    def verify(self, answer: str, category: str) -> dict:
        return {"verified": False, "confidence": 0.0, "warnings": ["Réponse non vérifiée par une source externe."]}
