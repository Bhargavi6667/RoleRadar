from fastapi import APIRouter, HTTPException
from app.schemas.analysis import ResumeAnalysisRequest, ResumeAnalysisResponse
from app.schemas.job import JobParseRequest, JobRequirements
from app.schemas.role_fit import RoleFitRequest, RoleFitResponse
from app.services.llm_service import llm_service
from app.services.role_service import analyze_role_fit
from app.config import settings

router = APIRouter(prefix="/analysis", tags=["Analysis & Matching"])

@router.post("/parse-job", response_model=JobRequirements)
async def parse_job_description(request: JobParseRequest):
    """Extract structured skills, requirements, and responsibilities from JD text."""
    if not request.description.strip():
        raise HTTPException(status_code=400, detail="Job description text cannot be empty")
    return llm_service.parse_job_description(request.description, title=request.title or "")

@router.post("/match", response_model=ResumeAnalysisResponse)
async def analyze_match(request: ResumeAnalysisRequest):
    """
    Perform deep evidence-backed matching between candidate resume and job description.
    Computes 6-dimensional score, gap analysis, and tailored learning roadmap.
    """
    if not request.resume_text.strip() or not request.job_description.strip():
        raise HTTPException(status_code=400, detail="Both resume text and job description are required")

    return llm_service.analyze(
        resume_text=request.resume_text,
        job_text=request.job_description,
        parsed_resume=request.parsed_resume,
        parsed_job=request.parsed_job
    )


@router.post("/role-fit", response_model=RoleFitResponse)
async def role_fit(request: RoleFitRequest):
    """
    Resume-only analysis (no job description needed): finds the roles the resume
    suits best (frontend, sales, ...), scores the fit, grades the resume, and
    returns prioritised suggestions.
    """
    text = request.resume_text.strip()
    if len(text) < 80:
        raise HTTPException(
            status_code=422,
            detail="Not enough readable text in the resume. If it is a scanned image PDF, upload a text-based PDF instead."
        )
    return analyze_role_fit(text, llm_client=llm_service.client, model=settings.OPENAI_MODEL)
