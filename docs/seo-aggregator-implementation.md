name: "SEO Analytics Aggregator Platform - Implementation PRP"
description: |
  Detailed implementation plan for building a scalable SEO analytics platform with data collection,
  processing, and analysis capabilities using the agent framework.

---

## Goal

**Feature Goal**: Implement a comprehensive SEO analytics aggregation platform that efficiently collects, processes, and analyzes SEO data from multiple sources.

**Deliverable**: 
- Scalable data collection system
- Real-time analytics processing
- RESTful API for data access
- Monitoring and management dashboard

**Success Definition**: System successfully aggregates SEO data from multiple sources with >99% accuracy, processes in real-time, and serves analytics via API with <200ms latency.

## User Persona

**Target User**: SEO professionals and marketing teams

**Use Case**: Collect and analyze SEO metrics across multiple websites/domains

**User Journey**:
1. Configure data sources and credentials
2. System collects and processes SEO data
3. Access analytics via API/dashboard
4. Generate custom reports and insights

**Pain Points Addressed**:
- Manual data collection from multiple sources
- Inconsistent data formats
- Slow processing and analysis
- Limited real-time insights

## Why

- Enable data-driven SEO optimization
- Automate manual data collection
- Standardize SEO metrics analysis
- Scale analytics capabilities
- Reduce analysis time and effort

## What

A production-ready SEO analytics platform with:

### Core Features
- Multi-source data collection system
- Real-time data processing pipeline
- Analytics computation engine
- RESTful API interface
- Monitoring and alerting

### Success Criteria
- [ ] Data collection from major SEO APIs working
- [ ] Real-time processing with <1min latency
- [ ] API response time <200ms for 95th percentile
- [ ] >99% data collection accuracy
- [ ] Scalable to 1000+ domains
- [ ] Comprehensive error handling
- [ ] Full monitoring coverage

## All Needed Context

### Context Completeness Check

_This PRP provides complete implementation details, patterns, and validation criteria for building the SEO analytics platform._

### Documentation & References

```yaml
# Core Implementation
- file: src/agents/base/agent_interface.py
  why: Base agent patterns for data collection
  pattern: Async operation handling and state management
  gotcha: Proper error propagation in agent chain

- file: src/knowledge/vector_store/chroma_client.py
  why: Data storage and retrieval patterns
  pattern: Async database operations
  gotcha: Batch operation size limits

- file: src/api/rest/base_router.py
  why: API endpoint implementation patterns
  pattern: FastAPI route organization
  gotcha: Proper response models and validation

- file: src/config/settings.py
  why: Configuration management patterns
  pattern: Environment variable handling
  gotcha: Secure credential management

# Testing & Validation
- file: tests/test_models.py
  why: Test structure and patterns
  pattern: Async test implementation
  gotcha: Mock external dependencies

- docfile: PRPs/ai_docs/cc_commands.md
  why: Command patterns for tools
  section: API integration patterns
```

### Current Codebase Structure

```bash
src/
├── agents/            # Agent implementations
├── api/               # API endpoints
├── config/            # Configuration
├── knowledge/         # Data storage
└── models.py         # Data models
```

### Desired Codebase Structure

```bash
src/
├── agents/
│   └── seo/
│       ├── collector_agent.py     # Data collection
│       ├── processor_agent.py     # Data processing
│       └── analytics_agent.py     # Analysis logic
├── api/
│   └── seo/
│       ├── routes.py             # API endpoints
│       ├── models.py             # API models
│       └── dependencies.py       # API dependencies
├── services/
│   └── seo/
│       ├── collector.py          # Collection service
│       ├── processor.py          # Processing service
│       └── analytics.py          # Analytics service
├── models/
│   └── seo.py                    # Domain models
└── config/
    └── seo_settings.py           # SEO config
```

### Known Gotchas & Library Quirks

```python
# CRITICAL: Rate Limiting
# Search APIs have strict rate limits
# Implement exponential backoff and quota management

# CRITICAL: Data Freshness
# SEO data becomes stale quickly
# Use TTL-based caching and periodic updates

# CRITICAL: API Versioning
# External APIs may change without notice
# Implement adapter pattern for API clients

# CRITICAL: Data Volume
# SEO metrics can be extremely large
# Use efficient storage and pagination

# CRITICAL: Error Handling
# Network issues and API failures common
# Implement comprehensive retry logic
```

## Implementation Blueprint

### Data Models and Structure

```python
# Domain Models
class SEOMetrics(BaseModel):
    url: str
    metrics: Dict[str, float]
    timestamp: datetime
    source: str
    metadata: Dict[str, Any]
    
    class Config:
        frozen = True

class CrawlJob(BaseModel):
    id: str
    site_url: str
    config: CrawlConfig
    status: JobStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        frozen = True

# Service Models
class CollectorResult(BaseModel):
    job_id: str
    metrics: List[SEOMetrics]
    success: bool
    error: Optional[str] = None
    
class AnalyticsResult(BaseModel):
    site_id: str
    insights: Dict[str, Any]
    trends: List[TrendData]
    recommendations: List[str]
```

### Implementation Tasks

```yaml
Task 1: CREATE src/models/seo.py
  - IMPLEMENT: Core domain models (SEOMetrics, CrawlJob, etc.)
  - FOLLOW pattern: src/models.py base model structure
  - NAMING: Domain models with clear purpose
  - DEPENDENCIES: None - foundational models
  - PLACEMENT: Domain models directory

Task 2: CREATE src/services/seo/collector.py
  - IMPLEMENT: SEOCollectorService for data gathering
  - FOLLOW pattern: Existing service patterns with async
  - NAMING: Clear service methods (collect_metrics, etc.)
  - DEPENDENCIES: Import models from Task 1
  - PLACEMENT: SEO service directory

Task 3: CREATE src/services/seo/processor.py
  - IMPLEMENT: SEOProcessorService for data processing
  - FOLLOW pattern: Async processing patterns
  - NAMING: Process-focused method names
  - DEPENDENCIES: Collector service from Task 2
  - PLACEMENT: SEO service directory

Task 4: CREATE src/services/seo/analytics.py
  - IMPLEMENT: SEOAnalyticsService for insights
  - FOLLOW pattern: Analytics computation patterns
  - NAMING: Analysis-focused method names
  - DEPENDENCIES: Processor service from Task 3
  - PLACEMENT: SEO service directory

Task 5: CREATE src/agents/seo/collector_agent.py
  - IMPLEMENT: SEOCollectorAgent for orchestration
  - FOLLOW pattern: Base agent implementation
  - NAMING: Agent-specific method names
  - DEPENDENCIES: Services from Tasks 2-4
  - PLACEMENT: SEO agents directory

Task 6: CREATE src/api/seo/models.py
  - IMPLEMENT: API request/response models
  - FOLLOW pattern: FastAPI model patterns
  - NAMING: Clear API model names
  - DEPENDENCIES: Domain models from Task 1
  - PLACEMENT: SEO API directory

Task 7: CREATE src/api/seo/routes.py
  - IMPLEMENT: REST API endpoints
  - FOLLOW pattern: FastAPI route patterns
  - NAMING: RESTful endpoint names
  - DEPENDENCIES: API models from Task 6
  - PLACEMENT: SEO API directory

Task 8: CREATE src/config/seo_settings.py
  - IMPLEMENT: SEO-specific configuration
  - FOLLOW pattern: Pydantic settings pattern
  - NAMING: Clear config property names
  - DEPENDENCIES: None - configuration only
  - PLACEMENT: Config directory

Task 9: CREATE tests for all components
  - IMPLEMENT: Comprehensive test suite
  - FOLLOW pattern: Existing test patterns
  - NAMING: Clear test case names
  - COVERAGE: All core functionality
  - PLACEMENT: Tests alongside code
```

### Implementation Patterns

```python
# Collector Service Pattern
class SEOCollectorService:
    def __init__(self, settings: SEOSettings):
        self.settings = settings
        self.rate_limiter = RateLimiter()
        
    async def collect_metrics(self, site_url: str) -> CollectorResult:
        async with self.rate_limiter:
            try:
                metrics = await self._fetch_metrics(site_url)
                return CollectorResult(success=True, metrics=metrics)
            except Exception as e:
                return CollectorResult(success=False, error=str(e))

# Processor Service Pattern
class SEOProcessorService:
    async def process_metrics(self, metrics: List[SEOMetrics]) -> ProcessorResult:
        normalized = await self._normalize_metrics(metrics)
        validated = await self._validate_metrics(normalized)
        return ProcessorResult(metrics=validated)

# Analytics Service Pattern
class SEOAnalyticsService:
    async def compute_insights(self, site_id: str) -> AnalyticsResult:
        metrics = await self._get_site_metrics(site_id)
        insights = await self._analyze_metrics(metrics)
        return AnalyticsResult(insights=insights)

# API Route Pattern
@router.get("/sites/{site_id}/metrics")
async def get_site_metrics(
    site_id: str,
    service: SEOAnalyticsService = Depends(get_analytics_service)
) -> MetricsResponse:
    result = await service.get_metrics(site_id)
    return MetricsResponse(metrics=result.metrics)
```

### Integration Points

```yaml
DATABASES:
  - PostgreSQL: Metrics storage
  - Redis: Job queues and caching
  - Vector Store: Analytics data

EXTERNAL_APIS:
  - Google Search Console API
  - Ahrefs API
  - Moz API
  - Semrush API

MONITORING:
  - Prometheus metrics
  - Grafana dashboards
  - Alert manager

DEPLOYMENT:
  - Docker containers
  - Kubernetes orchestration
  - Load balancer configuration
```

## Validation Loop

### Level 1: Syntax & Style

```bash
# Run after each component
ruff check src/services/seo/ --fix
ruff check src/agents/seo/ --fix
ruff check src/api/seo/ --fix
mypy src/

# Expected: Zero style/type errors
```

### Level 2: Unit Tests

```bash
# Component testing
pytest src/services/seo/tests/ -v
pytest src/agents/seo/tests/ -v
pytest src/api/seo/tests/ -v

# Integration testing
pytest tests/integration/seo/ -v

# Expected: All tests pass with coverage
```

### Level 3: Integration Testing

```bash
# Start services
docker-compose up -d

# API health check
curl http://localhost:8000/health

# Collector test
curl -X POST http://localhost:8000/api/v1/seo/collect \
  -H "Content-Type: application/json" \
  -d '{"site_url": "example.com"}'

# Analytics test
curl http://localhost:8000/api/v1/seo/sites/123/metrics

# Expected: Successful API responses
```

### Level 4: Performance Testing

```bash
# Load testing
locust -f tests/performance/locustfile.py

# Benchmark critical paths
pytest tests/performance/ --benchmark-only

# Expected: Meet performance SLAs
```

## Final Validation Checklist

### Technical Validation
- [ ] All syntax checks pass
- [ ] 100% test coverage
- [ ] Performance benchmarks met
- [ ] Security audit complete

### Feature Validation
- [ ] Data collection working
- [ ] Processing pipeline efficient
- [ ] Analytics accurate
- [ ] API documented and tested

### Integration Validation
- [ ] All external APIs integrated
- [ ] Database operations optimal
- [ ] Caching effective
- [ ] Monitoring functional

---

## Anti-Patterns to Avoid

- ❌ Don't skip rate limiting - critical for API stability
- ❌ Don't store raw metrics - normalize first
- ❌ Don't ignore data freshness - implement TTL
- ❌ Don't block the event loop - use async
- ❌ Don't ignore partial failures - implement circuit breakers
- ❌ Don't cache everything - be selective
- ❌ Don't skip input validation - verify all data