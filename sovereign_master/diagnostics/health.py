import os

from sovereign_master import ENGINE_NAME, __version__


def health():
    return {
        "status": "ok",
        "engine": os.getenv("APP_NAME", os.getenv("ENGINE_NAME", ENGINE_NAME)),
        "version": os.getenv("APP_VERSION", os.getenv("ENGINE_VERSION", __version__)),
    }


class HealthService:
    """Small compatibility service for API and future health checks."""

    def check(self):
        return health()
