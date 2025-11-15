"""
Statistics Service Module
Handles all statistics and metrics calculations
"""
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class StatsService:
    """Service for managing system statistics"""

    def __init__(self, report_dir):
        """
        Initialize stats service

        Args:
            report_dir (Path): Directory containing reports
        """
        self.report_dir = Path(report_dir)

    def get_stats(self):
        """
        Get system statistics

        Returns:
            dict: Statistics dictionary with metrics
        """
        stats = {
            'total_relatorios': 0,
            'relatorios_hoje': 0,
            'custo_total': 0.0,
            'custo_hoje': 0.0,
            'tempo_medio': 0
        }

        try:
            # Count reports
            if self.report_dir.exists():
                reports = list(self.report_dir.glob("*.md"))
                stats['total_relatorios'] = len(reports)

                # Today's reports
                hoje = datetime.now().strftime("%Y%m%d")
                stats['relatorios_hoje'] = sum(
                    1 for r in reports if r.stem.startswith(hoje)
                )

                # Cost estimation ($0.05 per report - should be configurable)
                COST_PER_REPORT = 0.05
                stats['custo_total'] = stats['total_relatorios'] * COST_PER_REPORT
                stats['custo_hoje'] = stats['relatorios_hoje'] * COST_PER_REPORT

            logger.debug(f"Stats calculated: {stats}")
            return stats

        except Exception as e:
            logger.error(f"Error calculating stats: {e}")
            return stats

    def get_report_count_by_date_range(self, start_date, end_date):
        """
        Get report count within a date range

        Args:
            start_date (datetime): Start date
            end_date (datetime): End date

        Returns:
            int: Number of reports in range
        """
        if not self.report_dir.exists():
            return 0

        count = 0
        try:
            reports = list(self.report_dir.glob("*.md"))
            for report in reports:
                # Parse timestamp from filename: YYYYMMDD_HHMMSS_...
                try:
                    date_str = report.stem.split('_')[0]
                    report_date = datetime.strptime(date_str, "%Y%m%d")

                    if start_date <= report_date <= end_date:
                        count += 1
                except (ValueError, IndexError):
                    continue

            return count

        except Exception as e:
            logger.error(f"Error counting reports in date range: {e}")
            return 0

    def get_total_api_cost(self, cost_per_report=0.05):
        """
        Calculate total API cost

        Args:
            cost_per_report (float): Cost per report in USD

        Returns:
            float: Total cost
        """
        try:
            if self.report_dir.exists():
                report_count = len(list(self.report_dir.glob("*.md")))
                return report_count * cost_per_report
            return 0.0
        except Exception as e:
            logger.error(f"Error calculating API cost: {e}")
            return 0.0
