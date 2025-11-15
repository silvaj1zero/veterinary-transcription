"""
PDF Conversion Module with proper Unicode support
Replaces the problematic fpdf implementation
"""
import re
from pathlib import Path
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import logging

# Configure logging
logger = logging.getLogger(__name__)


class MarkdownToPDFConverter:
    """Converts Markdown content to PDF with proper Unicode support"""

    def __init__(self):
        """Initialize the converter with styles"""
        self.styles = getSampleStyleSheet()

        # Create custom styles for veterinary reports
        self.styles.add(ParagraphStyle(
            name='CustomHeading1',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.HexColor('#1f77b4'),
            fontName='Helvetica-Bold'
        ))

        self.styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=10,
            textColor=colors.HexColor('#2a9d8f'),
            fontName='Helvetica-Bold'
        ))

        self.styles.add(ParagraphStyle(
            name='CustomHeading3',
            parent=self.styles['Heading3'],
            fontSize=12,
            spaceAfter=8,
            fontName='Helvetica-Bold'
        ))

        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=10,
            leading=14,
            spaceAfter=6
        ))

        self.styles.add(ParagraphStyle(
            name='CustomBullet',
            parent=self.styles['BodyText'],
            fontSize=10,
            leading=14,
            leftIndent=20,
            bulletIndent=10
        ))

    def _clean_text_for_pdf(self, text):
        """
        Clean text for PDF rendering (escape XML chars, keep Unicode)

        Args:
            text (str): Raw text

        Returns:
            str: Cleaned text safe for PDF
        """
        # Escape XML special characters for reportlab
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')

        # Remove emojis (they may not render well)
        text = re.sub(r'[\U0001F000-\U0001FFFF]+', '', text)

        # Keep all other Unicode characters (Portuguese accents, etc.)
        return text

    def _parse_markdown_line(self, line):
        """
        Parse a markdown line and return (type, content, style)

        Args:
            line (str): Markdown line

        Returns:
            tuple: (line_type, content, style_name)
        """
        line = line.strip()

        if not line:
            return ('empty', '', None)

        # Skip table separators
        if re.match(r'^[\|\s\-:]+$', line) and '|' in line:
            return ('skip', '', None)

        if re.match(r'^[\-]{3,}$', line):
            return ('skip', '', None)

        # Headers
        if line.startswith('### '):
            return ('heading3', self._clean_text_for_pdf(line[4:]), 'CustomHeading3')
        elif line.startswith('## '):
            return ('heading2', self._clean_text_for_pdf(line[3:]), 'CustomHeading2')
        elif line.startswith('# '):
            return ('heading1', self._clean_text_for_pdf(line[2:]), 'CustomHeading1')

        # Bullet points
        elif line.startswith('- ') or line.startswith('* '):
            return ('bullet', self._clean_text_for_pdf(line[2:]), 'CustomBullet')

        # Table rows
        elif line.startswith('|') and line.endswith('|'):
            cells = [cell.strip() for cell in line.split('|') if cell.strip()]
            return ('table_row', cells, None)

        # Normal text
        else:
            # Remove markdown bold/italic
            text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', line)
            text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
            text = self._clean_text_for_pdf(text)
            return ('paragraph', text, 'CustomBody')

    def convert(self, md_content, output_path=None):
        """
        Convert markdown content to PDF

        Args:
            md_content (str): Markdown content
            output_path (str, optional): Output file path. If None, returns bytes

        Returns:
            bytes or None: PDF bytes if output_path is None, otherwise None
        """
        # Create PDF document
        if output_path:
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=0.75*inch,
                leftMargin=0.75*inch,
                topMargin=0.75*inch,
                bottomMargin=0.75*inch
            )
        else:
            # Create in-memory PDF
            from io import BytesIO
            buffer = BytesIO()
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=0.75*inch,
                leftMargin=0.75*inch,
                topMargin=0.75*inch,
                bottomMargin=0.75*inch
            )

        # Build content
        story = []
        lines = md_content.split('\n')
        table_rows = []

        for line in lines:
            line_type, content, style = self._parse_markdown_line(line)

            if line_type == 'skip':
                continue

            elif line_type == 'empty':
                # Add small spacer for empty lines
                story.append(Spacer(1, 0.1*inch))

            elif line_type == 'table_row':
                table_rows.append(content)

            elif line_type == 'bullet':
                # Flush any pending table
                if table_rows:
                    self._add_table_to_story(story, table_rows)
                    table_rows = []

                bullet_text = f"• {content}"
                para = Paragraph(bullet_text, self.styles[style])
                story.append(para)

            else:  # heading or paragraph
                # Flush any pending table
                if table_rows:
                    self._add_table_to_story(story, table_rows)
                    table_rows = []

                if content:
                    para = Paragraph(content, self.styles[style])
                    story.append(para)

                    # Add space after headings
                    if 'heading' in line_type.lower():
                        story.append(Spacer(1, 0.15*inch))

        # Flush any remaining table
        if table_rows:
            self._add_table_to_story(story, table_rows)

        # Build PDF
        try:
            doc.build(story)
            logger.info("PDF generated successfully")

            if output_path is None:
                return buffer.getvalue()

        except Exception as e:
            logger.error(f"Error generating PDF: {e}")
            raise

    def _add_table_to_story(self, story, table_rows):
        """Add a table to the story"""
        if not table_rows:
            return

        # Clean table cells
        cleaned_rows = []
        for row in table_rows:
            cleaned_row = [self._clean_text_for_pdf(cell) for cell in row]
            cleaned_rows.append(cleaned_row)

        # Create table
        table = Table(cleaned_rows)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))

        story.append(table)
        story.append(Spacer(1, 0.2*inch))


def convert_md_to_pdf(md_content, output_filename=None):
    """
    Convert markdown content to PDF with proper Unicode support

    Args:
        md_content (str): Markdown content
        output_filename (str, optional): Output filename (not used when returning bytes)

    Returns:
        bytes: PDF content as bytes
    """
    try:
        converter = MarkdownToPDFConverter()
        pdf_bytes = converter.convert(md_content, output_path=None)
        return pdf_bytes
    except Exception as e:
        logger.error(f"PDF conversion failed: {e}")
        # Fallback: return a simple error PDF
        from reportlab.pdfgen import canvas
        from io import BytesIO

        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Erro ao gerar PDF. Por favor, use o formato MD ou TXT.")
        c.save()
        return buffer.getvalue()
