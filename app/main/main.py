import uvicorn
from .config.app import app

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info", reload=True)
