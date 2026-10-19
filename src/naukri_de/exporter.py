"""
Data exporter for formatting Naukri DE market analytics into Markdown and CSV reports.
"""

from typing import List
from datetime import datetime
from .models import MarketReport


class DataExporter:
    @staticmethod
    def to_markdown(report: MarketReport) -> str:
        lines = [
            "# 📈 Naukri Data Engineer Market Intelligence Report",
            f"**Generated**: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}",
            f"**Total Postings Analyzed**: {report.total_jobs_analyzed}",
            "",
            "## 🛠️ Most Demanded Data Engineering Skills",
            "",
            "| Rank | Skill / Technology | Frequency | Demand Share (%) |",
            "| :--- | :--- | :--- | :--- |",
        ]

        for rank, stat in enumerate(report.top_skills, start=1):
            lines.append(f"| #{rank} | **{stat.skill_name}** | {stat.frequency} | `{stat.percentage}%` |")

        lines.extend([
            "",
            "## 🏙️ Location & Hub Distribution",
            "",
            "| Tech Hub | Active Postings |",
            "| :--- | :--- |",
        ])

        for city, count in report.city_distribution.items():
            lines.append(f"| {city} | {count} |")

        lines.extend([
            "",
            "## 🎓 Experience Breakdown",
            "",
            "| Experience Bracket | Number of Postings |",
            "| :--- | :--- |",
        ])

        for bracket, count in report.experience_brackets.items():
            lines.append(f"| {bracket} | {count} |")

        if report.avg_salary_min_lacs and report.avg_salary_max_lacs:
            lines.extend([
                "",
                "## 💰 Disclosed Compensation Overview",
                f"- **Average Minimum**: {report.avg_salary_min_lacs} LPA",
                f"- **Average Maximum**: {report.avg_salary_max_lacs} LPA",
            ])

        lines.extend([
            "",
            "> *Report compiled automatically from sanitized sample datasets.*"
        ])

        return "\n".join(lines)
