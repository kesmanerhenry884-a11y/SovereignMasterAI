from .confidence import EvidenceStatus, VerificationResult
class VerificationEngine:
    def verify(self, answer, category):
        status=EvidenceStatus.INTERPRETATION.value if category=="spiritual" else EvidenceStatus.UNCERTAIN.value
        return VerificationResult(status,0.0,["Aucune vérification externe effectuée; ne pas traiter cette réponse comme un fait vérifié."])
