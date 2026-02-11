"""
Backend module for Math Study AI
Handles Flask API and data management
"""

from .app import app
from .data_handler import MathResourcesManager

__all__ = ['app', 'MathResourcesManager']
