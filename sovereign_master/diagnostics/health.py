import os
from sovereign_master import ENGINE_NAME, __version__
def health(): return {"status": "ok", "engine": os.getenv("ENGINE_NAME", ENGINE_NAME), "version": os.getenv("ENGINE_VERSION", __version__)}
