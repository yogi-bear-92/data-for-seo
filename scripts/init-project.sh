#!/bin/bash

# Data for SEO - Project Initialization Script
# This script sets up the initial project structure and configuration

set -e  # Exit on any error

echo "🚀 Initializing Data for SEO project..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "docs" ]; then
    print_error "Please run this script from the data-for-seo project root directory"
    exit 1
fi

print_status "Setting up project structure..."

# Create necessary directories if they don't exist
mkdir -p .claude/commands/{prp-commands,development,code-quality,rapid-development,git-operations,seo-specific}
mkdir -p .cursor/rules
mkdir -p PRPs/{templates,scripts,ai_docs}
mkdir -p src/{agent_factory,agents/{base,seo_analyst,content_optimizer,technical_auditor,performance_monitor,automation_engineer,coordinator},api/{rest,streaming,ui},communication/{message_bus,protocols,coordination},knowledge/{memory,rag,vector_store},workflows/{monitoring,prp_engine,validation},tools/{deployment,git,testing,seo},config}
mkdir -p tests
mkdir -p docker
mkdir -p claude_md_files
mkdir -p archon-projects/seo-automation/{tasks/{seo-analysis,data-integration,automation},knowledge/{agent-factory,seo-patterns,integration},features/{seo-api,data-processing,reporting},workflows}

print_success "Directory structure created"

# Create basic configuration files
print_status "Creating configuration files..."

# Create .env.example
cat > .env.example << 'EOF'
# Data for SEO API Configuration
DATAFORSEO_LOGIN=your-login
DATAFORSEO_PASSWORD=your-password
DATAFORSEO_API_URL=https://api.dataforseo.com

# Agent Factory Integration
AGENT_FACTORY_REDIS_URL=redis://localhost:6379
AGENT_FACTORY_CHROMA_URL=http://localhost:8000
AGENT_FACTORY_KNOWLEDGE_INTEGRATION=true

# Archon MCP Configuration
ARCHON_SERVER_URL=http://localhost:8051
ARCHON_API_KEY=your-api-key
ARCHON_PROJECT_DIR=./archon-projects

# Development Settings
DEBUG=true
LOG_LEVEL=INFO
ENVIRONMENT=development

# API Rate Limiting
API_RATE_LIMIT=100
API_RATE_LIMIT_WINDOW=3600

# SEO Analysis Settings
SEO_ANALYSIS_DEPTH=comprehensive
KEYWORD_RESEARCH_LIMIT=1000
COMPETITOR_ANALYSIS_LIMIT=10
EOF

print_success "Environment configuration created"

# Create pyproject.toml
cat > pyproject.toml << 'EOF'
[project]
name = "data-for-seo"
version = "0.1.0"
description = "SEO automation framework built on Agent Factory with Data for SEO API integration"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    # Core agent framework
    "langchain>=0.1.0",
    "langchain-community>=0.0.20",
    "langchain-core>=0.1.0",
    # Vector database and embeddings
    "chromadb>=0.4.22",
    "sentence-transformers>=2.2.2",
    # Message bus and communication
    "redis>=5.0.1",
    "redis[hiredis]>=5.0.1",
    # Web framework and API
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "websockets>=12.0",
    "streamlit>=1.28.0",
    # Data processing and serialization
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",
    # Async and concurrency
    "asyncio-mqtt>=0.16.1",
    "aiofiles>=23.2.1",
    "aioredis>=2.0.1",
    # External tool integrations
    "GitPython>=3.1.40",
    "docker>=6.1.3",
    # Testing and quality
    "pytest>=7.4.3",
    "pytest-asyncio>=0.21.1",
    "pytest-mock>=3.12.0",
    "ruff>=0.1.6",
    "mypy>=1.7.0",
    # Logging and monitoring
    "structlog>=23.2.0",
    "prometheus-client>=0.19.0",
    "opentelemetry-api>=1.21.0",
    "opentelemetry-sdk>=1.21.0",
    # Utilities
    "python-dotenv>=1.0.0",
    "click>=8.1.7",
    "rich>=13.7.0",
    "tenacity>=8.2.3",
    "boto3>=1.40.14",
    "openai>=1.30.0",
    # SEO-specific dependencies
    "requests>=2.31.0",
    "beautifulsoup4>=4.12.0",
    "lxml>=4.9.0",
    "pandas>=2.0.0",
    "numpy>=1.24.0",
    "matplotlib>=3.7.0",
    "seaborn>=0.12.0",
]

[project.scripts]
seo-automation = "src.agent_factory.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/agent_factory"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
asyncio_mode = "auto"
addopts = [
    "--strict-markers",
    "--strict-config",
    "--verbose",
]

[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true

[tool.ruff]
target-version = "py312"
line-length = 88

[tool.ruff.lint]
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4", # flake8-comprehensions
    "UP", # pyupgrade
]
ignore = [
    "E501",  # line too long, handled by black
    "B008",  # do not perform function calls in argument defaults
    "C901",  # too complex
]

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]
EOF

print_success "Python project configuration created"

# Create docker-compose.dev.yml
cat > docker-compose.dev.yml << 'EOF'
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

  chroma:
    image: chromadb/chroma:latest
    ports:
      - "8000:8000"
    volumes:
      - chroma_data:/chroma/chroma
    environment:
      - CHROMA_SERVER_HOST=0.0.0.0
      - CHROMA_SERVER_HTTP_PORT=8000
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/heartbeat"]
      interval: 10s
      timeout: 5s
      retries: 5

  seo-api:
    build: .
    ports:
      - "8001:8000"
    environment:
      - ENVIRONMENT=development
      - REDIS_URL=redis://redis:6379
      - CHROMA_URL=http://chroma:8000
    depends_on:
      redis:
        condition: service_healthy
      chroma:
        condition: service_healthy
    volumes:
      - .:/app
      - /app/__pycache__
    command: uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

  archon-server:
    image: archon/server:latest
    ports:
      - "8051:8051"
    environment:
      - ARCHON_ENVIRONMENT=development
      - ARCHON_LOG_LEVEL=debug
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8051/health"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  redis_data:
  chroma_data:
EOF

print_success "Docker development configuration created"

# Create basic source files
print_status "Creating basic source files..."

# Create __init__.py files
find src -type d -exec touch {}/__init__.py \;
touch tests/__init__.py

# Create basic models.py
cat > src/models.py << 'EOF'
"""Core type definitions for the SEO automation framework."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class MessageType(str, Enum):
    """Types of messages between agents."""

    TASK_ASSIGNMENT = "task_assignment"
    TASK_RESULT = "task_result"
    TASK_UPDATE = "task_update"
    COORDINATION = "coordination"
    HEARTBEAT = "heartbeat"
    ERROR = "error"


class TaskPriority(str, Enum):
    """Task priority levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskStatus(str, Enum):
    """Task execution status."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class SourceType(str, Enum):
    """Types of knowledge sources."""

    DOCUMENTATION = "documentation"
    CODE = "code"
    PATTERN = "pattern"
    FAILURE = "failure"
    SUCCESS = "success"
    CONTEXT = "context"
    SEO_DATA = "seo_data"


class AgentType(str, Enum):
    """Types of agents in the system."""

    COORDINATOR = "coordinator"
    SEO_ANALYST = "seo_analyst"
    CONTENT_OPTIMIZER = "content_optimizer"
    TECHNICAL_AUDITOR = "technical_auditor"
    PERFORMANCE_MONITOR = "performance_monitor"
    AUTOMATION_ENGINEER = "automation_engineer"


@dataclass
class AgentMessage:
    """Message structure for agent communication."""

    id: str = field(default_factory=lambda: str(uuid4()))
    sender_id: str = ""
    recipient_id: str = ""
    message_type: MessageType = MessageType.COORDINATION
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    correlation_id: str | None = None


@dataclass
class TaskSpecification:
    """Specification for a task to be executed by an agent."""

    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    description: str = ""
    requirements: list[str] = field(default_factory=list)
    acceptance_criteria: list[str] = field(default_factory=list)
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.PENDING
    assigned_agent: str | None = None
    dependencies: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class KnowledgeEntry:
    """Entry in the knowledge base."""

    id: str = field(default_factory=lambda: str(uuid4()))
    content: str = ""
    embedding: list[float] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    source_type: SourceType = SourceType.CONTEXT
    created_at: datetime = field(default_factory=datetime.utcnow)
    tags: list[str] = field(default_factory=list)


@dataclass
class AgentPRP:
    """Product Requirement Prompt optimized for agent consumption."""

    goal: str = ""
    justification: str = ""
    context: dict[str, Any] = field(default_factory=dict)
    implementation_steps: list[str] = field(default_factory=list)
    validation_criteria: list[str] = field(default_factory=list)
    success_metrics: list[str] = field(default_factory=list)
    failure_recovery: list[str] = field(default_factory=list)


class AgentResponse(BaseModel):
    """Response from an agent after processing a task."""

    agent_id: str
    task_id: str
    success: bool
    result: dict[str, Any] = Field(default_factory=dict)
    error_message: str | None = None
    execution_time: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ExecutionResult(BaseModel):
    """Result of PRP execution."""

    success: bool
    output: dict[str, Any] = Field(default_factory=dict)
    errors: list[str] = Field(default_factory=list)
    performance_metrics: dict[str, Any] = Field(default_factory=dict)
    execution_time: float = 0.0

    @classmethod
    def failure(cls, errors: list[str]) -> ExecutionResult:
        """Create a failure result."""
        return cls(success=False, errors=errors)

    @classmethod
    def success(cls, output: dict[str, Any]) -> ExecutionResult:
        """Create a success result."""
        return cls(success=True, output=output)


class FeatureRequest(BaseModel):
    """External feature request structure."""

    title: str
    description: str
    requirements: list[str]
    priority: TaskPriority = TaskPriority.MEDIUM
    metadata: dict[str, Any] = Field(default_factory=dict)


class SEOData(BaseModel):
    """SEO data structure for analysis and processing."""

    keyword: str
    search_volume: int | None = None
    difficulty: float | None = None
    cpc: float | None = None
    competition: float | None = None
    related_keywords: list[str] = Field(default_factory=list)
    search_intent: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
EOF

print_success "Basic source files created"

# Create basic test file
cat > tests/test_models.py << 'EOF'
"""Tests for core models."""

import pytest
from datetime import datetime
from src.models import (
    MessageType,
    TaskPriority,
    TaskStatus,
    AgentType,
    AgentMessage,
    TaskSpecification,
    KnowledgeEntry,
    AgentPRP,
    AgentResponse,
    ExecutionResult,
    FeatureRequest,
    SEOData,
)


class TestEnums:
    """Test enum values and behavior."""

    def test_message_type_values(self):
        """Test MessageType enum values."""
        assert MessageType.TASK_ASSIGNMENT == "task_assignment"
        assert MessageType.TASK_RESULT == "task_result"
        assert MessageType.COORDINATION == "coordination"

    def test_task_priority_values(self):
        """Test TaskPriority enum values."""
        assert TaskPriority.LOW == "low"
        assert TaskPriority.CRITICAL == "critical"

    def test_agent_type_values(self):
        """Test AgentType enum values."""
        assert AgentType.SEO_ANALYST == "seo_analyst"
        assert AgentType.CONTENT_OPTIMIZER == "content_optimizer"


class TestDataClasses:
    """Test dataclass behavior."""

    def test_agent_message_creation(self):
        """Test AgentMessage creation."""
        message = AgentMessage(
            sender_id="agent1",
            recipient_id="agent2",
            message_type=MessageType.TASK_ASSIGNMENT
        )
        assert message.sender_id == "agent1"
        assert message.recipient_id == "agent2"
        assert message.message_type == MessageType.TASK_ASSIGNMENT
        assert message.id is not None

    def test_task_specification_creation(self):
        """Test TaskSpecification creation."""
        task = TaskSpecification(
            title="Test Task",
            description="Test Description",
            priority=TaskPriority.HIGH
        )
        assert task.title == "Test Task"
        assert task.priority == TaskPriority.HIGH
        assert task.status == TaskStatus.PENDING


class TestPydanticModels:
    """Test Pydantic model behavior."""

    def test_agent_response_creation(self):
        """Test AgentResponse creation."""
        response = AgentResponse(
            agent_id="test_agent",
            task_id="test_task",
            success=True
        )
        assert response.agent_id == "test_agent"
        assert response.success is True

    def test_execution_result_factory_methods(self):
        """Test ExecutionResult factory methods."""
        success_result = ExecutionResult.success({"data": "test"})
        assert success_result.success is True
        assert success_result.output["data"] == "test"

        failure_result = ExecutionResult.failure(["error1", "error2"])
        assert failure_result.success is False
        assert len(failure_result.errors) == 2

    def test_seo_data_creation(self):
        """Test SEOData creation."""
        seo_data = SEOData(
            keyword="test keyword",
            search_volume=1000,
            difficulty=0.5
        )
        assert seo_data.keyword == "test keyword"
        assert seo_data.search_volume == 1000
        assert seo_data.difficulty == 0.5
EOF

print_success "Basic test files created"

# Create development startup script
cat > scripts/dev-start.sh << 'EOF'
#!/bin/bash

# Data for SEO - Development Environment Startup Script

set -e

echo "🚀 Starting Data for SEO development environment..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_warning "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating from .env.example..."
    cp .env.example .env
    print_warning "Please edit .env file with your Data for SEO API credentials"
fi

# Start development services
print_status "Starting development services with Docker Compose..."

docker-compose -f docker-compose.dev.yml up -d

# Wait for services to be healthy
print_status "Waiting for services to be healthy..."

# Wait for Redis
print_status "Waiting for Redis..."
until docker-compose -f docker-compose.dev.yml exec -T redis redis-cli ping > /dev/null 2>&1; do
    sleep 2
done
print_success "Redis is ready"

# Wait for Chroma
print_status "Waiting for Chroma..."
until curl -f http://localhost:8000/api/v1/heartbeat > /dev/null 2>&1; do
    sleep 2
done
print_success "Chroma is ready"

# Wait for Archon server (if configured)
if grep -q "ARCHON_SERVER_URL" .env; then
    print_status "Waiting for Archon server..."
    until curl -f http://localhost:8051/health > /dev/null 2>&1; do
        sleep 2
    done
    print_success "Archon server is ready"
fi

print_success "All development services are running!"

# Display service status
echo ""
print_status "Service Status:"
docker-compose -f docker-compose.dev.yml ps

echo ""
print_status "Service URLs:"
echo "  - Chroma Vector DB: http://localhost:8000"
echo "  - Redis: localhost:6379"
echo "  - Archon Server: http://localhost:8051"
echo "  - SEO API: http://localhost:8001"

echo ""
print_status "Next steps:"
echo "  1. Install dependencies: uv sync"
echo "  2. Initialize project context: claude /prime-core"
echo "  3. Create your first PRP: claude /prp-base-create 'implement SEO feature'"
echo "  4. Execute PRP: uv run PRPs/scripts/prp_runner.py --prp feature-name --interactive"

echo ""
print_success "Development environment is ready! 🎉"
EOF

chmod +x scripts/dev-start.sh

print_success "Development startup script created"

# Create SEO setup script
cat > scripts/seo-setup.sh << 'EOF'
#!/bin/bash

# Data for SEO - SEO-Specific Setup Script

set -e

echo "🔍 Setting up SEO-specific components..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if .env file exists and has Data for SEO credentials
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Please run init-project.sh first."
    exit 1
fi

# Check if Data for SEO credentials are configured
if ! grep -q "DATAFORSEO_LOGIN" .env || ! grep -q "DATAFORSEO_PASSWORD" .env; then
    print_warning "Data for SEO credentials not found in .env file."
    print_warning "Please add your Data for SEO API credentials:"
    echo ""
    echo "DATAFORSEO_LOGIN=your-login"
    echo "DATAFORSEO_PASSWORD=your-password"
    echo ""
    print_warning "You can edit .env file manually or run this script again after adding credentials."
    exit 1
fi

print_status "Data for SEO credentials found in .env file"

# Create SEO-specific directories and files
print_status "Creating SEO-specific project structure..."

# Create SEO automation project in Archon
mkdir -p archon-projects/seo-automation/{tasks,knowledge,features,workflows}

# Create SEO task templates
cat > archon-projects/seo-automation/tasks/seo-analysis/keyword-research.md << 'EOF'
# Keyword Research Task Template

## Overview
Automated keyword research using Data for SEO APIs.

## Input
- Target keywords
- Language/locale
- Search volume requirements
- Competition level preferences

## Process
1. Query Data for SEO keyword research API
2. Analyze search volume and difficulty
3. Identify long-tail opportunities
4. Generate keyword recommendations

## Output
- Keyword analysis report
- Search volume data
- Difficulty scores
- Related keywords
- Content suggestions

## Validation
- API response validation
- Data quality checks
- Performance metrics
EOF

cat > archon-projects/seo-automation/tasks/seo-analysis/rank-tracking.md << 'EOF'
# Rank Tracking Task Template

## Overview
Monitor search engine rankings for target keywords.

## Input
- Target keywords
- Target URLs
- Search engines
- Tracking frequency

## Process
1. Query Data for SEO rank tracking API
2. Store historical ranking data
3. Calculate ranking changes
4. Generate trend analysis

## Output
- Current rankings
- Ranking change history
- Trend analysis
- Performance alerts

## Validation
- Data accuracy verification
- Historical consistency
- Alert threshold validation
EOF

print_success "SEO task templates created"

# Create SEO knowledge base
cat > archon-projects/seo-automation/knowledge/seo-patterns/best-practices.md << 'EOF'
# SEO Best Practices

## Technical SEO
- Page speed optimization
- Mobile-first indexing
- Schema markup implementation
- XML sitemap generation
- Robots.txt configuration

## On-Page SEO
- Title tag optimization
- Meta description writing
- Header tag structure
- Image alt text
- Internal linking

## Content SEO
- Keyword research and targeting
- Content quality and depth
- User intent matching
- Content freshness
- Multimedia optimization

## Off-Page SEO
- Link building strategies
- Social media signals
- Brand mentions
- Local SEO optimization
- E-A-T signals
EOF

cat > archon-projects/seo-automation/knowledge/seo-patterns/automation-patterns.md << 'EOF'
# SEO Automation Patterns

## Data Collection
- API integration patterns
- Rate limiting strategies
- Error handling approaches
- Data validation methods
- Caching strategies

## Analysis Patterns
- Trend analysis algorithms
- Competitive analysis methods
- Performance benchmarking
- Anomaly detection
- Predictive modeling

## Reporting Patterns
- Automated report generation
- Data visualization
- Alert systems
- Performance dashboards
- Custom metrics
EOF

print_success "SEO knowledge base created"

# Create SEO feature specifications
cat > archon-projects/seo-automation/features/seo-api/integration-spec.md << 'EOF'
# Data for SEO API Integration Specification

## Authentication
- Login/password authentication
- API key management
- Rate limiting compliance
- Error handling

## Core APIs
- Keyword research
- Rank tracking
- Site audit
- Competitor analysis
- Local SEO

## Data Processing
- Response parsing
- Data normalization
- Quality validation
- Storage optimization

## Integration Points
- Agent Factory integration
- Knowledge base population
- Workflow automation
- Reporting systems
EOF

print_success "SEO feature specifications created"

# Create SEO workflow definitions
cat > archon-projects/seo-automation/workflows/keyword-research-workflow.md << 'EOF'
# Keyword Research Workflow

## Trigger
- New content creation
- Content optimization
- Competitive analysis
- Seasonal campaigns

## Steps
1. **Input Collection**: Gather target topics and requirements
2. **Keyword Research**: Query Data for SEO APIs
3. **Analysis**: Process and analyze keyword data
4. **Recommendation**: Generate keyword recommendations
5. **Validation**: Verify data quality and relevance
6. **Delivery**: Provide results to content team

## Agents Involved
- SEO Analyst: Primary research and analysis
- Content Optimizer: Content strategy input
- Coordinator: Workflow orchestration

## Success Metrics
- Keyword relevance score
- Search volume accuracy
- Competition level precision
- Recommendation quality
EOF

print_success "SEO workflow definitions created"

# Create basic PRP template for SEO
cat > PRPs/templates/prp_seo.md << 'EOF'
# SEO Implementation PRP Template

## Goal
[Describe the SEO feature or automation goal]

## User Persona
[Define the target user and their needs]

## Why
[Explain the business value and problem being solved]

## What
[Define the specific requirements and success criteria]

## All Needed Context
[Include relevant documentation, patterns, and gotchas]

## Implementation Blueprint
[Define data models, tasks, and patterns]

## Validation Loop
[Define testing and validation steps]

## Anti-Patterns to Avoid
[List common mistakes and anti-patterns]
EOF

print_success "SEO PRP template created"

# Create basic AI documentation
cat > PRPs/ai_docs/seo_patterns.md << 'EOF'
# SEO Patterns and Best Practices

## Keyword Research Patterns
- Volume vs. difficulty analysis
- Long-tail keyword identification
- Search intent classification
- Seasonal trend analysis

## Content Optimization Patterns
- Topic clustering
- Content gap analysis
- Competitive content analysis
- Performance optimization

## Technical SEO Patterns
- Site structure optimization
- Page speed optimization
- Mobile optimization
- Schema markup implementation

## Automation Patterns
- Data collection workflows
- Analysis automation
- Reporting automation
- Alert systems
EOF

print_success "SEO AI documentation created"

print_success "SEO-specific setup completed!"

echo ""
print_status "SEO Components Created:"
echo "  - Task templates for keyword research and rank tracking"
echo "  - Knowledge base with best practices and automation patterns"
echo "  - Feature specifications for API integration"
echo "  - Workflow definitions for common SEO processes"
echo "  - SEO-specific PRP template"
echo "  - AI documentation for SEO patterns"

echo ""
print_status "Next steps:"
echo "  1. Review and customize the created templates"
echo "  2. Test Data for SEO API connectivity"
echo "  3. Create your first SEO automation PRP"
echo "  4. Execute and validate the automation workflow"

echo ""
print_success "SEO setup is complete! 🎯"
EOF

chmod +x scripts/seo-setup.sh

print_success "SEO setup script created"

# Create basic CLAUDE.md
cat > CLAUDE.md << 'EOF'
# Data for SEO - Claude Code Instructions

## Project Overview

This is a **Data for SEO automation project** built on the **Agent Factory framework**. The project enables AI agents to develop and deploy SEO automation features through structured PRP workflows and comprehensive knowledge management.

## Key Commands

### Core Workflow
- `/prime-core` - Initialize project context
- `/prp-base-create` - Create comprehensive PRPs for SEO features
- `/prp-base-execute` - Execute existing PRPs
- `/review-staged-unstaged` - Review changes using PRP methodology

### SEO-Specific Commands
- `/seo-analyze` - SEO analysis and insights
- `/seo-keyword-research` - Keyword research automation
- `/seo-rank-tracking` - Rank tracking setup and monitoring
- `/seo-content-optimize` - Content optimization suggestions
- `/seo-technical-audit` - Technical SEO analysis

## Project Structure

- **`docs/`**: Comprehensive documentation (ONBOARDING.md, QUICKSTART.md, ARCHITECTURE.md)
- **`PRPs/`**: Product Requirement Prompts and templates
- **`src/`**: Source code with multi-agent system
- **`archon-projects/`**: Archon project containers for SEO automation
- **`scripts/`**: Automation and setup scripts

## Development Patterns

- **Multi-Agent System**: Specialized agents for different SEO functions
- **PRP Methodology**: Structured approach to feature development
- **Knowledge Management**: Vector database and RAG for context-aware decisions
- **Event-Driven Communication**: Redis pub/sub for agent coordination

## SEO Integration

- **Data for SEO APIs**: Comprehensive SEO data and analysis
- **Automation Workflows**: Automated keyword research, rank tracking, and analysis
- **Pattern Recognition**: SEO best practices and automation patterns
- **Performance Monitoring**: SEO performance tracking and reporting

## Getting Started

1. Read `docs/ONBOARDING.md` for comprehensive setup
2. Use `docs/QUICKSTART.md` for fast setup
3. Study `docs/ARCHITECTURE.md` for system understanding
4. Create your first SEO PRP with `/prp-base-create`
5. Execute PRPs with the multi-agent system

## Quality Standards

- Follow existing code patterns and architecture
- Maintain comprehensive test coverage
- Use structured error handling and validation
- Document all changes and patterns
- Integrate with existing knowledge management systems

Welcome to Data for SEO automation! Let's build intelligent SEO systems together.
EOF

print_success "CLAUDE.md created"

# Create basic .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
*.log
logs/

# Database
*.db
*.sqlite3

# Docker
.docker/

# Testing
.coverage
.pytest_cache/
htmlcov/

# Temporary files
*.tmp
*.temp
EOF

print_success ".gitignore created"

print_success "Project initialization completed!"

echo ""
print_status "Project Structure Created:"
echo "  📁 docs/ - Comprehensive documentation"
echo "  📁 src/ - Source code with multi-agent system"
echo "  📁 PRPs/ - Product Requirement Prompts"
echo "  📁 archon-projects/ - Archon project containers"
echo "  📁 scripts/ - Automation and setup scripts"
echo "  📁 tests/ - Test suite"
echo "  📁 docker/ - Docker configuration"

echo ""
print_status "Configuration Files Created:"
echo "  ⚙️  .env.example - Environment configuration template"
echo "  ⚙️  pyproject.toml - Python project configuration"
echo "  ⚙️  docker-compose.dev.yml - Development services"
echo "  ⚙️  CLAUDE.md - Claude Code instructions"
echo "  ⚙️  .gitignore - Git ignore patterns"

echo ""
print_status "Next Steps:"
echo "  1. Edit .env file with your Data for SEO API credentials"
echo "  2. Run: ./scripts/dev-start.sh (starts development services)"
echo "  3. Run: ./scripts/seo-setup.sh (sets up SEO-specific components)"
echo "  4. Install dependencies: uv sync"
echo "  5. Initialize project context: claude /prime-core"
echo "  6. Create your first SEO PRP: claude /prp-base-create 'implement SEO feature'"

echo ""
print_success "🎉 Data for SEO project is ready for development!"
print_success "🚀 Start building intelligent SEO automation systems!"
