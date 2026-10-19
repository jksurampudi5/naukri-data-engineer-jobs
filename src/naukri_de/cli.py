"""
CLI entrypoint for Naukri Data Engineer job analytics.
"""

import argparse
import sys
from pathlib import Path
from .client import NaukriScraperClient
from .analytics import MarketAnalyticsEngine
from .exporter import DataExporter


def main(args=None):
    parser = argparse.ArgumentParser(
        description="Naukri Data Engineer Jobs Pipeline & Market Analytics"
    )
    parser.add_argument(
        "--sample",
        type=str,
        default=str(Path(__file__).parent.parent.parent / "data" / "sample" / "fictional_naukri_jobs.json"),
        help="Path to sample Naukri jobs JSON fixture",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="Number of top skills to display in summary",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate and print full Markdown intelligence report",
    )

    parsed = parser.parse_args(args)

    print(f"🔍 Loading Naukri Data Engineering job postings from: {parsed.sample}")
    client = NaukriScraperClient(offline_mode=True, fixture_path=parsed.sample)
    jobs = client.fetch_jobs()

    print(f"📊 Analyzing market trends across {len(jobs)} postings...")
    report = MarketAnalyticsEngine.analyze_market(jobs)

    print(f"\n✅ Market Intelligence Summary:")
    print(f"  • Total Jobs Analyzed: {report.total_jobs_analyzed}")
    print(f"  • Top {parsed.top} High-Demand Skills:")
    for stat in report.top_skills[:parsed.top]:
        print(f"     - {stat.skill_name}: {stat.frequency} postings ({stat.percentage}%)")

    print(f"  • Top Locations:")
    for city, count in list(report.city_distribution.items())[:3]:
        print(f"     - {city}: {count} jobs")

    if parsed.report:
        md = DataExporter.to_markdown(report)
        print("\n" + "=" * 50)
        print(md)
        print("=" * 50)

    return 0


if __name__ == "__main__":
    sys.exit(main())
