from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from app.schemas.resume import ResumeParseResponse, ParsedResume
from app.services.pdf_service import pdf_service
from app.services.llm_service import llm_service

router = APIRouter(prefix="/resume", tags=["Resume Intelligence"])

@router.post("/parse", response_model=ResumeParseResponse)
async def parse_resume_file(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None)
):
    """
    Parse a resume from an uploaded PDF file or raw text.
    Extracts text via PyMuPDF and produces structured candidate information.
    """
    extracted_text = ""
    if file:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are currently supported")
        try:
            content = await file.read()
            extracted_text = pdf_service.extract_text_from_bytes(content)
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Failed to read PDF: {str(e)}")
    elif text:
        extracted_text = text
    else:
        raise HTTPException(status_code=400, detail="Either a PDF file or raw text must be provided")

    if not extracted_text.strip():
        raise HTTPException(status_code=422, detail="No readable text found in the document")

    parsed_resume = llm_service.parse_resume(extracted_text)
    return ResumeParseResponse(
        success=True,
        message="Resume extracted and parsed successfully",
        resume=parsed_resume
    )
