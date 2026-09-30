from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from gemini_generator import GeminiDocumentGenerator

router = APIRouter()
generator = None


def get_generator():
    """Create the Gemini client only when a document is requested.

    Keeping this lazy means the API can still start and expose /health when
    GEMINI_API_KEY has not been configured yet.
    """
    global generator
    if generator is None:
        generator = GeminiDocumentGenerator()
    return generator

class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=1)
    parties: str = Field(..., min_length=1)
    terms: str = Field(..., min_length=1)
    dates: str = Field(..., min_length=1)

@router.post("/generate")
def generate_document(request: DocumentRequest):
    try:
        text = get_generator().generate_document(
            request.document_type,
            request.parties,
            request.terms,
            request.dates,
        )
        if not text:
            raise HTTPException(
                status_code=502,
                detail="The Gemini API returned an empty document.",
            )
        return {"status":"success", "document":text}
    except HTTPException:
        raise
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Document generation failed: {exc}",
        ) from exc
