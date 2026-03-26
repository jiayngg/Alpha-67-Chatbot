"""
Brain module for LLM-powered reasoning.

This module provides different brain implementations that use LLMs for reasoning.
"""

from .base import BaseBrain as BrainInterface
from .variants.llm_brain import LLMBrain
from .brain_factory import create_brain

__all__ = [
    "BrainInterface",
    "LLMBrain",
    "create_brain"
] 