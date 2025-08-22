"""Unit tests for SEO-specific models."""

import pytest
from datetime import datetime
from uuid import UUID

from src.data_for_seo.models.seo import (
    AuditSeverity,
    ContentOptimization,
    ContentType,
    KeywordData,
    KeywordDifficulty,
    RankingData,
    SearchEngine,
    SEOAnalysis,
    SEOProject,
    TechnicalAudit,
)


class TestSearchEngine:
    """Test SearchEngine enum."""
    
    def test_search_engine_values(self):
        """Test SearchEngine enum values."""
        assert SearchEngine.GOOGLE == "google"
        assert SearchEngine.BING == "bing"
        assert SearchEngine.YAHOO == "yahoo"
        assert SearchEngine.YANDEX == "yandex"
        assert SearchEngine.BAIDU == "baidu"


class TestKeywordDifficulty:
    """Test KeywordDifficulty enum."""
    
    def test_keyword_difficulty_values(self):
        """Test KeywordDifficulty enum values."""
        assert KeywordDifficulty.VERY_EASY == "very_easy"
        assert KeywordDifficulty.EASY == "easy"
        assert KeywordDifficulty.MEDIUM == "medium"
        assert KeywordDifficulty.HARD == "hard"
        assert KeywordDifficulty.VERY_HARD == "very_hard"


class TestContentType:
    """Test ContentType enum."""
    
    def test_content_type_values(self):
        """Test ContentType enum values."""
        assert ContentType.WEBPAGE == "webpage"
        assert ContentType.BLOG_POST == "blog_post"
        assert ContentType.PRODUCT_PAGE == "product_page"
        assert ContentType.CATEGORY_PAGE == "category_page"
        assert ContentType.LANDING_PAGE == "landing_page"


class TestAuditSeverity:
    """Test AuditSeverity enum."""
    
    def test_audit_severity_values(self):
        """Test AuditSeverity enum values."""
        assert AuditSeverity.INFO == "info"
        assert AuditSeverity.WARNING == "warning"
        assert AuditSeverity.ERROR == "error"
        assert AuditSeverity.CRITICAL == "critical"


class TestKeywordData:
    """Test KeywordData model."""
    
    def test_keyword_data_creation(self):
        """Test KeywordData creation."""
        keyword_data = KeywordData(
            keyword="test keyword",
            search_volume=1000,
            keyword_difficulty=KeywordDifficulty.MEDIUM,
            cpc=1.25,
            competition=0.65,
            current_position=5,
            previous_position=7,
            position_change=2,
            search_engine=SearchEngine.GOOGLE,
            location="United States",
            language="en",
            related_keywords=["related 1", "related 2"],
            long_tail_keywords=["long tail 1", "long tail 2"],
            url="https://example.com/test"
        )
        
        assert keyword_data.keyword == "test keyword"
        assert keyword_data.search_volume == 1000
        assert keyword_data.keyword_difficulty == KeywordDifficulty.MEDIUM
        assert keyword_data.cpc == 1.25
        assert keyword_data.competition == 0.65
        assert keyword_data.current_position == 5
        assert keyword_data.previous_position == 7
        assert keyword_data.position_change == 2
        assert keyword_data.search_engine == SearchEngine.GOOGLE
        assert keyword_data.location == "United States"
        assert keyword_data.language == "en"
        assert keyword_data.related_keywords == ["related 1", "related 2"]
        assert keyword_data.long_tail_keywords == ["long tail 1", "long tail 2"]
        assert str(keyword_data.url) == "https://example.com/test"
        assert isinstance(keyword_data.last_updated, datetime)
    
    def test_keyword_data_defaults(self):
        """Test KeywordData with default values."""
        keyword_data = KeywordData(keyword="basic keyword")
        
        assert keyword_data.keyword == "basic keyword"
        assert keyword_data.search_volume is None
        assert keyword_data.keyword_difficulty is None
        assert keyword_data.cpc is None
        assert keyword_data.competition is None
        assert keyword_data.current_position is None
        assert keyword_data.previous_position is None
        assert keyword_data.position_change is None
        assert keyword_data.search_engine == SearchEngine.GOOGLE
        assert keyword_data.location is None
        assert keyword_data.language == "en"
        assert keyword_data.related_keywords == []
        assert keyword_data.long_tail_keywords == []
        assert keyword_data.url is None
        assert isinstance(keyword_data.last_updated, datetime)
    
    def test_position_trend_property(self):
        """Test position_trend property."""
        # Improving trend
        keyword_data = KeywordData(keyword="test", position_change=3)
        assert keyword_data.position_trend == "improving"
        
        # Declining trend
        keyword_data = KeywordData(keyword="test", position_change=-2)
        assert keyword_data.position_trend == "declining"
        
        # Stable trend
        keyword_data = KeywordData(keyword="test", position_change=0)
        assert keyword_data.position_trend == "stable"
        
        # No change data
        keyword_data = KeywordData(keyword="test")
        assert keyword_data.position_trend == "stable"


class TestRankingData:
    """Test RankingData model."""
    
    def test_ranking_data_creation(self):
        """Test RankingData creation."""
        ranking_data = RankingData(
            url="https://example.com/test",
            keyword="test keyword",
            position=3,
            search_engine=SearchEngine.GOOGLE,
            location="United States",
            device_type="mobile",
            featured_snippet=True,
            local_pack=False,
            image_pack=True,
            video_results=False,
            click_through_rate=0.15,
            impressions=1500,
            clicks=225,
            position_history=[
                {"date": "2024-01-01", "position": 5},
                {"date": "2024-01-02", "position": 3},
            ]
        )
        
        assert str(ranking_data.url) == "https://example.com/test"
        assert ranking_data.keyword == "test keyword"
        assert ranking_data.position == 3
        assert ranking_data.search_engine == SearchEngine.GOOGLE
        assert ranking_data.location == "United States"
        assert ranking_data.device_type == "mobile"
        assert ranking_data.featured_snippet is True
        assert ranking_data.local_pack is False
        assert ranking_data.image_pack is True
        assert ranking_data.video_results is False
        assert ranking_data.click_through_rate == 0.15
        assert ranking_data.impressions == 1500
        assert ranking_data.clicks == 225
        assert len(ranking_data.position_history) == 2
        assert isinstance(ranking_data.tracked_since, datetime)
        assert isinstance(ranking_data.last_checked, datetime)
    
    def test_ranking_data_defaults(self):
        """Test RankingData with default values."""
        ranking_data = RankingData(
            url="https://example.com",
            keyword="test",
            position=1
        )
        
        assert ranking_data.search_engine == SearchEngine.GOOGLE
        assert ranking_data.location is None
        assert ranking_data.device_type == "desktop"
        assert ranking_data.featured_snippet is False
        assert ranking_data.local_pack is False
        assert ranking_data.image_pack is False
        assert ranking_data.video_results is False
        assert ranking_data.click_through_rate is None
        assert ranking_data.impressions is None
        assert ranking_data.clicks is None
        assert ranking_data.position_history == []


class TestSEOAnalysis:
    """Test SEOAnalysis model."""
    
    def test_seo_analysis_creation(self):
        """Test SEOAnalysis creation."""
        analysis = SEOAnalysis(
            url="https://example.com/test",
            title="Test Page Title",
            meta_description="Test meta description",
            word_count=500,
            heading_structure={"h1": 1, "h2": 3, "h3": 5},
            keyword_density={"test": 2.5, "keyword": 1.8},
            page_load_time=1.5,
            mobile_friendly=True,
            https_enabled=True,
            internal_links=10,
            external_links=5,
            broken_links=["https://broken.com"],
            images_count=8,
            images_without_alt=2,
            schema_markup=["Article", "WebPage"],
            seo_score=85.5,
            content_score=78.2,
            technical_score=92.1,
            analysis_duration=3.45
        )
        
        assert str(analysis.url) == "https://example.com/test"
        assert analysis.title == "Test Page Title"
        assert analysis.meta_description == "Test meta description"
        assert analysis.word_count == 500
        assert analysis.heading_structure == {"h1": 1, "h2": 3, "h3": 5}
        assert analysis.keyword_density == {"test": 2.5, "keyword": 1.8}
        assert analysis.page_load_time == 1.5
        assert analysis.mobile_friendly is True
        assert analysis.https_enabled is True
        assert analysis.internal_links == 10
        assert analysis.external_links == 5
        assert analysis.broken_links == ["https://broken.com"]
        assert analysis.images_count == 8
        assert analysis.images_without_alt == 2
        assert analysis.schema_markup == ["Article", "WebPage"]
        assert analysis.seo_score == 85.5
        assert analysis.content_score == 78.2
        assert analysis.technical_score == 92.1
        assert analysis.analysis_duration == 3.45
        assert isinstance(analysis.analyzed_at, datetime)
    
    def test_seo_analysis_defaults(self):
        """Test SEOAnalysis with default values."""
        analysis = SEOAnalysis(url="https://example.com")
        
        assert analysis.title is None
        assert analysis.meta_description is None
        assert analysis.word_count is None
        assert analysis.heading_structure == {}
        assert analysis.keyword_density == {}
        assert analysis.page_load_time is None
        assert analysis.mobile_friendly is None
        assert analysis.https_enabled is False
        assert analysis.internal_links == 0
        assert analysis.external_links == 0
        assert analysis.broken_links == []
        assert analysis.images_count == 0
        assert analysis.images_without_alt == 0
        assert analysis.schema_markup == []
        assert analysis.seo_score is None
        assert analysis.content_score is None
        assert analysis.technical_score is None
        assert analysis.analysis_duration is None


class TestContentOptimization:
    """Test ContentOptimization model."""
    
    def test_content_optimization_creation(self):
        """Test ContentOptimization creation."""
        optimization = ContentOptimization(
            url="https://example.com/blog/post",
            content_type=ContentType.BLOG_POST,
            target_keywords=["seo", "optimization", "content"],
            current_title="Current Blog Post Title",
            current_meta_description="Current meta description",
            current_word_count=750,
            title_recommendations=["Include primary keyword", "Keep under 60 chars"],
            meta_description_recommendations=["Add call to action", "Include secondary keyword"],
            content_recommendations=["Add more internal links", "Improve readability"],
            keyword_recommendations=["Increase keyword density", "Add LSI keywords"],
            suggested_title="Optimized Blog Post Title for SEO",
            suggested_meta_description="Optimized meta description with keywords and CTA",
            suggested_headings=["H1: Main Topic", "H2: Subtopic 1", "H2: Subtopic 2"],
            competitor_urls=["https://competitor1.com", "https://competitor2.com"],
            content_gaps=["Missing section on advanced techniques", "No case studies"],
            priority_score=0.85,
            estimated_impact="high"
        )
        
        assert str(optimization.url) == "https://example.com/blog/post"
        assert optimization.content_type == ContentType.BLOG_POST
        assert optimization.target_keywords == ["seo", "optimization", "content"]
        assert optimization.current_title == "Current Blog Post Title"
        assert optimization.current_meta_description == "Current meta description"
        assert optimization.current_word_count == 750
        assert len(optimization.title_recommendations) == 2
        assert len(optimization.meta_description_recommendations) == 2
        assert len(optimization.content_recommendations) == 2
        assert len(optimization.keyword_recommendations) == 2
        assert optimization.suggested_title == "Optimized Blog Post Title for SEO"
        assert optimization.suggested_meta_description == "Optimized meta description with keywords and CTA"
        assert len(optimization.suggested_headings) == 3
        assert len(optimization.competitor_urls) == 2
        assert len(optimization.content_gaps) == 2
        assert optimization.priority_score == 0.85
        assert optimization.estimated_impact == "high"
        assert isinstance(optimization.created_at, datetime)
        assert optimization.updated_at is None
    
    def test_content_optimization_defaults(self):
        """Test ContentOptimization with default values."""
        optimization = ContentOptimization(
            url="https://example.com",
            content_type=ContentType.WEBPAGE,
            target_keywords=["test"]
        )
        
        assert optimization.current_title is None
        assert optimization.current_meta_description is None
        assert optimization.current_word_count is None
        assert optimization.title_recommendations == []
        assert optimization.meta_description_recommendations == []
        assert optimization.content_recommendations == []
        assert optimization.keyword_recommendations == []
        assert optimization.suggested_title is None
        assert optimization.suggested_meta_description is None
        assert optimization.suggested_headings == []
        assert optimization.competitor_urls == []
        assert optimization.content_gaps == []
        assert optimization.priority_score == 0.0
        assert optimization.estimated_impact is None


class TestTechnicalAudit:
    """Test TechnicalAudit model."""
    
    def test_technical_audit_creation(self):
        """Test TechnicalAudit creation."""
        audit = TechnicalAudit(
            url="https://example.com",
            audit_type="site",
            page_speed_desktop=85.0,
            page_speed_mobile=78.0,
            first_contentful_paint=1.2,
            largest_contentful_paint=2.5,
            cumulative_layout_shift=0.05,
            robots_txt_exists=True,
            sitemap_exists=True,
            crawl_errors=["404 on /old-page"],
            indexing_issues=["Blocked by robots.txt: /admin"],
            duplicate_content=["/page1", "/page1-copy"],
            missing_meta_descriptions=["/contact", "/about"],
            missing_title_tags=["/terms"],
            broken_internal_links=["/broken-link"],
            mobile_friendly_issues=["Touch targets too small"],
            accessibility_issues=["Missing alt text", "Low contrast"],
            https_issues=["Mixed content warnings"],
            schema_errors=["Invalid JSON-LD syntax"],
            critical_issues=2,
            warning_issues=5,
            info_issues=3,
            technical_health_score=82.5,
            audit_duration=45.67,
            pages_audited=25
        )
        
        assert str(audit.url) == "https://example.com/"
        assert audit.audit_type == "site"
        assert audit.page_speed_desktop == 85.0
        assert audit.page_speed_mobile == 78.0
        assert audit.first_contentful_paint == 1.2
        assert audit.largest_contentful_paint == 2.5
        assert audit.cumulative_layout_shift == 0.05
        assert audit.robots_txt_exists is True
        assert audit.sitemap_exists is True
        assert audit.crawl_errors == ["404 on /old-page"]
        assert audit.indexing_issues == ["Blocked by robots.txt: /admin"]
        assert audit.duplicate_content == ["/page1", "/page1-copy"]
        assert audit.missing_meta_descriptions == ["/contact", "/about"]
        assert audit.missing_title_tags == ["/terms"]
        assert audit.broken_internal_links == ["/broken-link"]
        assert audit.mobile_friendly_issues == ["Touch targets too small"]
        assert audit.accessibility_issues == ["Missing alt text", "Low contrast"]
        assert audit.https_issues == ["Mixed content warnings"]
        assert audit.schema_errors == ["Invalid JSON-LD syntax"]
        assert audit.critical_issues == 2
        assert audit.warning_issues == 5
        assert audit.info_issues == 3
        assert audit.technical_health_score == 82.5
        assert audit.audit_duration == 45.67
        assert audit.pages_audited == 25
        assert isinstance(audit.audited_at, datetime)
    
    def test_technical_audit_defaults(self):
        """Test TechnicalAudit with default values."""
        audit = TechnicalAudit(
            url="https://example.com",
            audit_type="page"
        )
        
        assert audit.page_speed_desktop is None
        assert audit.page_speed_mobile is None
        assert audit.first_contentful_paint is None
        assert audit.largest_contentful_paint is None
        assert audit.cumulative_layout_shift is None
        assert audit.robots_txt_exists is False
        assert audit.sitemap_exists is False
        assert audit.crawl_errors == []
        assert audit.indexing_issues == []
        assert audit.duplicate_content == []
        assert audit.missing_meta_descriptions == []
        assert audit.missing_title_tags == []
        assert audit.broken_internal_links == []
        assert audit.mobile_friendly_issues == []
        assert audit.accessibility_issues == []
        assert audit.https_issues == []
        assert audit.schema_errors == []
        assert audit.critical_issues == 0
        assert audit.warning_issues == 0
        assert audit.info_issues == 0
        assert audit.technical_health_score is None
        assert audit.audit_duration is None
        assert audit.pages_audited == 1


class TestSEOProject:
    """Test SEOProject model."""
    
    def test_seo_project_creation(self):
        """Test SEOProject creation."""
        project = SEOProject(
            name="Example.com SEO Campaign",
            description="Comprehensive SEO optimization for example.com",
            domain="example.com",
            target_urls=["https://example.com", "https://example.com/about"],
            target_keywords=["example", "demo", "test site"],
            search_engines=[SearchEngine.GOOGLE, SearchEngine.BING],
            locations=["United States", "Canada"],
            languages=["en", "fr"],
            config={
                "tracking_frequency": "weekly",
                "competitor_analysis": True,
                "technical_audits": True
            },
            tags=["client-a", "high-priority", "ecommerce"]
        )
        
        assert project.name == "Example.com SEO Campaign"
        assert project.description == "Comprehensive SEO optimization for example.com"
        assert project.domain == "example.com"
        assert project.target_urls == ["https://example.com", "https://example.com/about"]
        assert project.target_keywords == ["example", "demo", "test site"]
        assert project.search_engines == [SearchEngine.GOOGLE, SearchEngine.BING]
        assert project.locations == ["United States", "Canada"]
        assert project.languages == ["en", "fr"]
        assert project.config["tracking_frequency"] == "weekly"
        assert project.config["competitor_analysis"] is True
        assert project.config["technical_audits"] is True
        assert project.tags == ["client-a", "high-priority", "ecommerce"]
        assert project.is_active is True
        assert isinstance(project.id, UUID)
        assert isinstance(project.created_at, datetime)
        assert project.updated_at is None
    
    def test_seo_project_defaults(self):
        """Test SEOProject with default values."""
        project = SEOProject(
            name="Basic Project",
            description="Basic description",
            domain="basic.com"
        )
        
        assert project.target_urls == []
        assert project.target_keywords == []
        assert project.search_engines == [SearchEngine.GOOGLE]
        assert project.locations == []
        assert project.languages == ["en"]
        assert project.is_active is True
        assert project.config == {}
        assert project.tags == []
        assert project.updated_at is None


class TestModelValidation:
    """Test model validation and edge cases."""
    
    def test_invalid_url_validation(self):
        """Test that invalid URLs are rejected."""
        with pytest.raises(ValueError):
            SEOAnalysis(url="not-a-valid-url")
    
    def test_valid_url_formats(self):
        """Test that various valid URL formats are accepted."""
        test_cases = [
            ("https://example.com", "https://example.com/"),
            ("http://example.com", "http://example.com/"),
            ("https://subdomain.example.com/path", "https://subdomain.example.com/path"),
            ("https://example.com:8080/path?param=value", "https://example.com:8080/path?param=value"),
        ]
        
        for input_url, expected_url in test_cases:
            analysis = SEOAnalysis(url=input_url)
            assert str(analysis.url) == expected_url
    
    def test_string_field_stripping(self):
        """Test that string fields are stripped of whitespace."""
        keyword_data = KeywordData(
            keyword="  test keyword  ",
            location="  United States  ",
            language="  en  "
        )
        
        assert keyword_data.keyword == "test keyword"
        assert keyword_data.location == "United States"
        assert keyword_data.language == "en"
    
    def test_list_field_defaults(self):
        """Test that list fields have proper default values."""
        analysis = SEOAnalysis(url="https://example.com")
        
        assert analysis.broken_links == []
        assert analysis.schema_markup == []
        assert isinstance(analysis.broken_links, list)
        assert isinstance(analysis.schema_markup, list)
    
    def test_dict_field_defaults(self):
        """Test that dict fields have proper default values."""
        analysis = SEOAnalysis(url="https://example.com")
        
        assert analysis.heading_structure == {}
        assert analysis.keyword_density == {}
        assert isinstance(analysis.heading_structure, dict)
        assert isinstance(analysis.keyword_density, dict)