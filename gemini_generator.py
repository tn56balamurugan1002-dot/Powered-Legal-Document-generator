import os
import re
from dotenv import load_dotenv
load_dotenv()

class GeminiDocumentGenerator:
    def __init__(self):
        self.api_key=os.getenv("GEMINI_API_KEY")
        self.model_name=os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.client = None
        self.mode = "template"
        if not self.api_key:
            return
        try:
            from google import genai
        except ImportError as exc:
            raise RuntimeError("Install google-genai with: pip install google-genai") from exc
        self.client=genai.Client(api_key=self.api_key)
        self.mode = "gemini"

    def generate_document(self, document_type, parties, terms, dates):
        if self.client is None:
            return self.generate_template(document_type, parties, terms, dates)

        prompt=f"""Draft a clear legal-document draft based only on these inputs. Do not invent facts, laws, dates, or values.

Document type: {document_type}
Parties: {parties}
Terms: {terms}
Effective dates: {dates}

Use a professional structure with title, parties, purpose, definitions where useful, terms, effective date/duration, relevant clauses, and signature section. State that it is an AI-assisted draft requiring legal review."""
        response=self.client.models.generate_content(model=self.model_name, contents=prompt)
        return (response.text or "").strip()

    @staticmethod
    def generate_template(document_type, parties, terms, dates):
        """Create a deterministic draft when Gemini is not configured."""
        clauses = [
            item.strip(" \t-•")
            for item in re.split(r"[;\n]+", terms)
            if item.strip(" \t-•")
        ]
        if not clauses:
            clauses = [terms.strip()]

        numbered_terms = "\n\n".join(
            f"{index}. {clause}" for index, clause in enumerate(clauses, start=1)
        )

        return f"""{document_type.upper()}

TEMPLATE-BASED DRAFT — LEGAL REVIEW REQUIRED

1. PARTIES
This document is entered into by the following parties:
{parties}

2. PURPOSE
The parties wish to record the terms described in this document. This draft is based only on the information supplied by the user and does not add unstated facts or legal requirements.

3. AGREED TERMS
{numbered_terms}

4. EFFECTIVE DATE
This document is intended to take effect on: {dates}

5. AMENDMENTS
Any amendment should be recorded in writing and accepted by all affected parties.

6. ENTIRE UNDERSTANDING
This document records the parties' stated understanding about the matters described above. Any attachments or additional terms should be reviewed and incorporated before signing.

7. SIGNATURES

Party name: ______________________________
Signature: _______________________________
Date: ___________________________________

Party name: ______________________________
Signature: _______________________________
Date: ___________________________________

NOTICE
This is a template-based draft, not AI-generated legal advice. It should be reviewed and adapted by a qualified legal professional before use."""
