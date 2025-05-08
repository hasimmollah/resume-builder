from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class PromptData:
    topic = str,
    topic_content = str,
    job_description = str


@dataclass
class ResumeData:
    name = str,
    contact = str,
    professional_summary = str,
    keystrengths: List[str] = field(default_factory=list),
    company_data: List[Dict] = field(default_factory=Dict),
    certifications: List[str]= field(default_factory=list),
    education: List[str]= field(default_factory=list),
