import os

from dotenv import load_dotenv
import uvicorn

from api.routes import app


load_dotenv()


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host=host, port=port)
