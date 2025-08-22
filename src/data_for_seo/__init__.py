"""Data for SEO - SEO automation framework using Agent Factory."""

__version__ = "0.1.0"
__author__ = "Agent Factory"
__email__ = "dev@agent-factory.ai"

from .models.base import ExecutionResult, SEOTask, SEOMetrics
from .models.seo import (
    KeywordData,
    RankingData,
    SEOAnalysis,
    ContentOptimization,
    TechnicalAudit,
)

__all__ = [
    "ExecutionResult",
    "SEOTask", 
    "SEOMetrics",
    "KeywordData",
    "RankingData",
    "SEOAnalysis",
    "ContentOptimization",
    "TechnicalAudit",
]
