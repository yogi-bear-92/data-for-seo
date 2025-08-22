"""SEO-specific models for the Data for SEO framework."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, ConfigDict, HttpUrl


class SearchEngine(str, Enum):
    """Supported search engines."""
    
    GOOGLE = "google"
    BING = "bing"
    YAHOO = "yahoo"
    YANDEX = "yandex"
    BAIDU = "baidu"


class KeywordDifficulty(str, Enum):
    """Keyword difficulty levels."""
    
    VERY_EASY = "very_easy"
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    VERY_HARD = "very_hard"


class ContentType(str, Enum):
    """Content types for optimization."""
    
    WEBPAGE = "webpage"
    BLOG_POST = "blog_post"
    PRODUCT_PAGE = "product_page"
    CATEGORY_PAGE = "category_page"
    LANDING_PAGE = "landing_page"


class AuditSeverity(str, Enum):
    """Technical audit issue severity."""
    
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class KeywordData(BaseModel):
    """Keyword research and analysis data."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid",
    )
    
    # Basic keyword info
    keyword: str = Field(description="The keyword phrase")
    search_volume: Optional[int] = Field(
        default=None, description="Monthly search volume"
    )
    keyword_difficulty: Optional[KeywordDifficulty] = Field(
        default=None, description="Keyword difficulty level"
    )
    cpc: Optional[float] = Field(
        default=None, description="Cost per click in USD"
    )
    competition: Optional[float] = Field(
        default=None, description="Competition score (0-1)"
    )
    
    # Ranking data
    current_position: Optional[int] = Field(
        default=None, description="Current ranking position"
    )
    previous_position: Optional[int] = Field(
        default=None, description="Previous ranking position"
    )
    position_change: Optional[int] = Field(
        default=None, description="Position change (+/-)"
    )
    
    # Search engine and location
    search_engine: SearchEngine = Field(
        default=SearchEngine.GOOGLE, description="Target search engine"
    )
    location: Optional[str] = Field(
        default=None, description="Geographic location"
    )
    language: Optional[str] = Field(
        default="en", description="Language code"
    )
    
    # Related keywords
    related_keywords: List[str] = Field(
        default_factory=list, description="Related keyword suggestions"
    )
    long_tail_keywords: List[str] = Field(
        default_factory=list, description="Long-tail keyword variations"
    )
    
    # Metadata
    url: Optional[HttpUrl] = Field(
        default=None, description="URL being tracked for this keyword"
    )
    last_updated: datetime = Field(
        default_factory=datetime.utcnow, description="Last update timestamp"
    )
    
    @property
    def position_trend(self) -> str:
        """Get position trend indicator."""
        if self.position_change is None:
            return "stable"
        elif self.position_change > 0:
            return "improving"
        elif self.position_change < 0:
            return "declining"
        else:
            return "stable"


class RankingData(BaseModel):
    """Search engine ranking data."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid",
    )
    
    # Basic ranking info
    url: HttpUrl = Field(description="URL being ranked")
    keyword: str = Field(description="Keyword being tracked")
    position: int = Field(description="Current ranking position")
    
    # Search engine context
    search_engine: SearchEngine = Field(
        default=SearchEngine.GOOGLE, description="Search engine"
    )
    location: Optional[str] = Field(
        default=None, description="Geographic location"
    )
    device_type: str = Field(
        default="desktop", description="Device type (desktop/mobile)"
    )
    
    # SERP features
    featured_snippet: bool = Field(
        default=False, description="Has featured snippet"
    )
    local_pack: bool = Field(
        default=False, description="Appears in local pack"
    )
    image_pack: bool = Field(
        default=False, description="Appears in image pack"
    )
    video_results: bool = Field(
        default=False, description="Has video results"
    )
    
    # Metrics
    click_through_rate: Optional[float] = Field(
        default=None, description="Estimated CTR"
    )
    impressions: Optional[int] = Field(
        default=None, description="Number of impressions"
    )
    clicks: Optional[int] = Field(
        default=None, description="Number of clicks"
    )
    
    # Tracking
    tracked_since: datetime = Field(
        default_factory=datetime.utcnow, description="Tracking start date"
    )
    last_checked: datetime = Field(
        default_factory=datetime.utcnow, description="Last check timestamp"
    )
    
    # Historical data
    position_history: List[Dict[str, Any]] = Field(
        default_factory=list, description="Historical position data"
    )


class SEOAnalysis(BaseModel):
    """Comprehensive SEO analysis results."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid",
    )
    
    # Target information
    url: HttpUrl = Field(description="Analyzed URL")
    title: Optional[str] = Field(default=None, description="Page title")
    meta_description: Optional[str] = Field(
        default=None, description="Meta description"
    )
    
    # Content analysis
    word_count: Optional[int] = Field(
        default=None, description="Total word count"
    )
    heading_structure: Dict[str, int] = Field(
        default_factory=dict, description="Heading tag counts (H1, H2, etc.)"
    )
    keyword_density: Dict[str, float] = Field(
        default_factory=dict, description="Keyword density percentages"
    )
    
    # Technical SEO
    page_load_time: Optional[float] = Field(
        default=None, description="Page load time in seconds"
    )
    mobile_friendly: Optional[bool] = Field(
        default=None, description="Mobile-friendly status"
    )
    https_enabled: bool = Field(
        default=False, description="HTTPS enabled"
    )
    
    # Link analysis
    internal_links: int = Field(
        default=0, description="Number of internal links"
    )
    external_links: int = Field(
        default=0, description="Number of external links"
    )
    broken_links: List[str] = Field(
        default_factory=list, description="List of broken links"
    )
    
    # Images and media
    images_count: int = Field(
        default=0, description="Number of images"
    )
    images_without_alt: int = Field(
        default=0, description="Images without alt text"
    )
    
    # Schema and structured data
    schema_markup: List[str] = Field(
        default_factory=list, description="Detected schema types"
    )
    
    # Overall scores
    seo_score: Optional[float] = Field(
        default=None, description="Overall SEO score (0-100)"
    )
    content_score: Optional[float] = Field(
        default=None, description="Content quality score (0-100)"
    )
    technical_score: Optional[float] = Field(
        default=None, description="Technical SEO score (0-100)"
    )
    
    # Analysis metadata
    analyzed_at: datetime = Field(
        default_factory=datetime.utcnow, description="Analysis timestamp"
    )
    analysis_duration: Optional[float] = Field(
        default=None, description="Analysis duration in seconds"
    )


class ContentOptimization(BaseModel):
    """Content optimization recommendations."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid",
    )
    
    # Target content
    url: HttpUrl = Field(description="Content URL")
    content_type: ContentType = Field(description="Type of content")
    target_keywords: List[str] = Field(description="Target keywords")
    
    # Current content analysis
    current_title: Optional[str] = Field(
        default=None, description="Current page title"
    )
    current_meta_description: Optional[str] = Field(
        default=None, description="Current meta description"
    )
    current_word_count: Optional[int] = Field(
        default=None, description="Current word count"
    )
    
    # Optimization recommendations
    title_recommendations: List[str] = Field(
        default_factory=list, description="Title optimization suggestions"
    )
    meta_description_recommendations: List[str] = Field(
        default_factory=list, description="Meta description suggestions"
    )
    content_recommendations: List[str] = Field(
        default_factory=list, description="Content improvement suggestions"
    )
    keyword_recommendations: List[str] = Field(
        default_factory=list, description="Keyword usage recommendations"
    )
    
    # Suggested improvements
    suggested_title: Optional[str] = Field(
        default=None, description="Optimized title suggestion"
    )
    suggested_meta_description: Optional[str] = Field(
        default=None, description="Optimized meta description"
    )
    suggested_headings: List[str] = Field(
        default_factory=list, description="Suggested heading structure"
    )
    
    # Competitive analysis
    competitor_urls: List[str] = Field(
        default_factory=list, description="Competitor URLs analyzed"
    )
    content_gaps: List[str] = Field(
        default_factory=list, description="Content gaps identified"
    )
    
    # Priority and impact
    priority_score: float = Field(
        default=0.0, description="Optimization priority (0-1)"
    )
    estimated_impact: Optional[str] = Field(
        default=None, description="Estimated impact (low/medium/high)"
    )
    
    # Metadata
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Creation timestamp"
    )
    updated_at: Optional[datetime] = Field(
        default=None, description="Last update timestamp"
    )


class TechnicalAudit(BaseModel):
    """Technical SEO audit results."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid",
    )
    
    # Audit target
    url: HttpUrl = Field(description="Audited URL or domain")
    audit_type: str = Field(description="Type of audit (page/site/domain)")
    
    # Performance metrics
    page_speed_desktop: Optional[float] = Field(
        default=None, description="Desktop page speed score"
    )
    page_speed_mobile: Optional[float] = Field(
        default=None, description="Mobile page speed score"
    )
    first_contentful_paint: Optional[float] = Field(
        default=None, description="First Contentful Paint (seconds)"
    )
    largest_contentful_paint: Optional[float] = Field(
        default=None, description="Largest Contentful Paint (seconds)"
    )
    cumulative_layout_shift: Optional[float] = Field(
        default=None, description="Cumulative Layout Shift score"
    )
    
    # Crawlability and indexing
    robots_txt_exists: bool = Field(
        default=False, description="robots.txt file exists"
    )
    sitemap_exists: bool = Field(
        default=False, description="XML sitemap exists"
    )
    crawl_errors: List[str] = Field(
        default_factory=list, description="Crawl errors found"
    )
    indexing_issues: List[str] = Field(
        default_factory=list, description="Indexing issues"
    )
    
    # Technical issues
    duplicate_content: List[str] = Field(
        default_factory=list, description="Duplicate content URLs"
    )
    missing_meta_descriptions: List[str] = Field(
        default_factory=list, description="Pages missing meta descriptions"
    )
    missing_title_tags: List[str] = Field(
        default_factory=list, description="Pages missing title tags"
    )
    broken_internal_links: List[str] = Field(
        default_factory=list, description="Broken internal links"
    )
    
    # Mobile and accessibility
    mobile_friendly_issues: List[str] = Field(
        default_factory=list, description="Mobile usability issues"
    )
    accessibility_issues: List[str] = Field(
        default_factory=list, description="Accessibility issues"
    )
    
    # Security
    https_issues: List[str] = Field(
        default_factory=list, description="HTTPS/security issues"
    )
    
    # Structured data
    schema_errors: List[str] = Field(
        default_factory=list, description="Schema markup errors"
    )
    
    # Issue summary
    critical_issues: int = Field(
        default=0, description="Number of critical issues"
    )
    warning_issues: int = Field(
        default=0, description="Number of warning issues"
    )
    info_issues: int = Field(
        default=0, description="Number of info issues"
    )
    
    # Overall health score
    technical_health_score: Optional[float] = Field(
        default=None, description="Overall technical health (0-100)"
    )
    
    # Audit metadata
    audited_at: datetime = Field(
        default_factory=datetime.utcnow, description="Audit timestamp"
    )
    audit_duration: Optional[float] = Field(
        default=None, description="Audit duration in seconds"
    )
    pages_audited: int = Field(
        default=1, description="Number of pages audited"
    )


class SEOProject(BaseModel):
    """SEO project container."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid",
    )
    
    # Project info
    id: UUID = Field(default_factory=uuid4, description="Project identifier")
    name: str = Field(description="Project name")
    description: str = Field(description="Project description")
    
    # Target information
    domain: str = Field(description="Target domain")
    target_urls: List[str] = Field(
        default_factory=list, description="Target URLs"
    )
    target_keywords: List[str] = Field(
        default_factory=list, description="Target keywords"
    )
    
    # Project settings
    search_engines: List[SearchEngine] = Field(
        default_factory=lambda: [SearchEngine.GOOGLE],
        description="Target search engines"
    )
    locations: List[str] = Field(
        default_factory=list, description="Target locations"
    )
    languages: List[str] = Field(
        default_factory=lambda: ["en"], description="Target languages"
    )
    
    # Project status
    is_active: bool = Field(default=True, description="Project active status")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Creation timestamp"
    )
    updated_at: Optional[datetime] = Field(
        default=None, description="Last update timestamp"
    )
    
    # Configuration
    config: Dict[str, Any] = Field(
        default_factory=dict, description="Project configuration"
    )
    tags: List[str] = Field(default_factory=list, description="Project tags")
