import os
from dotenv import load_dotenv
load_dotenv()

class GeminiDocumentGenerator:
    def __init__(self):
        self.api_key=os.getenv("GEMINI_API_KEY")
        self.model_name=os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured. Create .env from .env.example.")
        try:
            from google import genai
        except ImportError as exc:
            raise RuntimeError("Install google-genai with: pip install google-genai") from exc
        self.client=genai.Client(api_key=self.api_key)

    def generate_document(self, document_type, parties, terms, dates):
        prompt=f"""Draft a clear legal-document draft based only on these inputs. Do not invent facts, laws, dates, or values.

Document type: {document_type}
Parties: {parties}
Terms: {terms}
Effective dates: {dates}

Use a professional structure with title, parties, purpose, definitions where useful, terms, effective date/duration, relevant clauses, and signature section. State that it is an AI-assisted draft requiring legal review."""
        response=self.client.models.generate_content(model=self.model_name, contents=prompt)
        return (response.text or "").strip()
