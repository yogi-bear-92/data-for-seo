"""Base workflow orchestration engine."""

import asyncio
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, ConfigDict

from ..models.base import ExecutionResult, SEOTask, TaskStatus


class WorkflowStatus(str, Enum):
    """Workflow execution status."""
    
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"


class WorkflowStepResult(BaseModel):
    """Result of a workflow step execution."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid",
    )
    
    step_name: str = Field(description="Name of the workflow step")
    success: bool = Field(description="Whether the step was successful")
    result: Optional[ExecutionResult] = Field(default=None, description="Step execution result")
    duration: Optional[float] = Field(default=None, description="Step duration in seconds")
    error_message: Optional[str] = Field(default=None, description="Error message if failed")


class WorkflowProgress(BaseModel):
    """Workflow execution progress tracking."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid",
    )
    
    workflow_id: UUID = Field(description="Workflow identifier")
    total_steps: int = Field(description="Total number of steps")
    completed_steps: int = Field(default=0, description="Number of completed steps")
    current_step: Optional[str] = Field(default=None, description="Current step name")
    progress_percentage: float = Field(default=0.0, description="Progress percentage (0-100)")
    step_results: List[WorkflowStepResult] = Field(
        default_factory=list, description="Results from completed steps"
    )
    
    def update_progress(self, step_result: WorkflowStepResult) -> None:
        """Update workflow progress with a completed step."""
        self.step_results.append(step_result)
        if step_result.success:
            self.completed_steps += 1
        self.progress_percentage = (self.completed_steps / self.total_steps) * 100


class WorkflowEngine(ABC):
    """Base class for all SEO workflow engines."""
    
    def __init__(
        self,
        name: str,
        description: str,
        config: Optional[Dict[str, Any]] = None,
    ):
        """Initialize the workflow engine."""
        self.id = uuid4()
        self.name = name
        self.description = description
        self.config = config or {}
        self.status = WorkflowStatus.PENDING
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        # Execution tracking
        self.created_at = datetime.utcnow()
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.progress: Optional[WorkflowProgress] = None
        self.final_result: Optional[ExecutionResult] = None
        
        # Error handling
        self.max_retries = self.config.get("max_retries", 3)
        self.retry_delay = self.config.get("retry_delay", 5.0)
        self.timeout = self.config.get("timeout", 300.0)  # 5 minutes default
    
    async def execute(self, parameters: Dict[str, Any]) -> ExecutionResult:
        """Execute the workflow with given parameters."""
        self.started_at = datetime.utcnow()
        self.status = WorkflowStatus.RUNNING
        
        try:
            # Validate parameters
            validation_result = await self.validate_parameters(parameters)
            if not validation_result.success:
                return self._mark_failed(validation_result.message, validation_result.errors)
            
            # Initialize progress tracking
            steps = await self.get_workflow_steps(parameters)
            self.progress = WorkflowProgress(
                workflow_id=self.id,
                total_steps=len(steps),
            )
            
            self.logger.info(f"Starting workflow: {self.name} with {len(steps)} steps")
            
            # Execute workflow with timeout
            try:
                result = await asyncio.wait_for(
                    self._execute_workflow_impl(parameters, steps),
                    timeout=self.timeout
                )
                
                return self._mark_completed(result)
                
            except asyncio.TimeoutError:
                error_msg = f"Workflow timed out after {self.timeout} seconds"
                self.logger.error(error_msg)
                return self._mark_failed(error_msg, ["Workflow execution timeout"])
            
        except Exception as e:
            error_msg = f"Workflow execution failed: {str(e)}"
            self.logger.exception(error_msg)
            return self._mark_failed(error_msg, [str(e)])
    
    async def _execute_workflow_impl(
        self, 
        parameters: Dict[str, Any], 
        steps: List[str]
    ) -> ExecutionResult:
        """Execute the workflow implementation with retry logic."""
        retry_count = 0
        last_error = None
        
        while retry_count <= self.max_retries:
            try:
                return await self.execute_workflow(parameters, steps)
            
            except Exception as e:
                last_error = e
                retry_count += 1
                
                if retry_count <= self.max_retries:
                    self.logger.warning(
                        f"Workflow step failed, retrying {retry_count}/{self.max_retries}: {str(e)}"
                    )
                    await asyncio.sleep(self.retry_delay)
                else:
                    raise e
        
        # This should never be reached, but just in case
        raise last_error or Exception("Unknown workflow execution error")
    
    @abstractmethod
    async def execute_workflow(
        self, 
        parameters: Dict[str, Any], 
        steps: List[str]
    ) -> ExecutionResult:
        """Execute the specific workflow implementation."""
        pass
    
    @abstractmethod
    async def get_workflow_steps(self, parameters: Dict[str, Any]) -> List[str]:
        """Get the list of workflow steps for the given parameters."""
        pass
    
    async def validate_parameters(self, parameters: Dict[str, Any]) -> ExecutionResult:
        """Validate workflow parameters. Override in subclasses for specific validation."""
        if not isinstance(parameters, dict):
            return ExecutionResult.failure_result(
                message="Invalid parameters format",
                errors=["Parameters must be a dictionary"]
            )
        
        return ExecutionResult.success_result("Parameters validated successfully")
    
    async def pause(self) -> bool:
        """Pause the workflow execution."""
        if self.status == WorkflowStatus.RUNNING:
            self.status = WorkflowStatus.PAUSED
            self.logger.info(f"Workflow paused: {self.name}")
            return True
        return False
    
    async def resume(self) -> bool:
        """Resume paused workflow execution."""
        if self.status == WorkflowStatus.PAUSED:
            self.status = WorkflowStatus.RUNNING
            self.logger.info(f"Workflow resumed: {self.name}")
            return True
        return False
    
    async def cancel(self) -> bool:
        """Cancel the workflow execution."""
        if self.status in [WorkflowStatus.RUNNING, WorkflowStatus.PAUSED]:
            self.status = WorkflowStatus.CANCELLED
            self.completed_at = datetime.utcnow()
            self.logger.info(f"Workflow cancelled: {self.name}")
            return True
        return False
    
    def get_progress(self) -> Optional[WorkflowProgress]:
        """Get current workflow progress."""
        return self.progress
    
    def get_status(self) -> WorkflowStatus:
        """Get current workflow status."""
        return self.status
    
    def get_duration(self) -> Optional[float]:
        """Get workflow duration in seconds."""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        elif self.started_at:
            return (datetime.utcnow() - self.started_at).total_seconds()
        return None
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get workflow execution metrics."""
        return {
            "workflow_id": str(self.id),
            "name": self.name,
            "status": self.status.value,
            "duration": self.get_duration(),
            "progress": self.progress.model_dump() if self.progress else None,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
    
    def _mark_completed(self, result: ExecutionResult) -> ExecutionResult:
        """Mark workflow as completed."""
        self.status = WorkflowStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        self.final_result = result
        
        duration = self.get_duration()
        self.logger.info(f"Workflow completed: {self.name} (Duration: {duration:.2f}s)")
        
        return result
    
    def _mark_failed(self, message: str, errors: List[str]) -> ExecutionResult:
        """Mark workflow as failed."""
        self.status = WorkflowStatus.FAILED
        self.completed_at = datetime.utcnow()
        
        result = ExecutionResult.failure_result(
            message=message,
            errors=errors,
            execution_time=self.get_duration()
        )
        self.final_result = result
        
        self.logger.error(f"Workflow failed: {self.name} - {message}")
        
        return result
    
    async def execute_step(
        self, 
        step_name: str, 
        step_function: Any, 
        *args, 
        **kwargs
    ) -> WorkflowStepResult:
        """Execute a single workflow step with progress tracking."""
        start_time = datetime.utcnow()
        
        if self.progress:
            self.progress.current_step = step_name
        
        self.logger.info(f"Executing step: {step_name}")
        
        try:
            # Execute the step function
            if asyncio.iscoroutinefunction(step_function):
                result = await step_function(*args, **kwargs)
            else:
                result = step_function(*args, **kwargs)
            
            duration = (datetime.utcnow() - start_time).total_seconds()
            
            step_result = WorkflowStepResult(
                step_name=step_name,
                success=True,
                result=result if isinstance(result, ExecutionResult) else None,
                duration=duration,
            )
            
            self.logger.info(f"Step completed: {step_name} (Duration: {duration:.2f}s)")
            
        except Exception as e:
            duration = (datetime.utcnow() - start_time).total_seconds()
            error_message = f"Step failed: {step_name} - {str(e)}"
            
            step_result = WorkflowStepResult(
                step_name=step_name,
                success=False,
                duration=duration,
                error_message=error_message,
            )
            
            self.logger.error(error_message)
        
        # Update progress
        if self.progress:
            self.progress.update_progress(step_result)
        
        return step_result