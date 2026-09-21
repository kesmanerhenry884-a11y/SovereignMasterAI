from sovereign_master.media import BaseMediaProvider, MediaResult

class MediaPipeline:
    def __init__(self, provider=None, watermark="PROPHÈTE KESMANER HENRY"):
        self.provider = provider
        self.watermark = watermark
    def run(self, request):
        if not self.provider:
            return MediaResult(False, request.get("media_type", "unknown"), status="provider_unavailable", warnings=["Media generation is not configured."])
        return self.provider.generate({**request, "watermark": self.watermark})
