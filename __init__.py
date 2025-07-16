"""QuantumMetaGPT - Autonomous Quantum AI Research Agent"""

from .utils.logger import get_logger

# Initialize root logger
logger = get_logger("QuantumMetaGPT")
logger.info("Initializing QuantumMetaGPT framework")

# API exports
from .llm_paper_parser import parse_arxiv_paper
from .task_synthesizer import TaskSynthesizer
from .quantum_algorithm_generator import get_agent
from .optimizer_engine import HybridOptimizer
from .evaluation_engine import QuantumEvaluator
from .report_generator import ReportGenerator
from .security_licensing import LicenseManager

__version__ = "0.1.0"
__all__ = [
    'parse_arxiv_paper',
    'TaskSynthesizer',
    'get_agent',
    'HybridOptimizer',
    'QuantumEvaluator',
    'ReportGenerator',
    'LicenseManager'
]