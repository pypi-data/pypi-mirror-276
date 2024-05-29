"""
The :mod:`fairbalance._tools` module should not be used. it includes different useful classes and functions internal to the process.
"""

from ._fairness_analysis import FairnessAnalysis
from ._mitigator import Mitigator
from ._processor import _Processor, RandomOverSamplerProcessor, SMOTENCProcessor, RandomUnderSamplerProcessor

__all__ = [
    "FairnessAnalysis",
    "Mitigator",
    "SMOTENCProcessor",
    "RandomOverSamplerProcessor",
    "RandomUnderSamplerProcessor",
]