from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from routes import router

app = FastAPI(title="LegalEase API", description="AI-Powered Legal Document Generator", version="1.0.0")
INDEX_FILE = Path(__file__).with_name("index.html")

@app.get("/")
def home():
    """Serve the browser UI from the same Vercel deployment as the API."""
    return HTMLResponse(INDEX_FILE.read_text(encoding="utf-8"))

@app.get("/health")
def health(): return {"status": "success"}

app.include_router(router)
