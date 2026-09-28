import html, os, requests, streamlit as st
from dotenv import load_dotenv
from document_utils import sanitize_text, format_docx, format_pdf
load_dotenv()
API_URL=os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="wide")
st.markdown("""<style>.title{text-align:center;font-size:42px;font-weight:700}.subtitle{text-align:center;color:#777}.preview{background:#1e1e1e;color:#f5f5f5;padding:25px;border-radius:12px;height:520px;overflow-y:auto;line-height:1.7;white-space:pre-wrap}</style>""", unsafe_allow_html=True)
c1,c2,c3=st.columns([1,2,1])
with c2:
    if os.path.exists("logo.png"): st.image("logo.png", width=140)
st.markdown('<div class="title">LegalEase</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-Powered Legal Document Generator</div>', unsafe_allow_html=True)
document_type=st.text_input("Document Type", placeholder="Example: Freelance Work Contract")
parties=st.text_area("Parties Involved", placeholder="Example: Jane Doe (Service Provider), TechNova Inc. (Client)")
terms=st.text_area("Terms & Conditions", placeholder="Separate clauses with semicolons (;)")
dates=st.text_input("Effective Date", placeholder="Example: 01-10-2026")
if "document" not in st.session_state: st.session_state.document=""
if "edit_mode" not in st.session_state: st.session_state.edit_mode=False
if st.button("Generate Document", type="primary", use_container_width=True):
    if not all([document_type.strip(), parties.strip(), terms.strip(), dates.strip()]): st.warning("Please fill in all required fields.")
    else:
        try:
            r=requests.post(f"{API_URL}/generate", json={"document_type":document_type,"parties":parties,"terms":terms,"dates":dates}, timeout=120)
            r.raise_for_status(); st.session_state.document=sanitize_text(r.json()["document"]); st.session_state.edit_mode=False
        except requests.RequestException as e: st.error(f"Backend request failed: {e}")
if st.session_state.document:
    st.subheader("Document Preview")
    if st.button("Click to Edit Document"): st.session_state.edit_mode=True
    if st.session_state.edit_mode: st.session_state.document=st.text_area("Edit Document", value=st.session_state.document, height=520)
    st.markdown(f'<div class="preview">{html.escape(st.session_state.document)}</div>', unsafe_allow_html=True)
    st.subheader("Download")
    b1,b2,b3=st.columns(3)
    with b1: st.download_button("Download TXT", st.session_state.document.encode(), "legal_document.txt", "text/plain", use_container_width=True)
    with b2: st.download_button("Download DOCX", format_docx(st.session_state.document, document_type), "legal_document.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
    with b3: st.download_button("Download PDF", format_pdf(st.session_state.document, document_type), "legal_document.pdf", "application/pdf", use_container_width=True)
st.caption("AI-assisted drafting only. Review generated documents with a qualified legal professional before use.")
