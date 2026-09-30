# LegalEase: AI-Powered Legal Document Generator

Streamlit + FastAPI application for AI-assisted drafting of contracts, agreements, NDAs and similar documents using Google's Gemini API.

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

This project contains two different applications:

- `main.py` is the FastAPI backend.
- `app.py` is the Streamlit frontend.

Do not deploy `app.py` as a Vercel Function. Vercel runs short-lived Python
Functions, while Streamlit needs its own server process. The included
`pyproject.toml` tells Vercel to use `main.py` as the backend entrypoint.
After deploying the backend to Vercel, add `GEMINI_API_KEY` and
`GEMINI_MODEL` in the Vercel project environment variables. Verify it at:

```text
https://YOUR-VERCEL-DOMAIN/health
```

Deploy the Streamlit frontend separately using Streamlit Community Cloud. Set
`BACKEND_URL` in the app's Streamlit secrets to the deployed backend URL, for
example:

```toml
BACKEND_URL = "https://YOUR-VERCEL-DOMAIN"
```

## Structure
- `main.py` - FastAPI application
- `routes.py` - `/generate` endpoint
- `gemini_generator.py` - Gemini integration
- `app.py` - Streamlit UI
- `document_utils.py` - TXT/DOCX/PDF utilities

## Note
Generated content is an AI-assisted draft and should be reviewed by a qualified legal professional before use. Check Google's current Gemini API documentation for model/API changes before deployment.
