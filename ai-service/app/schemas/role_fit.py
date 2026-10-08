from typing import List
from pydantic import BaseModel, Field


class RoleFitRequest(BaseModel):
    resume_text: str


class RoleScore(BaseModel):
    role_id: str
    role: str
    score: int
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)


class QualityCheck(BaseModel):
    label: str
    passed: bool
    tip: str = ""


class Suggestion(BaseModel):
    category: str
    priority: str  # High | Medium | Low
    text: str


class RoleFitResponse(BaseModel):
    best_role_id: str
    best_role: str
    overall_score: int
    fit_label: str
    summary: str
    low_signal: bool = False
    role_scores: List[RoleScore]
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    detected_skills: List[str] = Field(default_factory=list)
    resume_quality_score: int
    quality_checks: List[QualityCheck] = Field(default_factory=list)
    suggestions: List[Suggestion] = Field(default_factory=list)
    ai_enhanced: bool = False
