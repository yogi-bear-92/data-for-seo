"""Unit tests for SEO Analyzer Agent."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

from src.data_for_seo.agents.seo_analyzer import SEOAnalyzerAgent
from src.data_for_seo.models.base import ExecutionResult, SEOTask, TaskPriority
from src.data_for_seo.models.seo import SEOAnalysis


class TestSEOAnalyzerAgent:
    """Test SEOAnalyzerAgent class."""
    
    def test_agent_initialization(self):
        """Test SEOAnalyzerAgent initialization."""
        agent = SEOAnalyzerAgent()
        
        assert agent.name == "SEO Analyzer"
        assert agent.description == "Performs comprehensive SEO analysis including content, technical, and performance metrics"
        assert agent.agent_type == "seo_analyzer"
        assert agent.is_active is True
        assert isinstance(agent.config, dict)
    
    def test_agent_initialization_with_config(self):
        """Test SEOAnalyzerAgent initialization with custom config."""
        config = {"test_mode": True, "timeout": 30}
        agent = SEOAnalyzerAgent(config=config)
        
        assert agent.config == config
        assert agent.config["test_mode"] is True
        assert agent.config["timeout"] == 30
    
    def test_get_supported_task_types(self):
        """Test get_supported_task_types method."""
        agent = SEOAnalyzerAgent()
        supported_types = agent.get_supported_task_types()
        
        expected_types = [
            "seo_analysis",
            "page_analysis",
            "content_analysis",
            "technical_analysis",
            "performance_analysis",
        ]
        
        assert supported_types == expected_types
    
    @pytest.mark.asyncio
    async def test_validate_task_supported_type(self):
        """Test task validation for supported task types."""
        agent = SEOAnalyzerAgent()
        
        task = SEOTask(
            name="Test Analysis",
            description="Test SEO analysis",
            task_type="seo_analysis"
        )
        
        is_valid = await agent.validate_task(task)
        assert is_valid is True
    
    @pytest.mark.asyncio
    async def test_validate_task_unsupported_type(self):
        """Test task validation for unsupported task types."""
        agent = SEOAnalyzerAgent()
        
        task = SEOTask(
            name="Test Task",
            description="Test task",
            task_type="unsupported_task"
        )
        
        is_valid = await agent.validate_task(task)
        assert is_valid is False


class TestSEOAnalyzerAgentTaskExecution:
    """Test task execution methods."""
    
    @pytest.mark.asyncio
    async def test_execute_task_unsupported_type(self):
        """Test execution of unsupported task type."""
        agent = SEOAnalyzerAgent()
        
        task = SEOTask(
            name="Unsupported Task",
            description="Unsupported task type",
            task_type="unsupported_type"
        )
        
        result = await agent._execute_task_impl(task)
        
        assert result.success is False
        assert "Unsupported task type" in result.message
        assert "unsupported_type" in result.errors[0]
    
    @pytest.mark.asyncio
    async def test_execute_seo_analysis_missing_url(self):
        """Test SEO analysis with missing URL parameter."""
        agent = SEOAnalyzerAgent()
        
        task = SEOTask(
            name="SEO Analysis",
            description="SEO analysis without URL",
            task_type="seo_analysis",
            parameters={}  # Missing URL
        )
        
        result = await agent._execute_task_impl(task)
        
        assert result.success is False
        assert "URL parameter is required" in result.message
        assert "Missing 'url' parameter" in result.errors
    
    @pytest.mark.asyncio
    async def test_execute_seo_analysis_invalid_url(self):
        """Test SEO analysis with invalid URL parameter."""
        agent = SEOAnalyzerAgent()
        
        task = SEOTask(
            name="SEO Analysis",
            description="SEO analysis with invalid URL",
            task_type="seo_analysis",
            parameters={"url": "not-a-valid-url"}
        )
        
        result = await agent._execute_task_impl(task)
        
        assert result.success is False
        assert "Invalid URL format" in result.message
        assert "URL validation failed" in result.errors
    
    @pytest.mark.asyncio
    @patch('src.data_for_seo.agents.seo_analyzer.SEOAnalyzerAgent._fetch_page_data')
    async def test_execute_seo_analysis_fetch_failure(self, mock_fetch):
        """Test SEO analysis with page fetch failure."""
        mock_fetch.return_value = None
        
        agent = SEOAnalyzerAgent()
        
        task = SEOTask(
            name="SEO Analysis",
            description="SEO analysis with fetch failure",
            task_type="seo_analysis",
            parameters={"url": "https://example.com"}
        )
        
        result = await agent._execute_task_impl(task)
        
        assert result.success is False
        assert "Failed to fetch page data" in result.message
        assert "Page fetch failed" in result.errors
    
    @pytest.mark.asyncio
    @patch('src.data_for_seo.agents.seo_analyzer.SEOAnalyzerAgent._fetch_page_data')
    @patch('src.data_for_seo.agents.seo_analyzer.SEOAnalyzerAgent._extract_content_metrics')
    @patch('src.data_for_seo.agents.seo_analyzer.SEOAnalyzerAgent._extract_technical_metrics')
    @patch('src.data_for_seo.agents.seo_analyzer.SEOAnalyzerAgent._extract_performance_metrics')
    async def test_execute_seo_analysis_success(self, mock_performance, mock_technical, mock_content, mock_fetch):
        """Test successful SEO analysis execution."""
        # Mock the page data
        mock_fetch.return_value = {
            "content": "<html><head><title>Test</title></head><body>Content</body></html>",
            "status_code": 200,
            "headers": {"content-type": "text/html"},
            "response_time": 0.5
        }
        
        # Mock the analysis methods
        mock_content.return_value = {
            "title": "Test Page",
            "meta_description": "Test description",
            "word_count": 100,
            "heading_structure": {"h1": 1},
            "keyword_density": {"test": 2.0}
        }
        
        mock_technical.return_value = {
            "https_enabled": True,
            "mobile_friendly": True,
            "internal_links": 5,
            "external_links": 2,
            "broken_links": [],
            "images_count": 3,
            "images_without_alt": 1,
            "schema_markup": ["WebPage"]
        }
        
        mock_performance.return_value = {
            "page_load_time": 1.2,
            "first_contentful_paint": 0.8,
            "largest_contentful_paint": 1.5
        }
        
        agent = SEOAnalyzerAgent()
        
        task = SEOTask(
            name="SEO Analysis",
            description="Comprehensive SEO analysis",
            task_type="seo_analysis",
            parameters={"url": "https://example.com"}
        )
        
        result = await agent._execute_task_impl(task)
        
        assert result.success is True
        assert "SEO analysis completed" in result.message
        assert "analysis" in result.data
        assert "recommendations" in result.data
        
        # Verify the analysis data structure
        analysis_data = result.data["analysis"]
        assert analysis_data["url"] == "https://example.com"
        assert analysis_data["title"] == "Test Page"
        assert analysis_data["https_enabled"] is True
        assert analysis_data["seo_score"] is not None


class TestSEOAnalyzerAgentHelperMethods:
    """Test helper methods of SEOAnalyzerAgent."""
    
    def test_validate_url_valid(self):
        """Test URL validation with valid URLs."""
        agent = SEOAnalyzerAgent()
        
        valid_urls = [
            "https://example.com",
            "http://example.com",
            "https://subdomain.example.com/path",
            "https://example.com:8080",
        ]
        
        for url in valid_urls:
            assert agent.validate_url(url) is True
    
    def test_validate_url_invalid(self):
        """Test URL validation with invalid URLs."""
        agent = SEOAnalyzerAgent()
        
        invalid_urls = [
            "not-a-url",
            "ftp://example.com",  # Different scheme
            "",
            "example.com",  # Missing scheme
            "http://",  # Missing netloc
        ]
        
        for url in invalid_urls:
            assert agent.validate_url(url) is False
    
    def test_validate_keyword_valid(self):
        """Test keyword validation with valid keywords."""
        agent = SEOAnalyzerAgent()
        
        valid_keywords = [
            "test",
            "test keyword",
            "long tail keyword phrase",
            "SEO",
            "123",
        ]
        
        for keyword in valid_keywords:
            assert agent.validate_keyword(keyword) is True
    
    def test_validate_keyword_invalid(self):
        """Test keyword validation with invalid keywords."""
        agent = SEOAnalyzerAgent()
        
        invalid_keywords = [
            "",
            "   ",  # Only whitespace
            None,
            123,  # Not a string
            "a" * 201,  # Too long
        ]
        
        for keyword in invalid_keywords:
            assert agent.validate_keyword(keyword) is False
    
    def test_extract_domain_valid(self):
        """Test domain extraction from valid URLs."""
        agent = SEOAnalyzerAgent()
        
        test_cases = [
            ("https://example.com", "example.com"),
            ("http://subdomain.example.com", "subdomain.example.com"),
            ("https://example.com:8080/path", "example.com:8080"),
            ("https://Example.COM", "example.com"),  # Case insensitive
        ]
        
        for url, expected_domain in test_cases:
            assert agent.extract_domain(url) == expected_domain
    
    def test_extract_domain_invalid(self):
        """Test domain extraction from invalid URLs."""
        agent = SEOAnalyzerAgent()
        
        invalid_urls = [
            "not-a-url",
            "",
            None,
        ]
        
        for url in invalid_urls:
            assert agent.extract_domain(url) is None
    
    @pytest.mark.asyncio
    @patch('aiohttp.ClientSession.get')
    async def test_fetch_page_data_success(self, mock_get):
        """Test successful page data fetching."""
        # Mock aiohttp response
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text.return_value = "<html><body>Test</body></html>"
        mock_response.headers = {"content-type": "text/html"}
        mock_response.url = "https://example.com"
        
        mock_get.return_value.__aenter__.return_value = mock_response
        
        agent = SEOAnalyzerAgent()
        
        result = await agent._fetch_page_data("https://example.com")
        
        assert result is not None
        assert result["status_code"] == 200
        assert result["content"] == "<html><body>Test</body></html>"
        assert "response_time" in result
        assert result["url"] == "https://example.com"
    
    @pytest.mark.asyncio
    @patch('aiohttp.ClientSession.get')
    async def test_fetch_page_data_failure(self, mock_get):
        """Test page data fetching failure."""
        # Mock aiohttp to raise an exception
        mock_get.side_effect = Exception("Connection error")
        
        agent = SEOAnalyzerAgent()
        
        result = await agent._fetch_page_data("https://example.com")
        
        assert result is None
    
    def test_extract_title(self, sample_html_content):
        """Test title extraction from HTML."""
        from bs4 import BeautifulSoup
        
        agent = SEOAnalyzerAgent()
        soup = BeautifulSoup(sample_html_content, "html.parser")
        
        title = agent._extract_title(soup)
        
        assert title == "Test Page Title for SEO Analysis"
    
    def test_extract_title_missing(self):
        """Test title extraction when title tag is missing."""
        from bs4 import BeautifulSoup
        
        agent = SEOAnalyzerAgent()
        soup = BeautifulSoup("<html><body>No title</body></html>", "html.parser")
        
        title = agent._extract_title(soup)
        
        assert title is None
    
    def test_extract_meta_description(self, sample_html_content):
        """Test meta description extraction from HTML."""
        from bs4 import BeautifulSoup
        
        agent = SEOAnalyzerAgent()
        soup = BeautifulSoup(sample_html_content, "html.parser")
        
        meta_desc = agent._extract_meta_description(soup)
        
        assert meta_desc == "This is a test page for SEO analysis with proper meta description length."
    
    def test_extract_meta_description_missing(self):
        """Test meta description extraction when meta tag is missing."""
        from bs4 import BeautifulSoup
        
        agent = SEOAnalyzerAgent()
        soup = BeautifulSoup("<html><head><title>Test</title></head><body>Content</body></html>", "html.parser")
        
        meta_desc = agent._extract_meta_description(soup)
        
        assert meta_desc is None
    
    def test_count_words(self, sample_html_content):
        """Test word counting in HTML content."""
        from bs4 import BeautifulSoup
        
        agent = SEOAnalyzerAgent()
        soup = BeautifulSoup(sample_html_content, "html.parser")
        
        word_count = agent._count_words(soup)
        
        assert word_count > 0
        assert isinstance(word_count, int)
    
    def test_extract_heading_structure(self, sample_html_content):
        """Test heading structure extraction."""
        from bs4 import BeautifulSoup
        
        agent = SEOAnalyzerAgent()
        soup = BeautifulSoup(sample_html_content, "html.parser")
        
        structure = agent._extract_heading_structure(soup)
        
        assert isinstance(structure, dict)
        assert structure["h1"] == 1  # One H1 in sample content
        assert structure["h2"] == 2  # Two H2s in sample content
        assert structure["h3"] == 1  # One H3 in sample content
        assert structure["h4"] == 0  # No H4s in sample content
    
    def test_calculate_keyword_density(self):
        """Test keyword density calculation."""
        from bs4 import BeautifulSoup
        
        agent = SEOAnalyzerAgent()
        
        # Create simple HTML with known word frequencies
        html_content = """
        <html>
        <body>
            <p>Test keyword appears test multiple times. The test word is repeated test again.</p>
        </body>
        </html>
        """
        
        soup = BeautifulSoup(html_content, "html.parser")
        density = agent._calculate_keyword_density(soup)
        
        assert isinstance(density, dict)
        assert "test" in density
        assert density["test"] > 0  # Should have some density for "test"
    
    def test_calculate_seo_score(self):
        """Test SEO score calculation."""
        agent = SEOAnalyzerAgent()
        
        content_data = {
            "title": "Good Title",
            "meta_description": "Good meta description with proper length for SEO testing",
            "word_count": 500,
            "heading_structure": {"h1": 1, "h2": 3}
        }
        
        technical_data = {
            "https_enabled": True,
            "mobile_friendly": True,
            "images_count": 5,
            "images_without_alt": 0,
            "internal_links": 10,
            "schema_markup": ["WebPage"]
        }
        
        performance_data = {
            "page_load_time": 1.5,
            "content_size": 500000
        }
        
        score = agent._calculate_seo_score(content_data, technical_data, performance_data)
        
        assert isinstance(score, float)
        assert 0 <= score <= 100
    
    def test_calculate_content_score(self):
        """Test content score calculation."""
        agent = SEOAnalyzerAgent()
        
        content_data = {
            "title": "Optimal Length Title for SEO Testing",  # Good length
            "meta_description": "This is a meta description with optimal length for search engine optimization testing purposes.",  # Good length
            "word_count": 600,  # Good word count
            "heading_structure": {"h1": 1, "h2": 3, "h3": 2}  # Good structure
        }
        
        score = agent._calculate_content_score(content_data)
        
        assert isinstance(score, float)
        assert score > 50  # Should be good score with optimal content
    
    def test_calculate_technical_score(self):
        """Test technical score calculation."""
        agent = SEOAnalyzerAgent()
        
        technical_data = {
            "https_enabled": True,
            "mobile_friendly": True,
            "images_count": 10,
            "images_without_alt": 2,  # 80% have alt text
            "internal_links": 15,
            "schema_markup": ["WebPage", "Article"]
        }
        
        score = agent._calculate_technical_score(technical_data)
        
        assert isinstance(score, float)
        assert score > 50  # Should be good score with most technical aspects covered
    
    def test_calculate_performance_score(self):
        """Test performance score calculation."""
        agent = SEOAnalyzerAgent()
        
        # Good performance
        score = agent._calculate_performance_score(1.0, 500000)  # 1s, 500KB
        assert score > 80
        
        # Poor performance
        score = agent._calculate_performance_score(5.0, 5000000)  # 5s, 5MB
        assert score < 50
    
    def test_generate_recommendations(self, sample_seo_analysis):
        """Test recommendation generation."""
        agent = SEOAnalyzerAgent()
        
        recommendations = agent._generate_recommendations(sample_seo_analysis)
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        
        # Check recommendation structure
        for rec in recommendations:
            assert "type" in rec
            assert "priority" in rec
            assert "message" in rec
            assert "description" in rec
    
    def test_generate_recommendations_missing_title(self):
        """Test recommendations for missing title."""
        from src.data_for_seo.models.seo import SEOAnalysis
        
        agent = SEOAnalyzerAgent()
        
        analysis = SEOAnalysis(
            url="https://example.com",
            title=None,  # Missing title
            meta_description="Good meta description"
        )
        
        recommendations = agent._generate_recommendations(analysis)
        
        # Should have recommendation for missing title
        title_recs = [r for r in recommendations if r["type"] == "title"]
        assert len(title_recs) > 0
        assert title_recs[0]["priority"] == "high"
    
    def test_check_https(self):
        """Test HTTPS checking."""
        agent = SEOAnalyzerAgent()
        
        assert agent._check_https("https://example.com") is True
        assert agent._check_https("http://example.com") is False
    
    def test_check_viewport_meta(self):
        """Test viewport meta tag checking."""
        from bs4 import BeautifulSoup
        
        agent = SEOAnalyzerAgent()
        
        # HTML with viewport
        html_with_viewport = """
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body></body>
        </html>
        """
        
        soup = BeautifulSoup(html_with_viewport, "html.parser")
        assert agent._check_viewport_meta(soup) is True
        
        # HTML without viewport
        html_without_viewport = "<html><head></head><body></body></html>"
        soup = BeautifulSoup(html_without_viewport, "html.parser")
        assert agent._check_viewport_meta(soup) is False


class TestSEOAnalyzerAgentIntegration:
    """Integration tests for SEOAnalyzerAgent with mocked external dependencies."""
    
    @pytest.mark.asyncio
    @patch('aiohttp.ClientSession')
    async def test_full_seo_analysis_workflow(self, mock_session, sample_html_content):
        """Test complete SEO analysis workflow with mocked HTTP client."""
        # Mock aiohttp session and response
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text.return_value = sample_html_content
        mock_response.headers = {"content-type": "text/html"}
        mock_response.url = "https://example.com"
        
        mock_session_instance = AsyncMock()
        mock_session_instance.get.return_value.__aenter__.return_value = mock_response
        mock_session.return_value.__aenter__.return_value = mock_session_instance
        
        agent = SEOAnalyzerAgent()
        
        task = SEOTask(
            name="Full SEO Analysis",
            description="Complete SEO analysis test",
            task_type="seo_analysis",
            parameters={
                "url": "https://example.com",
                "target_keywords": ["test", "seo", "analysis"]
            }
        )
        
        result = await agent.execute_task(task)
        
        assert result.success is True
        assert "analysis" in result.data
        assert "recommendations" in result.data
        assert result.execution_time is not None
        assert result.execution_time > 0
        
        # Verify task status changes
        assert task.status.value in ["completed", "failed"]
        assert task.result is not None
    
    @pytest.mark.asyncio
    async def test_health_check(self):
        """Test agent health check."""
        agent = SEOAnalyzerAgent()
        
        health = await agent.health_check()
        
        assert isinstance(health, dict)
        assert "agent_id" in health
        assert "name" in health
        assert "type" in health
        assert "status" in health
        assert health["name"] == "SEO Analyzer"
        assert health["type"] == "seo_analyzer"
        assert health["status"] == "healthy"
    
    @pytest.mark.asyncio
    async def test_get_metrics(self):
        """Test agent metrics retrieval."""
        agent = SEOAnalyzerAgent()
        
        metrics = await agent.get_metrics()
        
        assert isinstance(metrics, dict)
        assert "tasks_executed" in metrics
        assert "success_rate" in metrics
        assert "average_execution_time" in metrics
        assert "last_activity" in metrics
    
    def test_update_config(self):
        """Test agent configuration update."""
        agent = SEOAnalyzerAgent(config={"initial": "value"})
        
        new_config = {"timeout": 60, "retries": 3}
        agent.update_config(new_config)
        
        assert agent.config["timeout"] == 60
        assert agent.config["retries"] == 3
        assert agent.config["initial"] == "value"  # Original config preserved
    
    def test_activate_deactivate(self):
        """Test agent activation and deactivation."""
        agent = SEOAnalyzerAgent()
        
        assert agent.is_active is True
        
        agent.deactivate()
        assert agent.is_active is False
        
        agent.activate()
        assert agent.is_active is True
    
    @pytest.mark.asyncio
    async def test_shutdown(self):
        """Test agent shutdown."""
        agent = SEOAnalyzerAgent()
        
        assert agent.is_active is True
        
        await agent.shutdown()
        
        assert agent.is_active is False