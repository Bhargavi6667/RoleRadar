from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.resume import ParsedResume
from app.schemas.job import JobRequirements

class SkillEvidence(BaseModel):
    skill: str
    status: str = "Strong"  # Strong, Moderate, Inferred, Missing
    evidence: str
    source: str = "Project"  # Project, Experience, Certification, Education, None
    confidence: float = 0.9  # 0.0 to 1.0

class ScoringBreakdown(BaseModel):
    skill_match: float = 0.0          # 35%
    evidence_strength: float = 0.0    # 20%
    project_relevance: float = 0.0    # 15%
    experience_alignment: float = 0.0 # 10%
    education_alignment: float = 0.0  # 10%
    resume_quality: float = 0.0       # 10%
    final_score: float = 0.0

class RoadmapStep(BaseModel):
    phase: str
    title: str
    topics: List[str]
    practical_project: Optional[str] = None

class ResumeAnalysisRequest(BaseModel):
    resume_text: str
    job_description: str
    parsed_resume: Optional[ParsedResume] = None
    parsed_job: Optional[JobRequirements] = None

class ResumeAnalysisResponse(BaseModel):
    overall_score: float
    scoring_breakdown: ScoringBreakdown
    strengths: List[str] = Field(default_factory=list)
    skill_gaps: List[str] = Field(default_factory=list)
    evidence: List[SkillEvidence] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    interview_topics: List[str] = Field(default_factory=list)
    learning_roadmap: List[RoadmapStep] = Field(default_factory=list)
