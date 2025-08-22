"""Base models for the Data for SEO framework."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, ConfigDict


class TaskStatus(str, Enum):
    """Task execution status."""
    
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    """Task priority levels."""
    
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ExecutionResult(BaseModel):
    """Result of task execution."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid",
    )
    
    success: bool = Field(description="Whether the execution was successful")
    message: str = Field(description="Human-readable result message")
    data: Optional[Dict[str, Any]] = Field(
        default=None, description="Result data payload"
    )
    errors: List[str] = Field(
        default_factory=list, description="List of error messages"
    )
    execution_time: Optional[float] = Field(
        default=None, description="Execution time in seconds"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Result timestamp"
    )
    
    @classmethod
    def success_result(
        cls,
        message: str,
        data: Optional[Dict[str, Any]] = None,
        execution_time: Optional[float] = None,
    ) -> "ExecutionResult":
        """Create a successful execution result."""
        return cls(
            success=True,
            message=message,
            data=data or {},
            execution_time=execution_time,
        )
    
    @classmethod
    def failure_result(
        cls,
        message: str,
        errors: Optional[List[str]] = None,
        execution_time: Optional[float] = None,
    ) -> "ExecutionResult":
        """Create a failed execution result."""
        return cls(
            success=False,
            message=message,
            errors=errors or [],
            execution_time=execution_time,
        )


class SEOTask(BaseModel):
    """Base SEO task model."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid",
    )
    
    id: UUID = Field(default_factory=uuid4, description="Unique task identifier")
    name: str = Field(description="Task name")
    description: str = Field(description="Task description")
    task_type: str = Field(description="Type of SEO task")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Task status")
    priority: TaskPriority = Field(
        default=TaskPriority.MEDIUM, description="Task priority"
    )
    
    # Execution metadata
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Task creation timestamp"
    )
    started_at: Optional[datetime] = Field(
        default=None, description="Task start timestamp"
    )
    completed_at: Optional[datetime] = Field(
        default=None, description="Task completion timestamp"
    )
    
    # Task configuration
    parameters: Dict[str, Any] = Field(
        default_factory=dict, description="Task parameters"
    )
    tags: List[str] = Field(default_factory=list, description="Task tags")
    
    # Results
    result: Optional[ExecutionResult] = Field(
        default=None, description="Task execution result"
    )
    
    def mark_started(self) -> None:
        """Mark task as started."""
        self.status = TaskStatus.RUNNING
        self.started_at = datetime.utcnow()
    
    def mark_completed(self, result: ExecutionResult) -> None:
        """Mark task as completed with result."""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        self.result = result
    
    def mark_failed(self, result: ExecutionResult) -> None:
        """Mark task as failed with result."""
        self.status = TaskStatus.FAILED
        self.completed_at = datetime.utcnow()
        self.result = result
    
    @property
    def duration(self) -> Optional[float]:
        """Get task duration in seconds."""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None


class SEOMetrics(BaseModel):
    """SEO performance metrics."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid",
    )
    
    # Basic metrics
    organic_traffic: Optional[int] = Field(
        default=None, description="Organic traffic count"
    )
    keyword_rankings: Optional[int] = Field(
        default=None, description="Number of ranking keywords"
    )
    backlinks: Optional[int] = Field(
        default=None, description="Number of backlinks"
    )
    domain_authority: Optional[float] = Field(
        default=None, description="Domain authority score"
    )
    
    # Technical metrics
    page_speed_score: Optional[float] = Field(
        default=None, description="Page speed score (0-100)"
    )
    core_web_vitals_score: Optional[float] = Field(
        default=None, description="Core Web Vitals score"
    )
    mobile_usability_score: Optional[float] = Field(
        default=None, description="Mobile usability score"
    )
    
    # Content metrics
    content_quality_score: Optional[float] = Field(
        default=None, description="Content quality score"
    )
    keyword_density: Optional[float] = Field(
        default=None, description="Keyword density percentage"
    )
    
    # Metadata
    measured_at: datetime = Field(
        default_factory=datetime.utcnow, description="Measurement timestamp"
    )
    url: Optional[str] = Field(default=None, description="URL being measured")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary."""
        return self.model_dump(exclude_none=True)


class BaseAgent(BaseModel):
    """Base agent model."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid",
    )
    
    id: UUID = Field(default_factory=uuid4, description="Agent identifier")
    name: str = Field(description="Agent name")
    description: str = Field(description="Agent description")
    agent_type: str = Field(description="Type of agent")
    
    # Status
    is_active: bool = Field(default=True, description="Whether agent is active")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Agent creation timestamp"
    )
    
    # Configuration
    config: Dict[str, Any] = Field(
        default_factory=dict, description="Agent configuration"
    )
    
    async def execute_task(self, task: SEOTask) -> ExecutionResult:
        """Execute a task. Override in subclasses."""
        raise NotImplementedError("Subclasses must implement execute_task")
    
    async def validate_task(self, task: SEOTask) -> bool:
        """Validate if agent can execute the task."""
        return True
    
    def get_supported_task_types(self) -> List[str]:
        """Get list of supported task types."""
        return []


class KnowledgeEntry(BaseModel):
    """Knowledge base entry."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid",
    )
    
    id: UUID = Field(default_factory=uuid4, description="Entry identifier")
    content: str = Field(description="Knowledge content")
    source_type: str = Field(description="Type of knowledge source")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Entry metadata"
    )
    tags: List[str] = Field(default_factory=list, description="Knowledge tags")
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Entry creation timestamp"
    )
    updated_at: Optional[datetime] = Field(
        default=None, description="Entry update timestamp"
    )
    
    # Embedding and search
    embedding: Optional[List[float]] = Field(
        default=None, description="Vector embedding"
    )
    similarity_score: Optional[float] = Field(
        default=None, description="Similarity score for search results"
    )
