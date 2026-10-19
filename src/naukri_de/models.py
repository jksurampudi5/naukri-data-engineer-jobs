"""
Data models for the Naukri Data Engineer job market analytics pipeline.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional


@dataclass
class NaukriJob:
    job_id: str
    title: str
    company_name: str
    experience_min: int
    experience_max: int
    salary_raw: str
    salary_min_lacs: Optional[float]
    salary_max_lacs: Optional[float]
    locations: List[str]
    skills_tags: List[str]
    description: str
    posted_days_ago: str
    application_url: str = ""
    source: str = "Naukri"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NaukriJob":
        return cls(**data)


@dataclass
class SkillDemandStat:
    skill_name: str
    frequency: int
    percentage: float  # Percentage of jobs requesting this skill


@dataclass
class MarketReport:
    total_jobs_analyzed: int
    top_skills: List[SkillDemandStat]
    city_distribution: Dict[str, int]
    experience_brackets: Dict[str, int]
    avg_salary_min_lacs: Optional[float] = None
    avg_salary_max_lacs: Optional[float] = None
