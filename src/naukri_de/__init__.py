"""
Naukri Data Engineer Jobs Ingestion & Market Analytics Pipeline.
"""

__version__ = "1.0.0"

from .models import NaukriJob, MarketReport, SkillDemandStat
from .parser import NaukriParser
from .client import NaukriScraperClient
from .analytics import MarketAnalyticsEngine
from .exporter import DataExporter

__all__ = [
    "NaukriJob",
    "MarketReport",
    "SkillDemandStat",
    "NaukriParser",
    "NaukriScraperClient",
    "MarketAnalyticsEngine",
    "DataExporter",
]
