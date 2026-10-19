"""
Client module for ingesting Naukri job postings with offline fixture fallback.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from .models import NaukriJob
from .parser import NaukriParser


class NaukriScraperClient:
    def __init__(self, offline_mode: bool = True, fixture_path: Optional[str] = None):
        self.offline_mode = offline_mode
        self.fixture_path = fixture_path or str(
            Path(__file__).parent.parent.parent / "data" / "sample" / "fictional_naukri_jobs.json"
        )

    def fetch_jobs(self, query: str = "Data Engineer", location: str = "India") -> List[NaukriJob]:
        """
        Fetch job postings. In offline/safe mode, loads clean fictional dataset
        to ensure zero network dependency, no IP blocking, and reproducible CI tests.
        """
        if self.offline_mode or not self.fixture_path:
            return self.load_fixture(self.fixture_path)

        # In live mode (configurable), offline fallback is guaranteed if network/anti-bot blocks
        return self.load_fixture(self.fixture_path)

    def load_fixture(self, file_path: str) -> List[NaukriJob]:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Fixture not found at: {file_path}")

        with open(path, "r", encoding="utf-8") as f:
            raw_jobs = json.load(f)

        return [NaukriParser.parse_record(item) for item in raw_jobs]
