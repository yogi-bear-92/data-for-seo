"""Test basic functionality of SEO agents."""

import asyncio
import sys
import os
from unittest.mock import AsyncMock, Mock, patch
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_for_seo.agents.seo_collector import SEOCollectorAgent
from data_for_seo.agents.seo_processor import SEOProcessorAgent
from data_for_seo.models.base import SEOTask, ExecutionResult
from data_for_seo.tools.dataforseo_client import DataForSEOClient, AsyncRateLimiter


class TestSEOCollectorAgent:
    """Test SEO Collector Agent functionality."""
    
    def test_agent_initialization(self):
        """Test agent initializes correctly."""
        agent = SEOCollectorAgent()
        
        assert agent.name == "SEO Collector"
        assert agent.agent_type == "seo_collector"
        assert agent.is_active is True
        
    def test_supported_task_types(self):
        """Test agent supports correct task types."""
        agent = SEOCollectorAgent()
        supported_types = agent.get_supported_task_types()
        
        expected_types = [
            "keyword_research",
            "serp_analysis", 
            "ranking_data",
            "competitor_analysis",
        ]
        
        assert set(supported_types) == set(expected_types)
    
    async def test_validate_task(self):
        """Test task validation."""
        agent = SEOCollectorAgent()
        
        # Valid task
        valid_task = SEOTask(
            name="Test keyword research",
            description="Test task",
            task_type="keyword_research"
        )
        
        assert await agent.validate_task(valid_task) is True
        
        # Invalid task type
        invalid_task = SEOTask(
            name="Test invalid task",
            description="Test task",
            task_type="invalid_type"
        )
        
        assert await agent.validate_task(invalid_task) is False
    
    async def test_keyword_research_task_validation(self):
        """Test keyword research task parameter validation."""
        agent = SEOCollectorAgent()
        
        # Task without keywords should fail
        task_no_keywords = SEOTask(
            name="Test keyword research",
            description="Test task",
            task_type="keyword_research",
            parameters={}
        )
        
        result = await agent._execute_task_impl(task_no_keywords)
        assert result.success is False
        assert "keywords" in result.message.lower()
    
    async def test_serp_analysis_task_validation(self):
        """Test SERP analysis task parameter validation."""
        agent = SEOCollectorAgent()
        
        # Task without keyword should fail
        task_no_keyword = SEOTask(
            name="Test SERP analysis",
            description="Test task",
            task_type="serp_analysis",
            parameters={}
        )
        
        result = await agent._execute_task_impl(task_no_keyword)
        assert result.success is False
        assert "keyword" in result.message.lower()


class TestSEOProcessorAgent:
    """Test SEO Processor Agent functionality."""
    
    def test_agent_initialization(self):
        """Test agent initializes correctly."""
        agent = SEOProcessorAgent()
        
        assert agent.name == "SEO Processor"
        assert agent.agent_type == "seo_processor"
        assert agent.is_active is True
        
    def test_supported_task_types(self):
        """Test agent supports correct task types."""
        agent = SEOProcessorAgent()
        supported_types = agent.get_supported_task_types()
        
        expected_types = [
            "data_analysis",
            "pattern_recognition",
            "recommendation_generation",
            "report_compilation",
        ]
        
        assert set(supported_types) == set(expected_types)
    
    async def test_data_analysis_task_validation(self):
        """Test data analysis task parameter validation."""
        agent = SEOProcessorAgent()
        
        # Task without data_source should fail
        task_no_data = SEOTask(
            name="Test data analysis",
            description="Test task",
            task_type="data_analysis",
            parameters={}
        )
        
        result = await agent._execute_task_impl(task_no_data)
        assert result.success is False
        assert "data source" in result.message.lower()
    
    def test_keyword_potential_calculation(self):
        """Test keyword potential score calculation."""
        agent = SEOProcessorAgent()
        
        # High potential keyword
        high_potential = {
            "search_volume": 10000,
            "competition": 0.2,
            "cpc": 3.5,
            "keyword_difficulty": "easy"
        }
        
        score = agent._calculate_keyword_potential(high_potential)
        assert score > 70  # Should be high score
        
        # Low potential keyword
        low_potential = {
            "search_volume": 10,
            "competition": 0.9,
            "cpc": 0.1,
            "keyword_difficulty": "very_hard"
        }
        
        score = agent._calculate_keyword_potential(low_potential)
        assert score < 40  # Should be low score


class TestDataForSEOClient:
    """Test Data for SEO client functionality."""
    
    def test_rate_limiter_initialization(self):
        """Test rate limiter initializes correctly."""
        limiter = AsyncRateLimiter(max_requests=100, time_window=60)
        
        assert limiter.max_requests == 100
        assert limiter.time_window == 60
        assert len(limiter.requests) == 0
    
    def test_client_initialization(self):
        """Test client initializes with credentials."""
        client = DataForSEOClient(username="test", password="test")
        
        assert client.username == "test"
        assert client.password == "test"
        assert client.base_url is not None
    
    def test_client_initialization_without_credentials(self):
        """Test client fails without credentials."""
        with patch('data_for_seo.tools.dataforseo_client.get_settings') as mock_settings:
            mock_settings.return_value.dataforseo_username = None
            mock_settings.return_value.dataforseo_password = None
            
            try:
                DataForSEOClient()
                assert False, "Should have raised ValueError"
            except ValueError as e:
                assert "credentials must be provided" in str(e)


class TestAgentIntegration:
    """Test agent integration scenarios."""
    
    async def test_collector_to_processor_workflow(self):
        """Test data flow from collector to processor."""
        collector = SEOCollectorAgent()
        processor = SEOProcessorAgent()
        
        # Mock collector result
        mock_collector_data = {
            "keywords": ["test keyword"],
            "keyword_data": [
                {
                    "keyword": "test keyword",
                    "search_volume": 1000,
                    "competition": 0.5,
                    "cpc": 2.0,
                }
            ],
            "collected_at": datetime.utcnow().isoformat(),
        }
        
        # Create processor task with collector data
        processor_task = SEOTask(
            name="Process collector data",
            description="Process SEO data from collector",
            task_type="data_analysis",
            parameters={
                "data_source": mock_collector_data,
                "analysis_type": "keyword_analysis",
                "store_results": False,  # Don't store in vector store for test
            }
        )
        
        # Mock vector store to avoid actual ChromaDB dependency
        with patch.object(processor, '_get_vector_store') as mock_vector_store:
            mock_vector_store.return_value = AsyncMock()
            
            result = await processor._execute_task_impl(processor_task)
            
            assert result.success is True
            assert "keyword_analysis" in result.data
            assert len(result.data["keyword_analysis"]["processed_keywords"]) == 1
    
    def test_workflow_task_creation(self):
        """Test workflow task creation."""
        # Test that we can create properly structured tasks
        keyword_task = SEOTask(
            name="Keyword research",
            description="Collect keyword data",
            task_type="keyword_research",
            parameters={
                "keywords": ["seo tools", "keyword research"],
                "include_metrics": True,
                "include_ideas": True,
            },
            tags=["workflow", "keyword_research"],
        )
        
        assert keyword_task.task_type == "keyword_research"
        assert len(keyword_task.parameters["keywords"]) == 2
        assert keyword_task.parameters["include_metrics"] is True
        
        # Test processor task
        analysis_task = SEOTask(
            name="Data analysis",
            description="Analyze collected data",
            task_type="data_analysis",
            parameters={
                "data_source": {"test": "data"},
                "analysis_type": "comprehensive",
            },
            tags=["workflow", "analysis"],
        )
        
        assert analysis_task.task_type == "data_analysis"
        assert analysis_task.parameters["analysis_type"] == "comprehensive"


if __name__ == "__main__":
    # Simple test runner for basic validation
    import sys
    import traceback
    
    def run_sync_tests():
        """Run synchronous tests."""
        test_classes = [
            TestSEOCollectorAgent,
            TestSEOProcessorAgent, 
            TestDataForSEOClient,
            TestAgentIntegration,
        ]
        
        passed = 0
        failed = 0
        
        for test_class in test_classes:
            instance = test_class()
            
            # Get all test methods
            test_methods = [
                method for method in dir(instance)
                if method.startswith('test_') and callable(getattr(instance, method))
            ]
            
            for method_name in test_methods:
                try:
                    method = getattr(instance, method_name)
                    
                    # Skip async tests in simple runner
                    if asyncio.iscoroutinefunction(method):
                        continue
                        
                    method()
                    print(f"✓ {test_class.__name__}::{method_name}")
                    passed += 1
                    
                except Exception as e:
                    print(f"✗ {test_class.__name__}::{method_name}: {e}")
                    traceback.print_exc()
                    failed += 1
        
        print(f"\nResults: {passed} passed, {failed} failed")
        return failed == 0
    
    async def run_async_tests():
        """Run asynchronous tests."""
        test_classes = [
            TestSEOCollectorAgent,
            TestSEOProcessorAgent,
            TestAgentIntegration,
        ]
        
        passed = 0
        failed = 0
        
        for test_class in test_classes:
            instance = test_class()
            
            # Get all async test methods
            test_methods = [
                method for method in dir(instance)
                if method.startswith('test_') and callable(getattr(instance, method))
                and asyncio.iscoroutinefunction(getattr(instance, method))
            ]
            
            for method_name in test_methods:
                try:
                    method = getattr(instance, method_name)
                    await method()
                    print(f"✓ {test_class.__name__}::{method_name}")
                    passed += 1
                    
                except Exception as e:
                    print(f"✗ {test_class.__name__}::{method_name}: {e}")
                    traceback.print_exc()
                    failed += 1
        
        print(f"\nAsync Results: {passed} passed, {failed} failed")
        return failed == 0
    
    print("Running synchronous tests...")
    sync_success = run_sync_tests()
    
    print("\nRunning asynchronous tests...")
    async_success = asyncio.run(run_async_tests())
    
    success = sync_success and async_success
    print(f"\nOverall: {'PASSED' if success else 'FAILED'}")
    sys.exit(0 if success else 1)