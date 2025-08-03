"""Card generator package for creating poker card images."""

__version__ = "2.0.0"
__author__ = "Richard Falconer"

from .card_generator import CardGenerator
from .config import Config

__all__ = ["CardGenerator", "Config"]
