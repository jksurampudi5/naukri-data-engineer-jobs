"""
Analytics engine for computing Data Engineer hiring trends from Naukri job data.
"""

from collections import Counter
from typing import List, Dict, Any, Optional
from .models import NaukriJob, MarketReport, SkillDemandStat


class MarketAnalyticsEngine:
    @staticmethod
    def categorize_experience(exp_min: int) -> str:
        if exp_min <= 2:
            return "Early Career (0-2 Yrs)"
        elif 3 <= exp_min <= 5:
            return "Mid-Senior (3-5 Yrs)"
        else:
            return "Senior / Lead (6+ Yrs)"

    @classmethod
    def analyze_market(cls, jobs: List[NaukriJob]) -> MarketReport:
        if not jobs:
            return MarketReport(
                total_jobs_analyzed=0,
                top_skills=[],
                city_distribution={},
                experience_brackets={},
            )

        total = len(jobs)
        skill_counter = Counter()
        city_counter = Counter()
        exp_counter = Counter()
        sal_mins = []
        sal_maxs = []

        for job in jobs:
            # Skills
            for skill in job.skills_tags:
                norm_skill = skill.strip()
                if norm_skill:
                    skill_counter[norm_skill] += 1

            # Cities
            for loc in job.locations:
                city_counter[loc] += 1

            # Experience
            bracket = cls.categorize_experience(job.experience_min)
            exp_counter[bracket] += 1

            # Salaries
            if job.salary_min_lacs is not None:
                sal_mins.append(job.salary_min_lacs)
            if job.salary_max_lacs is not None:
                sal_maxs.append(job.salary_max_lacs)

        # Build top skills stats
        top_skills = []
        for skill_name, count in skill_counter.most_common(15):
            pct = round((count / total) * 100.0, 1)
            top_skills.append(SkillDemandStat(skill_name=skill_name, frequency=count, percentage=pct))

        avg_sal_min = round(sum(sal_mins) / len(sal_mins), 1) if sal_mins else None
        avg_sal_max = round(sum(sal_maxs) / len(sal_maxs), 1) if sal_maxs else None

        return MarketReport(
            total_jobs_analyzed=total,
            top_skills=top_skills,
            city_distribution=dict(city_counter.most_common()),
            experience_brackets=dict(exp_counter),
            avg_salary_min_lacs=avg_sal_min,
            avg_salary_max_lacs=avg_sal_max,
        )
