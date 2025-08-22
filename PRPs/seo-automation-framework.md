name: "SEO Automation Framework Implementation - Data for SEO Integration"
description: |
  Complete implementation of a comprehensive SEO automation framework using Data for SEO APIs,
  multi-agent system, and Agent Factory patterns for autonomous SEO analysis, optimization,
  and monitoring workflows.

---

## Goal

**Feature Goal**: Build a complete SEO Automation Framework that autonomously performs comprehensive SEO analysis, content optimization, technical audits, and performance monitoring using Data for SEO APIs and specialized AI agents.

**Deliverable**: Multi-agent SEO system with Data for SEO API integration, persistent knowledge base, automated workflows, and comprehensive SEO analysis capabilities running on Agent Factory infrastructure.

**Success Definition**: The system can analyze websites, identify SEO opportunities, generate optimization recommendations, and track performance improvements autonomously with minimal human intervention.

## User Persona

**Target User**: SEO professionals, digital marketing agencies, website owners, and development teams needing comprehensive SEO automation

**Use Case**: Submit website URLs for analysis and receive complete SEO audits, optimization recommendations, keyword research, and ongoing performance monitoring

**User Journey**: 
1. User submits website URL and target keywords via API/CLI
2. System performs comprehensive SEO analysis using multiple agents
3. Agents collaborate to analyze content, technical SEO, and performance
4. System generates actionable optimization recommendations
5. User receives detailed reports and can track improvements over time
6. System continuously monitors and alerts on ranking changes

**Pain Points Addressed**: 
- Manual SEO analysis is time-consuming and error-prone
- Inconsistent SEO audit processes across team members
- Difficulty tracking SEO improvements over time
- Limited integration between SEO tools and development workflows
- Expensive enterprise SEO tools with limited customization

## Why

- **Automated SEO Workflows**: Enable 24/7 SEO monitoring and analysis without manual intervention
- **Comprehensive Analysis**: Multi-dimensional SEO analysis covering content, technical, and performance aspects
- **Data-Driven Insights**: Leverage Data for SEO's comprehensive database for accurate keyword and ranking data
- **Agent Factory Integration**: Utilize proven multi-agent patterns for reliable, scalable SEO automation
- **Cost-Effective**: Provide enterprise-level SEO capabilities at fraction of traditional tool costs
- **Customizable Workflows**: Tailor SEO analysis and reporting to specific business needs

## What

A comprehensive SEO automation framework that transforms website URLs into actionable SEO insights through:

### Core Capabilities
- **Multi-Agent SEO Team**: Specialized agents for analysis, data collection, and processing
- **Data for SEO Integration**: Complete API integration for keyword research, ranking data, and SERP analysis
- **Persistent Knowledge Base**: Vector database storing SEO patterns, successful optimizations, and domain expertise
- **Automated Workflows**: End-to-end SEO analysis pipelines with minimal human intervention
- **Comprehensive Reporting**: Detailed SEO reports with actionable recommendations and priority scoring

### Success Criteria

- [ ] Complete Data for SEO API integration with authentication and rate limiting
- [ ] Three specialized SEO agents (Analyzer, Collector, Processor) working in coordination
- [ ] Comprehensive SEO analysis covering 15+ technical and content factors
- [ ] Automated keyword research and ranking tracking capabilities
- [ ] Persistent storage of SEO data with historical trend analysis
- [ ] RESTful API endpoints for all SEO operations
- [ ] Comprehensive test suite with 80%+ code coverage
- [ ] Production-ready deployment configuration
- [ ] Real-time SEO monitoring and alerting system

## All Needed Context

### Context Completeness Check

_This PRP provides complete context for implementing a production-ready SEO automation framework using Agent Factory patterns, Data for SEO APIs, and modern Python development practices._

### Documentation & References

```yaml
# MUST READ - Include these in your context window
- url: https://docs.dataforseo.com/v3/
  why: Complete Data for SEO API documentation for all endpoints
  critical: Authentication, rate limiting, and response formats

- file: /Users/yogi/Projects/vlada/Ai/agent-factory/src/agents/base_agent.py
  why: Agent Factory base agent patterns for multi-agent coordination
  pattern: Agent lifecycle, task execution, error handling
  gotcha: Async/await patterns and proper resource cleanup

- file: /Users/yogi/Projects/vlada/Ai/agent-factory/src/models/base.py
  why: Base model patterns for Pydantic models and validation
  pattern: ExecutionResult, task status management, error handling
  gotcha: Pydantic v2 patterns and field validation

- file: /Users/yogi/Projects/vlada/Ai/agent-factory/src/knowledge/vector_store/chroma_client.py
  why: Vector database integration patterns for knowledge storage
  pattern: ChromaDB client setup, embedding generation, similarity search
  gotcha: Async operations and proper connection management

- docfile: PRPs/ai_docs/dataforseo_integration.md
  why: Data for SEO API integration patterns and best practices
  section: Authentication, rate limiting, error handling

- docfile: PRPs/ai_docs/seo_analysis_patterns.md
  why: SEO analysis methodologies and scoring algorithms
  section: Technical SEO, content analysis, performance metrics
```

### Current Codebase tree (run `tree` in the root of the project) to get an overview of the codebase

```bash
data-for-seo/
├── docs/
│   ├── ARCHITECTURE.md
│   ├── ONBOARDING.md
│   ├── QUICKSTART.md
│   └── seo-aggregator-implementation.md
├── pyproject.toml
├── README.md
├── scripts/
│   └── init-project.sh
├── setup.sh
├── src/
│   └── data_for_seo/
│       ├── __init__.py
│       ├── agents/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   └── seo_analyzer.py
│       ├── api/
│       ├── communication/
│       ├── config/
│       │   ├── __init__.py
│       │   └── settings.py
│       ├── knowledge/
│       ├── models/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   └── seo.py
│       ├── tools/
│       └── workflows/
└── tests/
    ├── fixtures/
    ├── integration/
    └── unit/
```

### Desired Codebase tree with files to be added and responsibility of file

```bash
data-for-seo/
├── src/data_for_seo/
│   ├── agents/
│   │   ├── seo_collector.py          # Data for SEO API integration agent
│   │   └── seo_processor.py          # SEO data processing and analysis agent
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI application entry point
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── seo_analysis.py       # SEO analysis endpoints
│   │   │   ├── keyword_research.py   # Keyword research endpoints
│   │   │   └── health.py             # Health check endpoints
│   │   └── middleware/
│   │       ├── __init__.py
│   │       ├── auth.py               # Authentication middleware
│   │       └── rate_limiting.py      # Rate limiting middleware
│   ├── communication/
│   │   ├── __init__.py
│   │   ├── redis_client.py           # Redis pub/sub for agent coordination
│   │   └── message_bus.py            # Message bus for inter-agent communication
│   ├── knowledge/
│   │   ├── __init__.py
│   │   ├── vector_store.py           # ChromaDB integration for SEO knowledge
│   │   └── seo_patterns.py           # SEO pattern recognition and storage
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── dataforseo_client.py      # Data for SEO API client
│   │   ├── seo_analyzer_tool.py      # SEO analysis tool wrapper
│   │   └── keyword_research_tool.py  # Keyword research tool wrapper
│   └── workflows/
│       ├── __init__.py
│       ├── seo_audit_workflow.py     # Complete SEO audit workflow
│       └── keyword_tracking_workflow.py # Keyword tracking workflow
├── PRPs/
│   ├── ai_docs/
│   │   ├── dataforseo_integration.md # Data for SEO API documentation
│   │   └── seo_analysis_patterns.md  # SEO analysis methodologies
│   └── scripts/
│       └── prp_runner.py             # PRP execution script
└── tests/
    ├── unit/
    │   ├── test_agents/
    │   ├── test_api/
    │   └── test_tools/
    └── integration/
        ├── test_dataforseo_integration.py
        └── test_seo_workflows.py
```

### Known Gotchas of our codebase & Library Quirks

```python
# CRITICAL: Data for SEO API requires specific authentication
# Example: Basic auth with username/password, not API key
auth = aiohttp.BasicAuth(username, password)

# CRITICAL: Data for SEO has strict rate limiting
# Example: Max 100 requests per minute, need exponential backoff
await asyncio.sleep(0.6)  # Minimum delay between requests

# CRITICAL: Pydantic v2 patterns for model validation
# Example: Use ConfigDict instead of class Config
model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

# CRITICAL: ChromaDB requires specific embedding dimensions
# Example: sentence-transformers/all-MiniLM-L6-v2 produces 384-dim vectors
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# CRITICAL: FastAPI async patterns for proper performance
# Example: All database/API operations must be async
async def analyze_seo(url: str) -> SEOAnalysis:
    async with aiohttp.ClientSession() as session:
        # API calls here
```

## Implementation Blueprint

### Data models and structure

Create the core data models to ensure type safety and consistency across all SEO operations.

```python
# SEO-specific Pydantic models for Data for SEO API integration
- KeywordResearchRequest/Response models
- SEOAnalysisRequest/Response models  
- RankingTrackingRequest/Response models
- TechnicalAuditRequest/Response models
- Data for SEO API response models
- Agent task models for SEO operations
```

### Implementation Tasks (ordered by dependencies)

```yaml
Task 1: CREATE src/data_for_seo/tools/dataforseo_client.py
  - IMPLEMENT: DataForSEOClient class with async HTTP client
  - FOLLOW pattern: Agent Factory HTTP client patterns (async/await, error handling)
  - NAMING: DataForSEOClient class, async def get_*, post_*, methods
  - DEPENDENCIES: aiohttp, pydantic models from models/seo.py
  - PLACEMENT: Tools layer for external API integration

Task 2: CREATE src/data_for_seo/agents/seo_collector.py
  - IMPLEMENT: SEOCollectorAgent class extending BaseSEOAgent
  - FOLLOW pattern: src/data_for_seo/agents/base.py (agent structure, task execution)
  - NAMING: SEOCollectorAgent class, async def collect_* methods
  - DEPENDENCIES: DataForSEOClient from Task 1, SEO models
  - PLACEMENT: Agent layer for data collection operations

Task 3: CREATE src/data_for_seo/agents/seo_processor.py
  - IMPLEMENT: SEOProcessorAgent class for data processing and analysis
  - FOLLOW pattern: src/data_for_seo/agents/base.py (agent lifecycle, error handling)
  - NAMING: SEOProcessorAgent class, async def process_* methods
  - DEPENDENCIES: SEO models, vector store for knowledge storage
  - PLACEMENT: Agent layer for data processing operations

Task 4: CREATE src/data_for_seo/knowledge/vector_store.py
  - IMPLEMENT: SEOVectorStore class for ChromaDB integration
  - FOLLOW pattern: Agent Factory ChromaDB patterns (embedding, similarity search)
  - NAMING: SEOVectorStore class, async def store_*, query_* methods
  - DEPENDENCIES: ChromaDB, sentence-transformers, SEO models
  - PLACEMENT: Knowledge layer for persistent storage

Task 5: CREATE src/data_for_seo/workflows/seo_audit_workflow.py
  - IMPLEMENT: SEOAuditWorkflow class orchestrating multiple agents
  - FOLLOW pattern: Agent Factory workflow patterns (agent coordination, task management)
  - NAMING: SEOAuditWorkflow class, async def execute_audit method
  - DEPENDENCIES: All three SEO agents, communication layer
  - PLACEMENT: Workflow layer for process orchestration

Task 6: CREATE src/data_for_seo/api/main.py
  - IMPLEMENT: FastAPI application with SEO endpoints
  - FOLLOW pattern: Agent Factory API patterns (FastAPI setup, middleware)
  - NAMING: FastAPI app instance, router registration
  - DEPENDENCIES: FastAPI, SEO workflows, authentication middleware
  - PLACEMENT: API layer for external interface

Task 7: CREATE src/data_for_seo/api/routes/seo_analysis.py
  - IMPLEMENT: SEO analysis REST endpoints
  - FOLLOW pattern: Agent Factory API route patterns (async endpoints, error handling)
  - NAMING: router instance, async def analyze_*, audit_* endpoints
  - DEPENDENCIES: SEO workflows, Pydantic request/response models
  - PLACEMENT: API routes for SEO operations

Task 8: CREATE comprehensive test suite
  - IMPLEMENT: Unit tests for all agents, tools, and workflows
  - FOLLOW pattern: Agent Factory test patterns (pytest, async testing, mocking)
  - NAMING: test_* files, test_* functions with descriptive scenarios
  - COVERAGE: All public methods, error cases, integration scenarios
  - PLACEMENT: Tests directory with unit and integration subdirectories
```

### Implementation Patterns & Key Details

```python
# Data for SEO API Client Pattern
class DataForSEOClient:
    def __init__(self, username: str, password: str):
        self.auth = aiohttp.BasicAuth(username, password)
        self.base_url = "https://api.dataforseo.com/v3"
        self.rate_limiter = AsyncRateLimiter(100, 60)  # 100 requests per minute
    
    async def make_request(self, endpoint: str, data: dict) -> dict:
        # PATTERN: Rate limiting before each request
        await self.rate_limiter.acquire()
        
        # PATTERN: Proper error handling with retries
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/{endpoint}",
                json=data,
                auth=self.auth
            ) as response:
                # CRITICAL: Handle Data for SEO specific error codes
                if response.status == 429:  # Rate limit exceeded
                    await asyncio.sleep(60)  # Wait before retry
                    return await self.make_request(endpoint, data)
                
                response.raise_for_status()
                return await response.json()

# SEO Agent Pattern
class SEOCollectorAgent(BaseSEOAgent):
    def __init__(self):
        super().__init__(
            name="SEO Collector",
            description="Collects SEO data from Data for SEO APIs",
            agent_type="seo_collector"
        )
        self.client = DataForSEOClient(
            username=self.settings.dataforseo_username,
            password=self.settings.dataforseo_password
        )
    
    async def _execute_task_impl(self, task: SEOTask) -> ExecutionResult:
        # PATTERN: Task type routing with validation
        if task.task_type == "keyword_research":
            return await self._collect_keyword_data(task)
        elif task.task_type == "ranking_data":
            return await self._collect_ranking_data(task)
        # CRITICAL: Always handle unknown task types
        else:
            return ExecutionResult.failure_result(
                message=f"Unsupported task type: {task.task_type}",
                errors=[f"SEO Collector cannot handle {task.task_type}"]
            )

# Workflow Orchestration Pattern
class SEOAuditWorkflow:
    def __init__(self):
        self.analyzer = SEOAnalyzerAgent()
        self.collector = SEOCollectorAgent()
        self.processor = SEOProcessorAgent()
    
    async def execute_audit(self, url: str, keywords: List[str]) -> SEOAnalysis:
        # PATTERN: Parallel agent execution for efficiency
        tasks = [
            self.analyzer.execute_task(self.create_analysis_task(url)),
            self.collector.execute_task(self.create_collection_task(url, keywords)),
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # PATTERN: Result aggregation with error handling
        analysis_result, collection_result = results
        
        if isinstance(analysis_result, Exception):
            # Handle analysis failure
            pass
        
        # CRITICAL: Process results and generate final analysis
        return await self.processor.execute_task(
            self.create_processing_task(analysis_result, collection_result)
        )
```

### Integration Points

```yaml
DATABASE:
  - setup: "ChromaDB persistent storage in ./data/chroma"
  - collections: "seo_knowledge, keyword_data, ranking_history"
  - embeddings: "sentence-transformers/all-MiniLM-L6-v2 (384 dimensions)"

CONFIG:
  - add to: src/data_for_seo/config/settings.py
  - pattern: "DATAFORSEO_USERNAME = Field(default=None, description='Data for SEO username')"
  - environment: "Load from .env file with validation"

REDIS:
  - setup: "Redis for agent communication and task queuing"
  - pattern: "redis://localhost:6379/0 with connection pooling"
  - usage: "Pub/sub for agent coordination, caching for API responses"

API_ROUTES:
  - add to: src/data_for_seo/api/main.py
  - pattern: "app.include_router(seo_router, prefix='/api/v1/seo')"
  - endpoints: "/analyze, /keywords, /rankings, /audit"
```

## Validation Loop

### Level 1: Syntax & Style (Immediate Feedback)

```bash
# Run after each file creation - fix before proceeding
ruff check src/data_for_seo/ --fix     # Auto-format and fix linting issues
mypy src/data_for_seo/                 # Type checking with strict mode
ruff format src/data_for_seo/          # Ensure consistent formatting

# Project-wide validation
ruff check . --fix
mypy src/
ruff format .

# Expected: Zero errors. If errors exist, READ output and fix before proceeding.
```

### Level 2: Unit Tests (Component Validation)

```bash
# Test each component as it's created
uv run pytest tests/unit/test_agents/test_seo_collector.py -v
uv run pytest tests/unit/test_tools/test_dataforseo_client.py -v
uv run pytest tests/unit/test_workflows/test_seo_audit_workflow.py -v

# Full test suite for affected areas
uv run pytest tests/unit/ -v
uv run pytest tests/integration/ -v

# Coverage validation
uv run pytest --cov=src/data_for_seo --cov-report=term-missing --cov-report=html

# Expected: All tests pass, coverage > 80%. If failing, debug and fix implementation.
```

### Level 3: Integration Testing (System Validation)

```bash
# Service startup validation
uv run python -m src.data_for_seo.api.main &
sleep 5  # Allow startup time

# Health check validation
curl -f http://localhost:8000/health || echo "Service health check failed"

# SEO analysis endpoint testing
curl -X POST http://localhost:8000/api/v1/seo/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "keywords": ["example", "test"]}' \
  | jq .

# Data for SEO API integration testing
curl -X POST http://localhost:8000/api/v1/seo/keywords \
  -H "Content-Type: application/json" \
  -d '{"keywords": ["seo", "optimization"], "location": "United States"}' \
  | jq .

# Agent coordination testing
curl -X POST http://localhost:8000/api/v1/seo/audit \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "comprehensive": true}' \
  | jq .

# Database validation
# Verify ChromaDB collections and data persistence
python -c "
import chromadb
client = chromadb.PersistentClient(path='./data/chroma')
collections = client.list_collections()
print(f'Collections: {[c.name for c in collections]}')
"

# Expected: All integrations working, proper responses, no connection errors
```

### Level 4: Creative & Domain-Specific Validation

```bash
# SEO Analysis Validation
# Test comprehensive SEO analysis with real websites
python -c "
import asyncio
from src.data_for_seo.workflows.seo_audit_workflow import SEOAuditWorkflow

async def test_seo_analysis():
    workflow = SEOAuditWorkflow()
    result = await workflow.execute_audit('https://example.com', ['example', 'test'])
    print(f'SEO Score: {result.seo_score}')
    print(f'Recommendations: {len(result.recommendations)}')

asyncio.run(test_seo_analysis())
"

# Data for SEO API Validation
# Test all major Data for SEO endpoints
python -c "
import asyncio
from src.data_for_seo.tools.dataforseo_client import DataForSEOClient

async def test_dataforseo():
    client = DataForSEOClient('username', 'password')
    
    # Test keyword research
    keywords = await client.get_keyword_data(['seo', 'optimization'])
    print(f'Keywords found: {len(keywords)}')
    
    # Test SERP analysis
    serp_data = await client.get_serp_data('seo tools', 'United States')
    print(f'SERP results: {len(serp_data)}')

asyncio.run(test_dataforseo())
"

# Performance Testing
# Test API response times and throughput
ab -n 100 -c 10 http://localhost:8000/api/v1/seo/analyze

# Load Testing for agent coordination
# Test multiple concurrent SEO audits
wrk -t4 -c20 -d30s --script=test_seo_load.lua http://localhost:8000/api/v1/seo/audit

# Knowledge Base Validation
# Test vector similarity search and knowledge retrieval
python -c "
import asyncio
from src.data_for_seo.knowledge.vector_store import SEOVectorStore

async def test_knowledge():
    store = SEOVectorStore()
    
    # Store SEO knowledge
    await store.store_seo_pattern('title optimization', 'Keep titles under 60 characters')
    
    # Query similar patterns
    results = await store.query_similar('title length best practices')
    print(f'Similar patterns found: {len(results)}')

asyncio.run(test_knowledge())
"

# Expected: All creative validations pass, performance meets requirements
```

## Final Validation Checklist

### Technical Validation

- [ ] All 4 validation levels completed successfully
- [ ] All tests pass: `uv run pytest -v`
- [ ] No linting errors: `ruff check . --fix`
- [ ] No type errors: `mypy src/`
- [ ] No formatting issues: `ruff format . --check`
- [ ] Code coverage > 80%: `pytest --cov=src --cov-report=term-missing`

### Feature Validation

- [ ] Complete Data for SEO API integration with all major endpoints
- [ ] Three SEO agents working in coordination (Analyzer, Collector, Processor)
- [ ] Comprehensive SEO analysis covering 15+ factors
- [ ] Automated keyword research and ranking tracking
- [ ] Persistent knowledge storage with vector similarity search
- [ ] RESTful API endpoints for all SEO operations
- [ ] Real-time agent coordination via Redis pub/sub
- [ ] Error handling and rate limiting for external APIs

### SEO Domain Validation

- [ ] Technical SEO analysis (HTTPS, mobile-friendly, page speed, etc.)
- [ ] Content analysis (title, meta description, keyword density, etc.)
- [ ] On-page SEO factors (headings, internal links, images, etc.)
- [ ] Keyword research with search volume and difficulty data
- [ ] SERP analysis and ranking position tracking
- [ ] Competitor analysis and content gap identification
- [ ] SEO recommendations with priority scoring
- [ ] Historical data tracking and trend analysis

### Code Quality Validation

- [ ] Follows Agent Factory patterns and naming conventions
- [ ] Proper async/await usage throughout
- [ ] Comprehensive error handling with specific exceptions
- [ ] Pydantic v2 models with proper validation
- [ ] ChromaDB integration with proper embedding handling
- [ ] Redis pub/sub for agent coordination
- [ ] FastAPI best practices with proper middleware
- [ ] Comprehensive logging with structured output

### Documentation & Deployment

- [ ] API documentation with OpenAPI/Swagger
- [ ] Environment variables documented in .env.example
- [ ] Docker configuration for production deployment
- [ ] Monitoring and health check endpoints
- [ ] Rate limiting and authentication middleware
- [ ] Proper secret management and security practices

---

## Anti-Patterns to Avoid

- ❌ Don't make synchronous calls to Data for SEO API - use async/await
- ❌ Don't ignore rate limiting - implement proper backoff strategies
- ❌ Don't store API credentials in code - use environment variables
- ❌ Don't skip error handling for external API failures
- ❌ Don't use blocking operations in async agent methods
- ❌ Don't hardcode SEO scoring algorithms - make them configurable
- ❌ Don't ignore ChromaDB embedding dimensions - ensure consistency
- ❌ Don't skip validation gates - they prevent production issues
