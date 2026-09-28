# LegalEase: AI-Powered Legal Document Generator

Streamlit + FastAPI application for AI-assisted drafting of contracts, agreements, NDAs and similar documents using Google's Gemini API.

## Setup
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
Copy `.env.example` to `.env` and add your real `GEMINI_API_KEY`. Never upload `.env`.

## Run backend
```powershell
cd backend
uvicorn main:app --reload
```
Open http://127.0.0.1:8000/docs

## Run frontend
In a second terminal:
```powershell
cd frontend
streamlit run app.py
```

## Structure
- `backend/main.py` - FastAPI application
- `backend/routes.py` - `/generate` endpoint
- `backend/ai_core/gemini_generator.py` - Gemini integration
- `frontend/app.py` - Streamlit UI
- `frontend/document_utils.py` - TXT/DOCX/PDF utilities

## Note
Generated content is an AI-assisted draft and should be reviewed by a qualified legal professional before use. Check Google's current Gemini API documentation for model/API changes before deployment.
