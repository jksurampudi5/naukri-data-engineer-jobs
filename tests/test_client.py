import pytest
from pathlib import Path
from src.naukri_de.client import NaukriScraperClient


def test_client_fixture_loading():
    client = NaukriScraperClient(offline_mode=True)
    jobs = client.fetch_jobs()
    assert len(jobs) >= 5
    assert all(hasattr(j, "title") for j in jobs)
    assert all(hasattr(j, "skills_tags") for j in jobs)


def test_client_missing_fixture():
    client = NaukriScraperClient(offline_mode=True, fixture_path="invalid_path.json")
    with pytest.raises(FileNotFoundError):
        client.fetch_jobs()
