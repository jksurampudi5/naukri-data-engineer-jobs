import pytest
from src.naukri_de.parser import NaukriParser


def test_parse_experience():
    assert NaukriParser.parse_experience("3-6 Yrs") == (3, 6)
    assert NaukriParser.parse_experience("5 Yrs") == (5, 8)
    assert NaukriParser.parse_experience("") == (0, 10)


def test_parse_salary():
    assert NaukriParser.parse_salary("14-22 Lacs P.A.") == (14.0, 22.0)
    assert NaukriParser.parse_salary("10-16 Lacs PA") == (10.0, 16.0)
    assert NaukriParser.parse_salary("Not Disclosed") == (None, None)


def test_normalize_locations():
    locs = NaukriParser.normalize_locations("Bangalore/Bengaluru, Hyderabad")
    assert "Bangalore" in locs
    assert "Hyderabad" in locs


def test_parse_record():
    raw = {
        "job_id": "TEST-101",
        "title": "Lead Data Engineer",
        "company_name": "TestCompany",
        "experience_raw": "4-8 Yrs",
        "salary_raw": "18-25 Lacs P.A.",
        "location_raw": "Pune, Remote",
        "skills_tags": ["PySpark", "Databricks", "SQL"],
        "description": "Building lakehouse with Spark.",
    }
    job = NaukriParser.parse_record(raw)
    assert job.job_id == "TEST-101"
    assert job.experience_min == 4
    assert job.experience_max == 8
    assert job.salary_min_lacs == 18.0
    assert job.salary_max_lacs == 25.0
    assert "Pune" in job.locations
    assert "Remote" in job.locations
    assert len(job.skills_tags) == 3


def test_parse_real_jobs_file():
    import json
    from pathlib import Path
    real_jobs_path = Path(__file__).parent.parent / "data" / "jobs.json"
    assert real_jobs_path.exists()
    with open(real_jobs_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    jobs = [NaukriParser.parse_record(r) for r in data]
    assert len(jobs) >= 20
    assert any("Amazon" in j.company_name for j in jobs)
    assert all(bool(j.application_url) for j in jobs)

