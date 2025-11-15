"""
Report Service Module
Handles report management and retrieval
"""
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ReportService:
    """Service for managing veterinary reports"""

    def __init__(self, report_dir):
        """
        Initialize report service

        Args:
            report_dir (Path): Directory containing reports
        """
        self.report_dir = Path(report_dir)

    def get_recent_reports(self, limit=10, offset=0):
        """
        Get recent reports with pagination support

        Args:
            limit (int): Maximum number of reports to return
            offset (int): Number of reports to skip

        Returns:
            list: List of report dictionaries
        """
        if not self.report_dir.exists():
            logger.warning(f"Report directory does not exist: {self.report_dir}")
            return []

        try:
            reports = list(self.report_dir.glob("*.md"))
            reports.sort(key=lambda x: x.stat().st_mtime, reverse=True)

            # Apply pagination
            paginated_reports = reports[offset:offset + limit]

            result = []
            for report in paginated_reports:
                report_info = self._parse_report_metadata(report)
                if report_info:
                    result.append(report_info)

            logger.debug(f"Retrieved {len(result)} reports (limit={limit}, offset={offset})")
            return result

        except Exception as e:
            logger.error(f"Error retrieving recent reports: {e}")
            return []

    def _parse_report_metadata(self, report_path):
        """
        Parse report metadata from filename and content

        Args:
            report_path (Path): Path to report file

        Returns:
            dict or None: Report metadata dictionary
        """
        try:
            # Parse filename: YYYYMMDD_HHMMSS_Nome_source.md
            parts = report_path.stem.split('_', 3)

            if len(parts) < 3:
                logger.warning(f"Invalid filename format: {report_path.name}")
                return None

            date_str = parts[0]
            time_str = parts[1]
            paciente = parts[2] if len(parts) > 2 else "Desconhecido"

            # Format date
            try:
                dt = datetime.strptime(f"{date_str}{time_str}", "%Y%m%d%H%M%S")
                data_formatada = dt.strftime("%d/%m/%Y %H:%M")
            except ValueError:
                data_formatada = "Data inválida"
                logger.warning(f"Invalid date format in filename: {report_path.name}")

            # Read first lines to determine consultation type
            motivo = self._extract_consultation_type(report_path)

            return {
                'data': data_formatada,
                'paciente': paciente,
                'motivo': motivo,
                'arquivo': report_path.name,
                'caminho': report_path
            }

        except Exception as e:
            logger.error(f"Error parsing report metadata for {report_path.name}: {e}")
            return None

    def _extract_consultation_type(self, report_path):
        """
        Extract consultation type from report content

        Args:
            report_path (Path): Path to report file

        Returns:
            str: Consultation type
        """
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()

                if "Motivo do retorno:" in content:
                    return "Retorno"
                else:
                    return "Consulta"

        except Exception as e:
            logger.error(f"Error reading report content: {e}")
            return "N/A"

    def search_reports(self, search_term=None, date_filter=None):
        """
        Search reports with filters

        Args:
            search_term (str, optional): Search term for patient name
            date_filter (str, optional): Date filter in DD/MM/YYYY format

        Returns:
            list: Filtered list of report dictionaries
        """
        try:
            all_reports = self.get_recent_reports(limit=1000)

            # Apply search term filter
            if search_term:
                all_reports = [
                    r for r in all_reports
                    if search_term.lower() in r['paciente'].lower()
                ]

            # Apply date filter
            if date_filter:
                all_reports = [
                    r for r in all_reports
                    if date_filter in r['data']
                ]

            logger.debug(f"Search returned {len(all_reports)} results")
            return all_reports

        except Exception as e:
            logger.error(f"Error searching reports: {e}")
            return []

    def get_report_content(self, report_path):
        """
        Get report file content

        Args:
            report_path (Path): Path to report file

        Returns:
            str or None: Report content
        """
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading report {report_path}: {e}")
            return None

    def update_report(self, report_path, new_content):
        """
        Update report content

        Args:
            report_path (Path): Path to report file
            new_content (str): New content

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            logger.info(f"Report updated successfully: {report_path.name}")
            return True
        except Exception as e:
            logger.error(f"Error updating report {report_path}: {e}")
            return False

    def delete_report(self, report_path):
        """
        Delete a report file

        Args:
            report_path (Path): Path to report file

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            report_path.unlink()
            logger.info(f"Report deleted successfully: {report_path.name}")
            return True
        except Exception as e:
            logger.error(f"Error deleting report {report_path}: {e}")
            return False
