from typing import List, Optional
from pydantic import BaseModel, Field

class JobRequirements(BaseModel):
    role: str = "Software Engineer"
    company: Optional[str] = None
    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    experience_years: Optional[str] = None
    education_requirements: List[str] = Field(default_factory=list)
    responsibilities: List[str] = Field(default_factory=list)
    raw_text: Optional[str] = ""

class JobParseRequest(BaseModel):
    title: Optional[str] = None
    description: str
