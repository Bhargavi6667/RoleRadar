from typing import List, Optional
from pydantic import BaseModel, Field

class ExperienceItem(BaseModel):
    role: str = ""
    company: str = ""
    duration: Optional[str] = ""
    description: List[str] = Field(default_factory=list)
    technologies: List[str] = Field(default_factory=list)

class ProjectItem(BaseModel):
    name: str = ""
    description: str = ""
    technologies: List[str] = Field(default_factory=list)
    link: Optional[str] = None

class EducationItem(BaseModel):
    degree: str = ""
    institution: str = ""
    year: Optional[str] = ""
    score: Optional[str] = None

class ParsedResume(BaseModel):
    name: Optional[str] = "Candidate"
    email: Optional[str] = ""
    phone: Optional[str] = ""
    location: Optional[str] = ""
    summary: Optional[str] = ""
    skills: List[str] = Field(default_factory=list)
    experiences: List[ExperienceItem] = Field(default_factory=list)
    projects: List[ProjectItem] = Field(default_factory=list)
    education: List[EducationItem] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    achievements: List[str] = Field(default_factory=list)
    raw_text: Optional[str] = ""

class ResumeParseResponse(BaseModel):
    success: bool = True
    message: str = "Resume parsed successfully"
    resume: ParsedResume
