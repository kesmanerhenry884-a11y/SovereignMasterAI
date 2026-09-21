"""
Sovereign Master AI
Main application entry point.

PROPHÈTE KESMANER HENRY
"""

import os

from dotenv import load_dotenv
import uvicorn

from api.routes import app


# Load local development values while keeping deployment-platform variables authoritative.
load_dotenv()


def main() -> None:
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))

    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level=os.getenv("LOG_LEVEL", "info").lower(),
    )


if __name__ == "__main__":
    main()
