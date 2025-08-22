"""Base SEO agent implementation."""

import asyncio
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from ..config import get_settings
from ..models.base import BaseAgent, ExecutionResult, SEOTask, TaskStatus

logger = logging.getLogger(__name__)


class BaseSEOAgent(BaseAgent, ABC):
    """Base class for all SEO agents."""
    
    def __init__(
        self,
        name: str,
        description: str,
        agent_type: str,
        config: Optional[Dict[str, Any]] = None,
    ):
        """Initialize the SEO agent."""
        super().__init__(
            name=name,
            description=description,
            agent_type=agent_type,
            config=config or {},
        )
        self.settings = get_settings()
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
    async def execute_task(self, task: SEOTask) -> ExecutionResult:
        """Execute a task with proper error handling and logging."""
        start_time = datetime.utcnow()
        
        try:
            # Validate task
            if not await self.validate_task(task):
                return ExecutionResult.failure_result(
                    message=f"Task validation failed for {task.name}",
                    errors=[f"Agent {self.name} cannot execute task type {task.task_type}"],
                )
            
            # Mark task as started
            task.mark_started()
            self.logger.info(f"Starting task: {task.name} (ID: {task.id})")
            
            # Execute the actual task
            result = await self._execute_task_impl(task)
            
            # Calculate execution time
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            result.execution_time = execution_time
            
            # Mark task as completed or failed
            if result.success:
                task.mark_completed(result)
                self.logger.info(
                    f"Task completed successfully: {task.name} "
                    f"(Duration: {execution_time:.2f}s)"
                )
            else:
                task.mark_failed(result)
                self.logger.error(
                    f"Task failed: {task.name} - {result.message} "
                    f"(Duration: {execution_time:.2f}s)"
                )
            
            return result
            
        except asyncio.TimeoutError:
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            error_result = ExecutionResult.failure_result(
                message=f"Task timed out after {execution_time:.2f} seconds",
                errors=["Task execution timeout"],
                execution_time=execution_time,
            )
            task.mark_failed(error_result)
            self.logger.error(f"Task timed out: {task.name}")
            return error_result
            
        except Exception as e:
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            error_result = ExecutionResult.failure_result(
                message=f"Task execution failed: {str(e)}",
                errors=[str(e)],
                execution_time=execution_time,
            )
            task.mark_failed(error_result)
            self.logger.exception(f"Task execution error: {task.name}")
            return error_result
    
    @abstractmethod
    async def _execute_task_impl(self, task: SEOTask) -> ExecutionResult:
        """Implement the actual task execution logic."""
        pass
    
    async def validate_task(self, task: SEOTask) -> bool:
        """Validate if the agent can execute the given task."""
        supported_types = self.get_supported_task_types()
        if not supported_types:
            return True  # Agent supports all task types
        
        return task.task_type in supported_types
    
    def get_supported_task_types(self) -> List[str]:
        """Get list of supported task types. Override in subclasses."""
        return []
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform agent health check."""
        return {
            "agent_id": str(self.id),
            "name": self.name,
            "type": self.agent_type,
            "status": "healthy" if self.is_active else "inactive",
            "created_at": self.created_at.isoformat(),
            "config": self.config,
        }
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get agent performance metrics."""
        # This would typically be implemented with actual metrics collection
        return {
            "tasks_executed": 0,
            "success_rate": 0.0,
            "average_execution_time": 0.0,
            "last_activity": None,
        }
    
    def update_config(self, config: Dict[str, Any]) -> None:
        """Update agent configuration."""
        self.config.update(config)
        self.logger.info(f"Agent configuration updated: {self.name}")
    
    def activate(self) -> None:
        """Activate the agent."""
        self.is_active = True
        self.logger.info(f"Agent activated: {self.name}")
    
    def deactivate(self) -> None:
        """Deactivate the agent."""
        self.is_active = False
        self.logger.info(f"Agent deactivated: {self.name}")
    
    async def shutdown(self) -> None:
        """Gracefully shutdown the agent."""
        self.deactivate()
        self.logger.info(f"Agent shutdown: {self.name}")


class SEOTaskMixin:
    """Mixin for common SEO task functionality."""
    
    @staticmethod
    def create_seo_task(
        name: str,
        description: str,
        task_type: str,
        parameters: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
    ) -> SEOTask:
        """Create a new SEO task."""
        return SEOTask(
            name=name,
            description=description,
            task_type=task_type,
            parameters=parameters or {},
            tags=tags or [],
        )
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format."""
        try:
            from urllib.parse import urlparse
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    @staticmethod
    def validate_keyword(keyword: str) -> bool:
        """Validate keyword format."""
        if not keyword or not isinstance(keyword, str):
            return False
        
        # Basic validation - not empty, reasonable length
        return 1 <= len(keyword.strip()) <= 200
    
    @staticmethod
    def extract_domain(url: str) -> Optional[str]:
        """Extract domain from URL."""
        try:
            from urllib.parse import urlparse
            return urlparse(url).netloc.lower()
        except Exception:
            return None
