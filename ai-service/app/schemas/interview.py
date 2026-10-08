from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class InterviewStartRequest(BaseModel):
    resume_text: str
    job_description: str
    topics: Optional[List[str]] = Field(default_factory=list)

class InterviewAnswerRequest(BaseModel):
    session_id: Optional[str] = "session-default"
    question: str
    answer: str
    resume_context: Optional[str] = ""
    job_context: Optional[str] = ""
    history: Optional[List[Dict[str, Any]]] = Field(default_factory=list)

class InterviewQuestion(BaseModel):
    question_id: str
    topic: str
    question: str
    context: Optional[str] = None
    difficulty: str = "Medium"  # Easy, Medium, Hard

class InterviewEvaluation(BaseModel):
    evaluation: str
    score: float
    strengths: List[str] = Field(default_factory=list)
    areas_for_improvement: List[str] = Field(default_factory=list)
    follow_up_question: Optional[str] = None
    next_question: InterviewQuestion


# ---- Role-based interview practice -------------------------------------------------
class RoleQuestionsRequest(BaseModel):
    role_id: str
    role: Optional[str] = ""
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    resume_text: Optional[str] = ""


class RoleQuestionItem(BaseModel):
    id: str
    category: str
    difficulty: str = "Medium"
    question: str
    tip: str = ""


class RoleQuestionsResponse(BaseModel):
    role_id: str
    role: str
    questions: List[RoleQuestionItem]
    ai_generated: bool = False


class RoleEvaluateRequest(BaseModel):
    role_id: str
    role: Optional[str] = ""
    question: str
    answer: str


class RoleEvaluateResponse(BaseModel):
    score: float
    verdict: str
    strengths: List[str] = Field(default_factory=list)
    improvements: List[str] = Field(default_factory=list)
    model_answer_tip: str = ""
    ai_generated: bool = False
