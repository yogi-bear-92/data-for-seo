# SEO Automation Workflows Documentation

This document provides comprehensive documentation for the SEO automation workflows implemented in the Data for SEO framework.

## Overview

The SEO automation workflows provide end-to-end orchestration of multiple agents to perform comprehensive SEO analysis and optimization tasks. Each workflow is designed to handle specific aspects of SEO while maintaining a consistent interface and providing robust error handling, progress tracking, and result aggregation.

## Architecture

### Base Components

#### WorkflowEngine
The `WorkflowEngine` is the abstract base class that provides the foundation for all SEO workflows:

- **Progress Tracking**: Real-time monitoring of workflow execution
- **Error Handling**: Comprehensive error handling with retry logic
- **Status Management**: Workflow state management (pending, running, completed, failed, cancelled, paused)
- **Timeout Management**: Configurable timeouts to prevent hanging workflows
- **Result Aggregation**: Standardized result collection and reporting

#### Key Features
- Async execution with proper error handling
- Configurable retry logic with exponential backoff
- Real-time progress tracking with step-by-step monitoring
- Workflow pause/resume capabilities
- Comprehensive logging and metrics collection

### Workflow Status Lifecycle

```
PENDING → RUNNING → COMPLETED
    ↓        ↓         ↑
    ↓     PAUSED  ←   ↑
    ↓        ↓         ↑
    ↓     CANCELLED   ↑
    ↓                 ↑
    ↓ → FAILED ← ← ← ←
```

## Available Workflows

### 1. SEO Audit Workflow

**Purpose**: Comprehensive website SEO analysis covering technical, content, and performance aspects.

**Key Features**:
- Parallel execution for improved performance
- Technical SEO analysis (crawlability, indexability, site structure)
- Content analysis (keyword optimization, readability, structure)
- Performance analysis (page speed, Core Web Vitals)
- Mobile optimization analysis
- Optional competitor analysis integration

**Usage**:
```python
from data_for_seo.workflows import SEOAuditWorkflow

# Initialize workflow
workflow = SEOAuditWorkflow({
    'parallel_execution': True,
    'include_competitor_analysis': True,
    'depth_level': 'standard'  # basic, standard, deep
})

# Execute audit
result = await workflow.execute({
    'url': 'https://example.com',
    'keywords': ['seo', 'optimization'],
    'competitors': ['https://competitor1.com'],
    'pages_to_audit': 50,
    'mobile_audit': True
})
```

**Output**:
- Overall SEO score and analysis summary
- Detailed technical, content, and performance metrics
- Prioritized recommendations with implementation timeline
- Competitor comparison insights (if enabled)

### 2. Keyword Tracking Workflow

**Purpose**: Automated keyword position monitoring with trend analysis and alerts.

**Key Features**:
- Multi-search engine tracking (Google, Bing, Yahoo, etc.)
- SERP feature monitoring (featured snippets, local packs, etc.)
- Historical trend analysis and change detection
- Automated alert generation for significant ranking changes
- Competitor position tracking
- Local search monitoring

**Usage**:
```python
from data_for_seo.workflows import KeywordTrackingWorkflow

# Initialize workflow
workflow = KeywordTrackingWorkflow({
    'tracking_frequency': 'daily',
    'search_engines': ['google', 'bing'],
    'alert_threshold': 5,  # Position change threshold
    'historical_days': 30
})

# Execute tracking
result = await workflow.execute({
    'url': 'https://example.com',
    'keywords': ['keyword1', 'keyword2', 'keyword3'],
    'search_engines': ['google', 'bing'],
    'locations': ['US', 'UK'],
    'device_types': ['desktop', 'mobile'],
    'competitor_tracking': True,
    'competitors': ['https://competitor.com']
})
```

**Output**:
- Current keyword positions across all specified parameters
- Ranking trends and historical comparisons
- SERP feature analysis and opportunities
- Automated alerts for significant changes
- Competitor position insights
- Comprehensive tracking reports

### 3. Content Optimization Workflow

**Purpose**: Content analysis and optimization recommendations for improved SEO performance.

**Key Features**:
- Keyword density and placement analysis
- Readability and engagement factor analysis
- SEO element optimization (titles, meta descriptions, headings)
- Content structure and hierarchy analysis
- Competitor content comparison
- User intent alignment analysis

**Usage**:
```python
from data_for_seo.workflows import ContentOptimizationWorkflow

# Initialize workflow
workflow = ContentOptimizationWorkflow({
    'analysis_depth': 'standard',  # basic, standard, deep
    'include_competitor_content': True,
    'optimization_focus': ['seo', 'readability', 'engagement']
})

# Execute optimization analysis
result = await workflow.execute({
    'url': 'https://example.com/article',
    'target_keywords': ['content optimization', 'seo content'],
    'competitors': ['https://competitor.com/similar-article'],
    'content_type': 'blog'
})
```

**Output**:
- Comprehensive content analysis report
- Keyword optimization recommendations
- Readability and engagement improvements
- SEO element optimization suggestions
- Content gap analysis against competitors
- Prioritized optimization action plan

### 4. Competitor Analysis Workflow

**Purpose**: Competitive SEO intelligence gathering and analysis.

**Key Features**:
- Keyword gap analysis and opportunity identification
- Ranking comparison across multiple keywords
- Content strategy analysis and benchmarking
- Backlink profile comparison and link opportunities
- Technical SEO comparison
- Market share and visibility analysis

**Usage**:
```python
from data_for_seo.workflows import CompetitorAnalysisWorkflow

# Initialize workflow
workflow = CompetitorAnalysisWorkflow({
    'analysis_scope': 'comprehensive',  # basic, standard, comprehensive
    'competitor_limit': 5,
    'include_backlink_analysis': True,
    'include_content_analysis': True
})

# Execute competitor analysis
result = await workflow.execute({
    'target_url': 'https://example.com',
    'competitors': [
        'https://competitor1.com',
        'https://competitor2.com',
        'https://competitor3.com'
    ],
    'keywords': ['target keyword 1', 'target keyword 2']
})
```

**Output**:
- Keyword gap analysis with opportunities
- Competitive ranking comparison
- Content strategy insights and gaps
- Backlink opportunities and link building targets
- Market positioning and share analysis
- Strategic recommendations and action plan

### 5. Technical SEO Workflow

**Purpose**: Technical SEO audit and recommendations for improved search engine crawlability and performance.

**Key Features**:
- Crawlability and indexability analysis
- Site structure and URL optimization audit
- Performance and Core Web Vitals analysis
- Mobile optimization assessment
- Security and HTTPS implementation review
- Schema markup and accessibility analysis

**Usage**:
```python
from data_for_seo.workflows import TechnicalSEOWorkflow

# Initialize workflow
workflow = TechnicalSEOWorkflow({
    'audit_depth': 'comprehensive',  # basic, standard, comprehensive
    'include_performance': True,
    'include_mobile': True,
    'include_security': True
})

# Execute technical audit
result = await workflow.execute({
    'url': 'https://example.com',
    'pages_to_audit': 100
})
```

**Output**:
- Overall technical SEO score
- Crawlability and indexability issues
- Performance optimization recommendations
- Mobile and security assessment
- Schema markup opportunities
- Prioritized technical improvements

## Configuration Options

### Global Configuration

All workflows support the following global configuration options:

```python
config = {
    'max_retries': 3,           # Maximum retry attempts
    'retry_delay': 5.0,         # Delay between retries (seconds)
    'timeout': 300.0,           # Workflow timeout (seconds)
}
```

### Workflow-Specific Configuration

Each workflow supports specific configuration options:

#### SEO Audit Workflow
```python
config = {
    'parallel_execution': True,
    'include_competitor_analysis': True,
    'depth_level': 'standard',  # basic, standard, deep
}
```

#### Keyword Tracking Workflow
```python
config = {
    'tracking_frequency': 'daily',
    'search_engines': ['google', 'bing'],
    'alert_threshold': 5,
    'historical_days': 30,
}
```

#### Content Optimization Workflow
```python
config = {
    'analysis_depth': 'standard',
    'include_competitor_content': True,
    'optimization_focus': ['seo', 'readability', 'engagement'],
}
```

#### Competitor Analysis Workflow
```python
config = {
    'analysis_scope': 'comprehensive',
    'competitor_limit': 5,
    'include_backlink_analysis': True,
    'include_content_analysis': True,
}
```

#### Technical SEO Workflow
```python
config = {
    'audit_depth': 'comprehensive',
    'include_performance': True,
    'include_mobile': True,
    'include_security': True,
    'page_limit': 100,
}
```

## Progress Monitoring

All workflows provide real-time progress monitoring:

```python
# Execute workflow
result_task = asyncio.create_task(workflow.execute(parameters))

# Monitor progress
while not result_task.done():
    progress = workflow.get_progress()
    if progress:
        print(f"Progress: {progress.progress_percentage:.1f}%")
        print(f"Current step: {progress.current_step}")
        print(f"Completed steps: {progress.completed_steps}/{progress.total_steps}")
    
    await asyncio.sleep(5)  # Check every 5 seconds

# Get final result
result = await result_task
```

## Error Handling

The workflows implement comprehensive error handling:

### Retry Logic
- Automatic retry on transient failures
- Configurable retry count and delay
- Exponential backoff for rate limiting

### Error Recovery
- Graceful handling of agent failures
- Partial result preservation
- Detailed error reporting and logging

### Timeout Management
- Configurable workflow timeouts
- Step-level timeout handling
- Graceful cancellation support

## Performance Optimization

### Parallel Execution
- Support for parallel agent execution where applicable
- Optimized task scheduling and resource management
- Configurable concurrency limits

### Large-Scale Operations
- Efficient handling of 1000+ URLs in audit workflows
- Support for 10,000+ keywords in tracking workflows
- Optimized memory usage and processing

### Caching and Optimization
- Result caching for repeated operations
- Efficient data structures for large datasets
- Optimized API usage patterns

## Integration Examples

### Basic Workflow Execution

```python
import asyncio
from data_for_seo.workflows import SEOAuditWorkflow

async def run_seo_audit():
    workflow = SEOAuditWorkflow()
    
    result = await workflow.execute({
        'url': 'https://example.com',
        'keywords': ['seo', 'optimization']
    })
    
    if result.success:
        print(f"Audit completed successfully!")
        print(f"Overall score: {result.data['summary']['overall_seo_score']}")
    else:
        print(f"Audit failed: {result.message}")

# Run the workflow
asyncio.run(run_seo_audit())
```

### Workflow Chaining

```python
async def comprehensive_seo_analysis(url: str, keywords: list):
    """Run multiple workflows in sequence for comprehensive analysis."""
    
    # Technical audit first
    tech_workflow = TechnicalSEOWorkflow()
    tech_result = await tech_workflow.execute({'url': url})
    
    # Content optimization
    content_workflow = ContentOptimizationWorkflow()
    content_result = await content_workflow.execute({
        'url': url,
        'target_keywords': keywords
    })
    
    # Keyword tracking
    tracking_workflow = KeywordTrackingWorkflow()
    tracking_result = await tracking_workflow.execute({
        'url': url,
        'keywords': keywords
    })
    
    return {
        'technical': tech_result,
        'content': content_result,
        'tracking': tracking_result
    }
```

## Best Practices

### 1. Workflow Configuration
- Always validate input parameters before execution
- Use appropriate timeout values for your use case
- Configure retry logic based on expected failure rates

### 2. Progress Monitoring
- Implement progress monitoring for long-running workflows
- Provide user feedback during execution
- Handle workflow cancellation gracefully

### 3. Error Handling
- Always check workflow results before processing data
- Implement proper logging for debugging
- Handle partial failures appropriately

### 4. Performance Optimization
- Use parallel execution for independent operations
- Implement appropriate rate limiting for API calls
- Monitor resource usage for large-scale operations

### 5. Result Processing
- Validate workflow results before using data
- Implement proper error handling for result processing
- Store results appropriately for future reference

## Troubleshooting

### Common Issues

1. **Workflow Timeout**
   - Increase timeout configuration
   - Check network connectivity
   - Verify API rate limits

2. **Parameter Validation Errors**
   - Ensure all required parameters are provided
   - Validate URL formats and keyword lists
   - Check parameter value ranges

3. **Agent Communication Failures**
   - Verify agent configuration
   - Check network connectivity
   - Review agent error logs

4. **Memory Issues with Large Datasets**
   - Reduce batch sizes
   - Implement streaming processing
   - Monitor memory usage

### Debug Mode

Enable debug logging for detailed troubleshooting:

```python
import logging
logging.getLogger('data_for_seo.workflows').setLevel(logging.DEBUG)
```

## API Reference

See the individual workflow class documentation for detailed API reference and method signatures.

## Contributing

When adding new workflows or modifying existing ones:

1. Inherit from `WorkflowEngine` base class
2. Implement required abstract methods
3. Follow the established patterns for error handling and progress tracking
4. Add comprehensive tests for new functionality
5. Update documentation accordingly

## License

This workflow implementation is part of the Data for SEO framework and is subject to the same license terms.