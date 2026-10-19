import pytest
from src.naukri_de.models import NaukriJob
from src.naukri_de.analytics import MarketAnalyticsEngine


def test_market_analytics_aggregation():
    jobs = [
        NaukriJob(
            job_id="1",
            title="Data Engineer",
            company_name="CorpA",
            experience_min=3,
            experience_max=6,
            salary_raw="12-18 Lacs P.A.",
            salary_min_lacs=12.0,
            salary_max_lacs=18.0,
            locations=["Bangalore"],
            skills_tags=["PySpark", "Databricks", "SQL"],
            description="DE role",
            posted_days_ago="1 day ago",
        ),
        NaukriJob(
            job_id="2",
            title="Senior Data Engineer",
            company_name="CorpB",
            experience_min=5,
            experience_max=9,
            salary_raw="20-30 Lacs P.A.",
            salary_min_lacs=20.0,
            salary_max_lacs=30.0,
            locations=["Bangalore", "Hyderabad"],
            skills_tags=["PySpark", "Airflow"],
            description="Senior role",
            posted_days_ago="3 days ago",
        ),
    ]

    report = MarketAnalyticsEngine.analyze_market(jobs)
    assert report.total_jobs_analyzed == 2
    assert report.avg_salary_min_lacs == 16.0
    assert report.avg_salary_max_lacs == 24.0

    skill_names = [s.skill_name for s in report.top_skills]
    assert "PySpark" in skill_names
    assert report.city_distribution["Bangalore"] == 2
    assert report.city_distribution["Hyderabad"] == 1


def test_empty_market_analytics():
    report = MarketAnalyticsEngine.analyze_market([])
    assert report.total_jobs_analyzed == 0
    assert len(report.top_skills) == 0
