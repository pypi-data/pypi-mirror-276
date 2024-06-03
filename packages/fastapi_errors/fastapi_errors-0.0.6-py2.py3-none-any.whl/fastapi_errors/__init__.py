"""Fastapi errors module."""
__version__ = "0.0.6"
from .exceptions import BaseHTTPException, DefaultHTTPException
from .generator import ExamplesGenerator, generate_examples

__all__ = [
    "BaseHTTPException",
    "DefaultHTTPException",
    "ExamplesGenerator",
    "generate_examples",
]
