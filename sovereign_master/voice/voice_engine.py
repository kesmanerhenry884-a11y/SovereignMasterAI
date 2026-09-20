import os
class VoiceEngine:
    def enabled(self): return os.getenv("VOICE_ENABLED", "false").lower() == "true"
    def speech_to_text(self, audio): raise NotImplementedError("Voice provider not configured")
    def text_to_speech(self, text): raise NotImplementedError("Voice provider not configured")
    def voice_profile(self): return {"enabled": self.enabled(), "provider": os.getenv("VOICE_PROVIDER", "")}
