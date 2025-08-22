"""Agent coordination utilities for SEO automation framework."""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Callable
from uuid import UUID, uuid4

import redis.asyncio as redis

from ..config import get_settings
from ..models.base import SEOTask, ExecutionResult, TaskStatus
from .seo_collector import SEOCollectorAgent
from .seo_processor import SEOProcessorAgent

logger = logging.getLogger(__name__)


class AgentMessage:
    """Message for agent communication."""
    
    def __init__(
        self,
        message_id: str,
        sender_id: str,
        recipient_id: Optional[str],
        message_type: str,
        content: Dict[str, Any],
        timestamp: Optional[datetime] = None,
    ):
        self.message_id = message_id
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.message_type = message_type
        self.content = content
        self.timestamp = timestamp or datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            "message_id": self.message_id,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "message_type": self.message_type,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentMessage":
        """Create message from dictionary."""
        return cls(
            message_id=data["message_id"],
            sender_id=data["sender_id"],
            recipient_id=data.get("recipient_id"),
            message_type=data["message_type"],
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )


class MessageBus:
    """Redis-based message bus for agent communication."""
    
    def __init__(self, redis_url: Optional[str] = None):
        """Initialize message bus.
        
        Args:
            redis_url: Redis connection URL (defaults to settings)
        """
        self.settings = get_settings()
        self.redis_url = redis_url or self.settings.redis_url
        self.redis_client: Optional[redis.Redis] = None
        self.subscribers: Dict[str, List[Callable]] = {}
        self.running = False
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    async def connect(self) -> None:
        """Connect to Redis."""
        try:
            self.redis_client = redis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True
            )
            # Test connection
            await self.redis_client.ping()
            self.logger.info("Connected to Redis message bus")
        except Exception as e:
            self.logger.error(f"Failed to connect to Redis: {e}")
            raise
    
    async def disconnect(self) -> None:
        """Disconnect from Redis."""
        if self.redis_client:
            await self.redis_client.close()
            self.redis_client = None
            self.logger.info("Disconnected from Redis message bus")
    
    async def publish(self, channel: str, message: AgentMessage) -> None:
        """Publish message to channel.
        
        Args:
            channel: Channel name
            message: Message to publish
        """
        if not self.redis_client:
            await self.connect()
        
        try:
            message_data = json.dumps(message.to_dict())
            await self.redis_client.publish(channel, message_data)
            self.logger.debug(f"Published message to {channel}: {message.message_type}")
        except Exception as e:
            self.logger.error(f"Failed to publish message: {e}")
            raise
    
    async def subscribe(self, channel: str, callback: Callable[[AgentMessage], None]) -> None:
        """Subscribe to channel.
        
        Args:
            channel: Channel name
            callback: Message handler function
        """
        if channel not in self.subscribers:
            self.subscribers[channel] = []
        
        self.subscribers[channel].append(callback)
        self.logger.debug(f"Subscribed to channel: {channel}")
    
    async def start_listening(self) -> None:
        """Start listening for messages."""
        if not self.redis_client:
            await self.connect()
        
        if not self.subscribers:
            self.logger.warning("No subscribers registered")
            return
        
        self.running = True
        pubsub = self.redis_client.pubsub()
        
        try:
            # Subscribe to all channels
            for channel in self.subscribers.keys():
                await pubsub.subscribe(channel)
                self.logger.info(f"Listening on channel: {channel}")
            
            while self.running:
                try:
                    message = await pubsub.get_message(timeout=1.0)
                    if message and message["type"] == "message":
                        await self._handle_message(message)
                except asyncio.TimeoutError:
                    continue
                except Exception as e:
                    self.logger.error(f"Error handling message: {e}")
                    
        except Exception as e:
            self.logger.error(f"Error in message listener: {e}")
        finally:
            await pubsub.close()
    
    async def _handle_message(self, redis_message: Dict[str, Any]) -> None:
        """Handle incoming message."""
        try:
            channel = redis_message["channel"]
            data = json.loads(redis_message["data"])
            message = AgentMessage.from_dict(data)
            
            # Call all subscribers for this channel
            for callback in self.subscribers.get(channel, []):
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(message)
                    else:
                        callback(message)
                except Exception as e:
                    self.logger.error(f"Error in message callback: {e}")
                    
        except Exception as e:
            self.logger.error(f"Error parsing message: {e}")
    
    async def stop_listening(self) -> None:
        """Stop listening for messages."""
        self.running = False
        self.logger.info("Stopped message bus listener")


class TaskQueue:
    """Redis-based task queue for distributed processing."""
    
    def __init__(self, redis_url: Optional[str] = None, queue_name: str = "seo_tasks"):
        """Initialize task queue.
        
        Args:
            redis_url: Redis connection URL
            queue_name: Name of the task queue
        """
        self.settings = get_settings()
        self.redis_url = redis_url or self.settings.redis_url
        self.queue_name = queue_name
        self.redis_client: Optional[redis.Redis] = None
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    async def connect(self) -> None:
        """Connect to Redis."""
        try:
            self.redis_client = redis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True
            )
            await self.redis_client.ping()
            self.logger.info("Connected to Redis task queue")
        except Exception as e:
            self.logger.error(f"Failed to connect to Redis: {e}")
            raise
    
    async def enqueue_task(self, task: SEOTask, priority: int = 1) -> None:
        """Enqueue task for processing.
        
        Args:
            task: Task to enqueue
            priority: Task priority (higher = more important)
        """
        if not self.redis_client:
            await self.connect()
        
        try:
            task_data = {
                "task": task.model_dump(),
                "enqueued_at": datetime.utcnow().isoformat(),
                "priority": priority,
            }
            
            # Use priority queue (higher priority = lower score in Redis)
            score = -priority
            await self.redis_client.zadd(
                self.queue_name,
                {json.dumps(task_data): score}
            )
            
            self.logger.debug(f"Enqueued task: {task.name} (priority: {priority})")
            
        except Exception as e:
            self.logger.error(f"Failed to enqueue task: {e}")
            raise
    
    async def dequeue_task(self, timeout: int = 30) -> Optional[SEOTask]:
        """Dequeue next task for processing.
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            Next task or None if queue is empty
        """
        if not self.redis_client:
            await self.connect()
        
        try:
            # Get highest priority task (lowest score)
            result = await self.redis_client.bzpopmin(self.queue_name, timeout=timeout)
            
            if result:
                _, task_json, _ = result
                task_data = json.loads(task_json)
                task_dict = task_data["task"]
                
                # Reconstruct SEOTask object
                task = SEOTask(**task_dict)
                self.logger.debug(f"Dequeued task: {task.name}")
                return task
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to dequeue task: {e}")
            return None
    
    async def get_queue_size(self) -> int:
        """Get current queue size."""
        if not self.redis_client:
            await self.connect()
        
        try:
            return await self.redis_client.zcard(self.queue_name)
        except Exception as e:
            self.logger.error(f"Failed to get queue size: {e}")
            return 0


class AgentCoordinator:
    """Coordinates SEO agents and manages workflows."""
    
    def __init__(
        self,
        collector_config: Optional[Dict[str, Any]] = None,
        processor_config: Optional[Dict[str, Any]] = None,
        redis_url: Optional[str] = None,
    ):
        """Initialize agent coordinator.
        
        Args:
            collector_config: Configuration for collector agent
            processor_config: Configuration for processor agent
            redis_url: Redis connection URL
        """
        self.settings = get_settings()
        
        # Initialize agents
        self.collector = SEOCollectorAgent(config=collector_config)
        self.processor = SEOProcessorAgent(config=processor_config)
        
        # Initialize communication infrastructure
        self.message_bus = MessageBus(redis_url=redis_url)
        self.task_queue = TaskQueue(redis_url=redis_url)
        
        # Workflow state
        self.running = False
        self.active_workflows: Dict[str, Dict[str, Any]] = {}
        
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    async def initialize(self) -> None:
        """Initialize coordinator and agents."""
        try:
            # Connect to infrastructure
            await self.message_bus.connect()
            await self.task_queue.connect()
            
            # Set up message handlers
            await self._setup_message_handlers()
            
            # Activate agents
            self.collector.activate()
            self.processor.activate()
            
            self.logger.info("Agent coordinator initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize coordinator: {e}")
            raise
    
    async def _setup_message_handlers(self) -> None:
        """Set up message handlers for agent communication."""
        # Handler for task completion messages
        await self.message_bus.subscribe(
            "task_completed",
            self._handle_task_completion
        )
        
        # Handler for agent status messages
        await self.message_bus.subscribe(
            "agent_status",
            self._handle_agent_status
        )
        
        # Handler for workflow coordination
        await self.message_bus.subscribe(
            "workflow_control",
            self._handle_workflow_control
        )
    
    async def _handle_task_completion(self, message: AgentMessage) -> None:
        """Handle task completion messages."""
        try:
            task_id = message.content.get("task_id")
            result = message.content.get("result")
            agent_type = message.content.get("agent_type")
            
            self.logger.info(f"Task {task_id} completed by {agent_type}")
            
            # Check if this is part of a workflow
            workflow_id = message.content.get("workflow_id")
            if workflow_id and workflow_id in self.active_workflows:
                await self._advance_workflow(workflow_id, task_id, result)
                
        except Exception as e:
            self.logger.error(f"Error handling task completion: {e}")
    
    async def _handle_agent_status(self, message: AgentMessage) -> None:
        """Handle agent status messages."""
        try:
            agent_id = message.sender_id
            status = message.content.get("status")
            
            self.logger.debug(f"Agent {agent_id} status: {status}")
            
        except Exception as e:
            self.logger.error(f"Error handling agent status: {e}")
    
    async def _handle_workflow_control(self, message: AgentMessage) -> None:
        """Handle workflow control messages."""
        try:
            action = message.content.get("action")
            workflow_id = message.content.get("workflow_id")
            
            if action == "start":
                await self._start_workflow(workflow_id, message.content)
            elif action == "pause":
                await self._pause_workflow(workflow_id)
            elif action == "cancel":
                await self._cancel_workflow(workflow_id)
                
        except Exception as e:
            self.logger.error(f"Error handling workflow control: {e}")
    
    async def create_seo_audit_workflow(
        self,
        target_url: str,
        keywords: List[str],
        workflow_id: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Create comprehensive SEO audit workflow.
        
        Args:
            target_url: URL to audit
            keywords: Keywords to analyze
            workflow_id: Optional workflow ID
            config: Workflow configuration
            
        Returns:
            Workflow ID
        """
        if not workflow_id:
            workflow_id = str(uuid4())
        
        workflow_config = config or {}
        
        # Create workflow definition
        workflow = {
            "id": workflow_id,
            "type": "seo_audit",
            "target_url": target_url,
            "keywords": keywords,
            "config": workflow_config,
            "created_at": datetime.utcnow().isoformat(),
            "status": "pending",
            "tasks": [],
            "results": {},
        }
        
        # Define workflow steps
        tasks = [
            # Step 1: Keyword research
            SEOTask(
                name=f"Keyword research for {target_url}",
                description="Collect keyword data and metrics",
                task_type="keyword_research",
                parameters={
                    "keywords": keywords,
                    "include_metrics": True,
                    "include_ideas": True,
                    "workflow_id": workflow_id,
                },
                tags=["workflow", "keyword_research"],
            ),
            
            # Step 2: SERP analysis
            SEOTask(
                name=f"SERP analysis for primary keyword",
                description="Analyze search results for target keywords",
                task_type="serp_analysis",
                parameters={
                    "keyword": keywords[0] if keywords else "",
                    "workflow_id": workflow_id,
                },
                tags=["workflow", "serp_analysis"],
            ),
            
            # Step 3: Ranking data collection
            SEOTask(
                name=f"Ranking data for {target_url}",
                description="Collect current ranking positions",
                task_type="ranking_data",
                parameters={
                    "keywords": keywords,
                    "target_url": target_url,
                    "workflow_id": workflow_id,
                },
                tags=["workflow", "ranking_data"],
            ),
            
            # Step 4: Competitor analysis
            SEOTask(
                name=f"Competitor analysis for {target_url}",
                description="Analyze competitor strategies",
                task_type="competitor_analysis",
                parameters={
                    "target_url": target_url,
                    "include_keywords": True,
                    "include_analytics": True,
                    "workflow_id": workflow_id,
                },
                tags=["workflow", "competitor_analysis"],
            ),
        ]
        
        workflow["tasks"] = [task.model_dump() for task in tasks]
        self.active_workflows[workflow_id] = workflow
        
        # Enqueue first task
        await self.task_queue.enqueue_task(tasks[0], priority=5)
        
        self.logger.info(f"Created SEO audit workflow: {workflow_id}")
        return workflow_id
    
    async def _advance_workflow(
        self,
        workflow_id: str,
        completed_task_id: str,
        result: Dict[str, Any]
    ) -> None:
        """Advance workflow to next step."""
        if workflow_id not in self.active_workflows:
            return
        
        workflow = self.active_workflows[workflow_id]
        
        # Store result
        workflow["results"][completed_task_id] = result
        
        # Check if we need to process the collected data
        if len(workflow["results"]) == len(workflow["tasks"]):
            # All collection tasks completed, start processing
            await self._start_processing_phase(workflow_id)
    
    async def _start_processing_phase(self, workflow_id: str) -> None:
        """Start data processing phase of workflow."""
        workflow = self.active_workflows[workflow_id]
        
        # Combine all collected data
        combined_data = {
            "target_url": workflow["target_url"],
            "keywords": workflow["keywords"],
            "collected_data": workflow["results"],
            "workflow_id": workflow_id,
        }
        
        # Create processing tasks
        processing_tasks = [
            # Data analysis
            SEOTask(
                name=f"SEO data analysis - {workflow_id}",
                description="Analyze collected SEO data",
                task_type="data_analysis",
                parameters={
                    "data_source": combined_data,
                    "analysis_type": "comprehensive",
                    "store_results": True,
                    "workflow_id": workflow_id,
                },
                tags=["workflow", "processing", "analysis"],
            ),
            
            # Pattern recognition
            SEOTask(
                name=f"Pattern recognition - {workflow_id}",
                description="Identify SEO patterns and trends",
                task_type="pattern_recognition",
                parameters={
                    "data_source": combined_data,
                    "pattern_types": ["keyword", "ranking", "content"],
                    "workflow_id": workflow_id,
                },
                tags=["workflow", "processing", "patterns"],
            ),
        ]
        
        # Enqueue processing tasks
        for task in processing_tasks:
            await self.task_queue.enqueue_task(task, priority=4)
        
        workflow["processing_tasks"] = [task.model_dump() for task in processing_tasks]
        
        self.logger.info(f"Started processing phase for workflow: {workflow_id}")
    
    async def run_task_processor(self) -> None:
        """Run task processor loop."""
        self.running = True
        
        self.logger.info("Starting task processor")
        
        while self.running:
            try:
                # Get next task from queue
                task = await self.task_queue.dequeue_task(timeout=5)
                
                if task:
                    await self._process_task(task)
                
            except Exception as e:
                self.logger.error(f"Error in task processor: {e}")
                await asyncio.sleep(1)
        
        self.logger.info("Task processor stopped")
    
    async def _process_task(self, task: SEOTask) -> None:
        """Process a single task."""
        try:
            self.logger.info(f"Processing task: {task.name} ({task.task_type})")
            
            # Route task to appropriate agent
            if task.task_type in self.collector.get_supported_task_types():
                result = await self.collector.execute_task(task)
                agent_type = "collector"
            elif task.task_type in self.processor.get_supported_task_types():
                result = await self.processor.execute_task(task)
                agent_type = "processor"
            else:
                result = ExecutionResult.failure_result(
                    message=f"No agent supports task type: {task.task_type}",
                    errors=[f"Unsupported task type: {task.task_type}"],
                )
                agent_type = "unknown"
            
            # Publish task completion message
            completion_message = AgentMessage(
                message_id=str(uuid4()),
                sender_id="coordinator",
                recipient_id=None,
                message_type="task_completed",
                content={
                    "task_id": str(task.id),
                    "task_type": task.task_type,
                    "agent_type": agent_type,
                    "result": result.model_dump(),
                    "workflow_id": task.parameters.get("workflow_id"),
                },
            )
            
            await self.message_bus.publish("task_completed", completion_message)
            
            self.logger.info(f"Completed task: {task.name} (success: {result.success})")
            
        except Exception as e:
            self.logger.error(f"Error processing task {task.name}: {e}")
    
    async def start(self) -> None:
        """Start the coordinator."""
        await self.initialize()
        
        # Start message bus listener
        asyncio.create_task(self.message_bus.start_listening())
        
        # Start task processor
        await self.run_task_processor()
    
    async def stop(self) -> None:
        """Stop the coordinator."""
        self.logger.info("Stopping agent coordinator")
        
        self.running = False
        
        # Stop message bus
        await self.message_bus.stop_listening()
        
        # Shutdown agents
        await self.collector.shutdown()
        await self.processor.shutdown()
        
        # Disconnect from infrastructure
        await self.message_bus.disconnect()
        
        self.logger.info("Agent coordinator stopped")
    
    async def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get workflow status.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            Workflow status or None if not found
        """
        if workflow_id in self.active_workflows:
            workflow = self.active_workflows[workflow_id].copy()
            
            # Add status information
            workflow["active_tasks"] = await self.task_queue.get_queue_size()
            workflow["last_updated"] = datetime.utcnow().isoformat()
            
            return workflow
        
        return None
    
    async def get_agent_metrics(self) -> Dict[str, Any]:
        """Get metrics from all agents.
        
        Returns:
            Combined agent metrics
        """
        return {
            "collector": await self.collector.get_metrics(),
            "processor": await self.processor.get_metrics(),
            "coordinator": {
                "active_workflows": len(self.active_workflows),
                "queue_size": await self.task_queue.get_queue_size(),
                "running": self.running,
            },
        }


# Convenience function for creating coordinator instances
async def create_agent_coordinator(
    collector_config: Optional[Dict[str, Any]] = None,
    processor_config: Optional[Dict[str, Any]] = None,
    redis_url: Optional[str] = None,
) -> AgentCoordinator:
    """Create and initialize agent coordinator.
    
    Args:
        collector_config: Configuration for collector agent
        processor_config: Configuration for processor agent
        redis_url: Redis connection URL
        
    Returns:
        Initialized AgentCoordinator instance
    """
    coordinator = AgentCoordinator(
        collector_config=collector_config,
        processor_config=processor_config,
        redis_url=redis_url,
    )
    await coordinator.initialize()
    return coordinator