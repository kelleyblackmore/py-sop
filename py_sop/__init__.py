"""
py-sop: A CLI tool for generating Standard Operating Procedure templates.
"""

__version__ = "0.1.0"

from .generator import SOPGenerator
from .templates import SOPTemplate

__all__ = ["SOPGenerator", "SOPTemplate", "__version__"]
