from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, Field

from document_utils import format_docx, format_pdf, sanitize_text
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
    document_type: str = Field(..., min_length=1, max_length=200)
    parties: str = Field(..., min_length=1, max_length=5000)
    terms: str = Field(..., min_length=1, max_length=15000)
    dates: str = Field(..., min_length=1, max_length=500)


class DownloadRequest(BaseModel):
    document: str = Field(..., min_length=1, max_length=100000)
    document_type: str = Field(default="Legal Document", max_length=200)

@router.post("/generate")
def generate_document(request: DocumentRequest):
    values = {
        "document_type": request.document_type.strip(),
        "parties": request.parties.strip(),
        "terms": request.terms.strip(),
        "dates": request.dates.strip(),
    }
    if not all(values.values()):
        raise HTTPException(status_code=422, detail="All fields are required.")

    try:
        text = get_generator().generate_document(
            values["document_type"],
            values["parties"],
            values["terms"],
            values["dates"],
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


@router.post("/download/{file_type}")
def download_document(file_type: str, request: DownloadRequest):
    """Create a downloadable file without storing the legal document."""
    document = sanitize_text(request.document)
    title = request.document_type.strip() or "Legal Document"

    if file_type == "txt":
        content = document.encode("utf-8")
        media_type = "text/plain; charset=utf-8"
        filename = "legal_document.txt"
    elif file_type == "docx":
        content = format_docx(document, title)
        media_type = (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        filename = "legal_document.docx"
    elif file_type == "pdf":
        content = format_pdf(document, title)
        media_type = "application/pdf"
        filename = "legal_document.pdf"
    else:
        raise HTTPException(
            status_code=404, detail="Supported formats are txt, docx, and pdf."
        )

    return Response(
        content=content,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
