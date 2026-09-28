from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()
generator = GeminiDocumentGenerator()

class DocumentRequest(BaseModel):
    document_type: str
    parties: str
    terms: str
    dates: str

@router.post("/generate")
def generate_document(request: DocumentRequest):
    try:
        text = generator.generate_document(request.document_type, request.parties, request.terms, request.dates)
        return {"status":"success", "document":text}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
