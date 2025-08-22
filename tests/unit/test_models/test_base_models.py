"""Unit tests for base models."""

import pytest
from datetime import datetime, timedelta
from uuid import UUID, uuid4

from src.data_for_seo.models.base import (
    BaseAgent,
    ExecutionResult,
    KnowledgeEntry,
    SEOMetrics,
    SEOTask,
    TaskPriority,
    TaskStatus,
)


class TestTaskStatus:
    """Test TaskStatus enum."""
    
    def test_task_status_values(self):
        """Test TaskStatus enum values."""
        assert TaskStatus.PENDING == "pending"
        assert TaskStatus.RUNNING == "running"
        assert TaskStatus.COMPLETED == "completed"
        assert TaskStatus.FAILED == "failed"
        assert TaskStatus.CANCELLED == "cancelled"


class TestTaskPriority:
    """Test TaskPriority enum."""
    
    def test_task_priority_values(self):
        """Test TaskPriority enum values."""
        assert TaskPriority.LOW == "low"
        assert TaskPriority.MEDIUM == "medium"
        assert TaskPriority.HIGH == "high"
        assert TaskPriority.CRITICAL == "critical"


class TestExecutionResult:
    """Test ExecutionResult model."""
    
    def test_execution_result_creation(self):
        """Test ExecutionResult creation."""
        result = ExecutionResult(
            success=True,
            message="Test successful",
            data={"test": "data"},
            execution_time=1.23
        )
        
        assert result.success is True
        assert result.message == "Test successful"
        assert result.data == {"test": "data"}
        assert result.execution_time == 1.23
        assert isinstance(result.timestamp, datetime)
        assert result.errors == []
    
    def test_execution_result_defaults(self):
        """Test ExecutionResult with default values."""
        result = ExecutionResult(
            success=False,
            message="Test failed"
        )
        
        assert result.success is False
        assert result.message == "Test failed"
        assert result.data is None
        assert result.errors == []
        assert result.execution_time is None
        assert isinstance(result.timestamp, datetime)
    
    def test_success_result_factory(self):
        """Test ExecutionResult.success_result factory method."""
        result = ExecutionResult.success_result(
            message="Operation successful",
            data={"key": "value"},
            execution_time=0.5
        )
        
        assert result.success is True
        assert result.message == "Operation successful"
        assert result.data == {"key": "value"}
        assert result.execution_time == 0.5
        assert result.errors == []
    
    def test_failure_result_factory(self):
        """Test ExecutionResult.failure_result factory method."""
        result = ExecutionResult.failure_result(
            message="Operation failed",
            errors=["Error 1", "Error 2"],
            execution_time=0.1
        )
        
        assert result.success is False
        assert result.message == "Operation failed"
        assert result.errors == ["Error 1", "Error 2"]
        assert result.execution_time == 0.1
        assert result.data is None


class TestSEOTask:
    """Test SEOTask model."""
    
    def test_seo_task_creation(self):
        """Test SEOTask creation."""
        task = SEOTask(
            name="Test Task",
            description="Test task description",
            task_type="seo_analysis",
            priority=TaskPriority.HIGH,
            parameters={"url": "https://example.com"},
            tags=["test", "seo"]
        )
        
        assert task.name == "Test Task"
        assert task.description == "Test task description"
        assert task.task_type == "seo_analysis"
        assert task.priority == TaskPriority.HIGH
        assert task.status == TaskStatus.PENDING
        assert task.parameters == {"url": "https://example.com"}
        assert task.tags == ["test", "seo"]
        assert isinstance(task.id, UUID)
        assert isinstance(task.created_at, datetime)
        assert task.started_at is None
        assert task.completed_at is None
        assert task.result is None
    
    def test_seo_task_defaults(self):
        """Test SEOTask with default values."""
        task = SEOTask(
            name="Minimal Task",
            description="Minimal description",
            task_type="basic_task"
        )
        
        assert task.priority == TaskPriority.MEDIUM
        assert task.status == TaskStatus.PENDING
        assert task.parameters == {}
        assert task.tags == []
        assert task.result is None
    
    def test_mark_started(self):
        """Test marking task as started."""
        task = SEOTask(
            name="Test Task",
            description="Test description",
            task_type="test"
        )
        
        assert task.status == TaskStatus.PENDING
        assert task.started_at is None
        
        start_time = datetime.utcnow()
        task.mark_started()
        
        assert task.status == TaskStatus.RUNNING
        assert task.started_at is not None
        assert task.started_at >= start_time
    
    def test_mark_completed(self):
        """Test marking task as completed."""
        task = SEOTask(
            name="Test Task",
            description="Test description",
            task_type="test"
        )
        
        result = ExecutionResult.success_result("Task completed")
        completion_time = datetime.utcnow()
        
        task.mark_completed(result)
        
        assert task.status == TaskStatus.COMPLETED
        assert task.completed_at is not None
        assert task.completed_at >= completion_time
        assert task.result == result
    
    def test_mark_failed(self):
        """Test marking task as failed."""
        task = SEOTask(
            name="Test Task",
            description="Test description",
            task_type="test"
        )
        
        result = ExecutionResult.failure_result("Task failed", errors=["Error"])
        failure_time = datetime.utcnow()
        
        task.mark_failed(result)
        
        assert task.status == TaskStatus.FAILED
        assert task.completed_at is not None
        assert task.completed_at >= failure_time
        assert task.result == result
    
    def test_duration_property(self):
        """Test duration property calculation."""
        task = SEOTask(
            name="Test Task",
            description="Test description",
            task_type="test"
        )
        
        # No duration when not started
        assert task.duration is None
        
        # Set started and completed times
        start_time = datetime.utcnow()
        task.started_at = start_time
        task.completed_at = start_time + timedelta(seconds=5)
        
        assert task.duration == 5.0
    
    def test_duration_without_completion(self):
        """Test duration when task is not completed."""
        task = SEOTask(
            name="Test Task",
            description="Test description",
            task_type="test"
        )
        
        task.started_at = datetime.utcnow()
        # No completed_at set
        
        assert task.duration is None


class TestSEOMetrics:
    """Test SEOMetrics model."""
    
    def test_seo_metrics_creation(self):
        """Test SEOMetrics creation."""
        metrics = SEOMetrics(
            organic_traffic=1000,
            keyword_rankings=50,
            backlinks=150,
            domain_authority=75.5,
            page_speed_score=85.0,
            core_web_vitals_score=90.0,
            mobile_usability_score=95.0,
            content_quality_score=80.0,
            keyword_density=2.5,
            url="https://example.com"
        )
        
        assert metrics.organic_traffic == 1000
        assert metrics.keyword_rankings == 50
        assert metrics.backlinks == 150
        assert metrics.domain_authority == 75.5
        assert metrics.page_speed_score == 85.0
        assert metrics.core_web_vitals_score == 90.0
        assert metrics.mobile_usability_score == 95.0
        assert metrics.content_quality_score == 80.0
        assert metrics.keyword_density == 2.5
        assert metrics.url == "https://example.com"
        assert isinstance(metrics.measured_at, datetime)
    
    def test_seo_metrics_defaults(self):
        """Test SEOMetrics with default values."""
        metrics = SEOMetrics()
        
        assert metrics.organic_traffic is None
        assert metrics.keyword_rankings is None
        assert metrics.backlinks is None
        assert metrics.domain_authority is None
        assert metrics.page_speed_score is None
        assert metrics.core_web_vitals_score is None
        assert metrics.mobile_usability_score is None
        assert metrics.content_quality_score is None
        assert metrics.keyword_density is None
        assert metrics.url is None
        assert isinstance(metrics.measured_at, datetime)
    
    def test_to_dict_method(self):
        """Test to_dict method."""
        metrics = SEOMetrics(
            organic_traffic=1000,
            keyword_rankings=50,
            url="https://example.com"
        )
        
        result_dict = metrics.to_dict()
        
        assert isinstance(result_dict, dict)
        assert result_dict["organic_traffic"] == 1000
        assert result_dict["keyword_rankings"] == 50
        assert result_dict["url"] == "https://example.com"
        assert "measured_at" in result_dict
        # None values should be excluded
        assert "backlinks" not in result_dict


class TestBaseAgent:
    """Test BaseAgent model."""
    
    def test_base_agent_creation(self):
        """Test BaseAgent creation."""
        agent = BaseAgent(
            name="Test Agent",
            description="Test agent description",
            agent_type="test_agent",
            config={"test": "config"}
        )
        
        assert agent.name == "Test Agent"
        assert agent.description == "Test agent description"
        assert agent.agent_type == "test_agent"
        assert agent.config == {"test": "config"}
        assert agent.is_active is True
        assert isinstance(agent.id, UUID)
        assert isinstance(agent.created_at, datetime)
    
    def test_base_agent_defaults(self):
        """Test BaseAgent with default values."""
        agent = BaseAgent(
            name="Minimal Agent",
            description="Minimal description",
            agent_type="minimal"
        )
        
        assert agent.config == {}
        assert agent.is_active is True
    
    @pytest.mark.asyncio
    async def test_execute_task_not_implemented(self):
        """Test that execute_task raises NotImplementedError."""
        agent = BaseAgent(
            name="Test Agent",
            description="Test description",
            agent_type="test"
        )
        
        task = SEOTask(
            name="Test Task",
            description="Test description",
            task_type="test"
        )
        
        with pytest.raises(NotImplementedError):
            await agent.execute_task(task)
    
    @pytest.mark.asyncio
    async def test_validate_task_default(self):
        """Test default validate_task implementation."""
        agent = BaseAgent(
            name="Test Agent",
            description="Test description",
            agent_type="test"
        )
        
        task = SEOTask(
            name="Test Task",
            description="Test description",
            task_type="any_type"
        )
        
        # Default implementation should return True
        result = await agent.validate_task(task)
        assert result is True
    
    def test_get_supported_task_types_default(self):
        """Test default get_supported_task_types implementation."""
        agent = BaseAgent(
            name="Test Agent",
            description="Test description",
            agent_type="test"
        )
        
        # Default implementation should return empty list
        result = agent.get_supported_task_types()
        assert result == []


class TestKnowledgeEntry:
    """Test KnowledgeEntry model."""
    
    def test_knowledge_entry_creation(self):
        """Test KnowledgeEntry creation."""
        entry = KnowledgeEntry(
            content="Test knowledge content",
            source_type="manual",
            metadata={"author": "test", "version": "1.0"},
            tags=["seo", "best-practice"],
            embedding=[0.1, 0.2, 0.3],
            similarity_score=0.95
        )
        
        assert entry.content == "Test knowledge content"
        assert entry.source_type == "manual"
        assert entry.metadata == {"author": "test", "version": "1.0"}
        assert entry.tags == ["seo", "best-practice"]
        assert entry.embedding == [0.1, 0.2, 0.3]
        assert entry.similarity_score == 0.95
        assert isinstance(entry.id, UUID)
        assert isinstance(entry.created_at, datetime)
        assert entry.updated_at is None
    
    def test_knowledge_entry_defaults(self):
        """Test KnowledgeEntry with default values."""
        entry = KnowledgeEntry(
            content="Minimal content",
            source_type="api"
        )
        
        assert entry.content == "Minimal content"
        assert entry.source_type == "api"
        assert entry.metadata == {}
        assert entry.tags == []
        assert entry.embedding is None
        assert entry.similarity_score is None
        assert entry.updated_at is None


class TestModelValidation:
    """Test model validation and edge cases."""
    
    def test_execution_result_extra_fields_forbidden(self):
        """Test that extra fields are forbidden in ExecutionResult."""
        with pytest.raises(ValueError):
            ExecutionResult(
                success=True,
                message="Test",
                extra_field="not_allowed"
            )
    
    def test_seo_task_extra_fields_forbidden(self):
        """Test that extra fields are forbidden in SEOTask."""
        with pytest.raises(ValueError):
            SEOTask(
                name="Test",
                description="Test",
                task_type="test",
                extra_field="not_allowed"
            )
    
    def test_seo_task_string_stripping(self):
        """Test that string fields are stripped of whitespace."""
        task = SEOTask(
            name="  Test Task  ",
            description="  Test description  ",
            task_type="  seo_analysis  "
        )
        
        assert task.name == "Test Task"
        assert task.description == "Test description"
        assert task.task_type == "seo_analysis"
    
    def test_execution_result_empty_message_validation(self):
        """Test validation with empty message."""
        result = ExecutionResult(
            success=True,
            message=""
        )
        
        assert result.message == ""
        assert result.success is True