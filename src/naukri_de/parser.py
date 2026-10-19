"""
Parser for extracting and normalizing structured attributes from Naukri job postings.
"""

import re
from typing import List, Dict, Any, Tuple, Optional
from .models import NaukriJob


class NaukriParser:
    LOCATION_CANONICAL = {
        "bangalore": "Bangalore",
        "bengaluru": "Bangalore",
        "hyderabad": "Hyderabad",
        "secunderabad": "Hyderabad",
        "pune": "Pune",
        "chennai": "Chennai",
        "mumbai": "Mumbai",
        "noida": "Delhi/NCR",
        "gurgaon": "Delhi/NCR",
        "gurugram": "Delhi/NCR",
        "delhi": "Delhi/NCR",
        "remote": "Remote",
    }

    @classmethod
    def parse_experience(cls, exp_raw: str) -> Tuple[int, int]:
        """Extract min and max years of experience from strings like '3-6 Yrs'."""
        if not exp_raw:
            return 0, 10

        match = re.search(r"(\d+)\s*-\s*(\d+)", exp_raw)
        if match:
            return int(match.group(1)), int(match.group(2))

        single_match = re.search(r"(\d+)", exp_raw)
        if single_match:
            val = int(single_match.group(1))
            return val, val + 3

        return 0, 10

    @classmethod
    def parse_salary(cls, salary_raw: str) -> Tuple[Optional[float], Optional[float]]:
        """Parse salary ranges in Lakhs Per Annum, e.g. '14-22 Lacs P.A.'."""
        if not salary_raw or "not disclosed" in salary_raw.lower():
            return None, None

        match = re.search(r"([\d\.]+)\s*-\s*([\d\.]+)\s*(?:lacs|lakh|lac|pa|p\.a\.)", salary_raw, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1)), float(match.group(2))
            except ValueError:
                return None, None

        return None, None

    @classmethod
    def normalize_locations(cls, loc_raw: str) -> List[str]:
        """Normalize location string into canonical list of tech hubs."""
        if not loc_raw:
            return ["Not Specified"]

        found_locations = set()
        parts = re.split(r"[,/|;]", loc_raw)
        for part in parts:
            clean = part.strip().lower()
            for key, canonical in cls.LOCATION_CANONICAL.items():
                if key in clean:
                    found_locations.add(canonical)

        if not found_locations:
            found_locations.add(loc_raw.strip())

        return sorted(list(found_locations))

    @classmethod
    def parse_record(cls, raw: Dict[str, Any]) -> NaukriJob:
        exp_raw = str(raw.get("experience_raw", ""))
        exp_min, exp_max = cls.parse_experience(exp_raw)

        salary_raw = str(raw.get("salary_raw", "Not Disclosed"))
        sal_min, sal_max = cls.parse_salary(salary_raw)

        loc_raw = str(raw.get("location_raw", ""))
        locations = cls.normalize_locations(loc_raw)

        skills = raw.get("skills_tags", [])
        if isinstance(skills, str):
            skills = [s.strip() for s in skills.split(",") if s.strip()]

        return NaukriJob(
            job_id=str(raw.get("job_id", "")),
            title=str(raw.get("title", "")).strip(),
            company_name=str(raw.get("company_name", "")).strip(),
            experience_min=exp_min,
            experience_max=exp_max,
            salary_raw=salary_raw,
            salary_min_lacs=sal_min,
            salary_max_lacs=sal_max,
            locations=locations,
            skills_tags=[s.strip() for s in skills if s.strip()],
            description=str(raw.get("description", "")).strip(),
            posted_days_ago=str(raw.get("posted_days_ago", "Recent")),
            source=str(raw.get("source", "Naukri")),
        )
