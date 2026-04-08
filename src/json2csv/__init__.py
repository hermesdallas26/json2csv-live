"""
JSON to CSV Converter Tool.

A Python CLI tool for converting JSON data to CSV format with support for
nested JSON flattening, custom delimiters, and flexible input/output options.
"""

__version__ = "0.1.0"
__author__ = "DevOrg"
__all__ = ["json_to_csv", "flatten_dict", "main"]

try:
    from .main import json_to_csv, flatten_dict, main
except ImportError:
    pass
