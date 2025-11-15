"""
Text Conversion Utilities
Handles conversion between different formats (MD, TXT, PDF)
"""
import re
import logging

logger = logging.getLogger(__name__)


def convert_md_to_txt(md_content):
    """
    Convert Markdown content to plain text

    Args:
        md_content (str): Markdown content

    Returns:
        str: Plain text content
    """
    try:
        # Remove headers (#)
        txt = re.sub(r'^#+\s+', '', md_content, flags=re.MULTILINE)

        # Remove bold/italic
        txt = re.sub(r'\*\*(.+?)\*\*', r'\1', txt)
        txt = re.sub(r'\*(.+?)\*', r'\1', txt)

        # Remove markdown links [text](url)
        txt = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', txt)

        # Remove table markdown (convert to simple text)
        txt = re.sub(r'\|', ' ', txt)
        txt = re.sub(r'^[-:\s]+$', '', txt, flags=re.MULTILINE)

        # Remove emojis if present
        txt = re.sub(r'[\U0001F000-\U0001FFFF]+', '', txt)

        # Remove extra blank lines
        txt = re.sub(r'\n{3,}', '\n\n', txt)

        return txt.strip()

    except Exception as e:
        logger.error(f"Error converting MD to TXT: {e}")
        return md_content  # Return original on error
