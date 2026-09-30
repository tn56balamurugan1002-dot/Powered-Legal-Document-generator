# LegalEase: AI-Powered Legal Document Generator

FastAPI web application for AI-assisted drafting of contracts, agreements,
NDAs, and similar documents using Google's Gemini API. The Vercel deployment
serves both the responsive browser interface and API from one project.

## Setup
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
Copy `env.example` to `.env` and add your real `GEMINI_API_KEY`. Never upload `.env`.

## Run backend
From the repository root:
```powershell
uvicorn main:app --reload
```
Open http://127.0.0.1:8000/docs

## Run frontend
In a second terminal:
```powershell
streamlit run app.py
```

## Deployment

This project contains:

- `main.py` — the FastAPI application and built-in Vercel web interface.
- `app.py` — an optional Streamlit frontend for local use or Streamlit Cloud.

The included `pyproject.toml` tells Vercel to use `main.py` as the application
entrypoint. After deploying, add `GEMINI_API_KEY` and optionally `GEMINI_MODEL`
in the Vercel project environment variables, then redeploy. Open the project
domain for the web interface and verify the API at:

```text
https://YOUR-VERCEL-DOMAIN/health
```

If `GEMINI_API_KEY` is not configured, the application remains usable in
template mode. It creates a structured, editable draft from the supplied
details and clearly labels the output as template-based. When a key is
configured, generation automatically uses Gemini.

If you prefer the optional Streamlit frontend, deploy `app.py` separately with
Streamlit Community Cloud. Set `BACKEND_URL` in Streamlit secrets to the
deployed Vercel URL:

```toml
BACKEND_URL = "https://YOUR-VERCEL-DOMAIN"
```

## Structure
- `main.py` - FastAPI application
- `index.html` - responsive web interface served by FastAPI
- `routes.py` - `/generate` endpoint
- `gemini_generator.py` - Gemini integration
- `app.py` - Streamlit UI
- `document_utils.py` - TXT/DOCX/PDF utilities

## Note
Generated content is an AI-assisted draft and should be reviewed by a qualified legal professional before use. Check Google's current Gemini API documentation for model/API changes before deployment.
