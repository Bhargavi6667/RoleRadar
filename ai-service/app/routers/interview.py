from fastapi import APIRouter, HTTPException
from app.schemas.interview import (
    InterviewStartRequest,
    InterviewAnswerRequest,
    InterviewQuestion,
    InterviewEvaluation,
    RoleQuestionsRequest,
    RoleQuestionsResponse,
    RoleEvaluateRequest,
    RoleEvaluateResponse,
)
from app.services.llm_service import llm_service
from app.services.role_interview_service import generate_questions, evaluate_answer
from app.config import settings
from app.services.interview_agent import interview_agent

router = APIRouter(prefix="/interview", tags=["AI Interview Agent"])

@router.post("/start", response_model=InterviewQuestion)
async def start_interview_session(request: InterviewStartRequest):
    """Initialize an adaptive technical mock interview tailored to candidate's background."""
    if not request.resume_text.strip() or not request.job_description.strip():
        raise HTTPException(status_code=400, detail="Resume context and Job Description are required")

    return interview_agent.start_interview(
        resume_text=request.resume_text,
        job_description=request.job_description,
        topics=request.topics
    )

@router.post("/respond", response_model=InterviewEvaluation)
async def submit_answer(request: InterviewAnswerRequest):
    """Submit candidate's answer for evaluation and retrieve next adaptive question."""
    if not request.question.strip() or not request.answer.strip():
        raise HTTPException(status_code=400, detail="Question and answer text cannot be empty")

    return interview_agent.evaluate_and_next(
        question=request.question,
        answer=request.answer,
        resume_context=request.resume_context or "",
        job_context=request.job_context or "",
        history=request.history or []
    )


@router.post("/role-questions", response_model=RoleQuestionsResponse)
async def role_questions(request: RoleQuestionsRequest):
    """Interview questions for a role, personalised with the candidate's matched / missing skills."""
    return generate_questions(
        role_id=request.role_id,
        role=request.role or "",
        matched=request.matched_skills,
        missing=request.missing_skills,
        resume_text=request.resume_text or "",
        client=llm_service.client,
        model=settings.OPENAI_MODEL,
    )


@router.post("/role-evaluate", response_model=RoleEvaluateResponse)
async def role_evaluate(request: RoleEvaluateRequest):
    """Feedback on a practice answer (AI if an OpenAI key is set, otherwise a basic checklist)."""
    if len(request.answer.strip()) < 5:
        raise HTTPException(status_code=400, detail="Please write an answer first.")
    return evaluate_answer(
        role_id=request.role_id,
        role=request.role or "",
        question=request.question,
        answer=request.answer,
        client=llm_service.client,
        model=settings.OPENAI_MODEL,
    )
