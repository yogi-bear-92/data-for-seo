# Product Requirement Prompt (PRP) Framework for Data for SEO

## Overview

This directory contains the PRP (Product Requirement Prompt) framework implementation for the Data for SEO project, following the exact methodology from Agent Factory.

## What is a PRP?

A PRP is a structured prompt that supplies an AI coding agent with everything it needs to deliver a vertical slice of working software—no more, no less.

**PRP = PRD + curated codebase intelligence + agent/runbook**

## Directory Structure

```
PRPs/
├── README.md                           # This file
├── seo-automation-framework.md         # Main PRP for SEO automation implementation
├── ai_docs/                           # AI-specific documentation
│   ├── dataforseo_integration.md      # Data for SEO API integration guide
│   └── seo_analysis_patterns.md       # SEO analysis methodologies
├── scripts/
│   └── prp_runner.py                  # PRP execution script
├── templates/                         # PRP templates (future use)
└── completed/                         # Completed PRPs
```

## Available PRPs

### 1. SEO Automation Framework (`seo-automation-framework.md`)

**Status**: Ready for execution  
**Goal**: Complete implementation of SEO automation framework with Data for SEO integration  
**Agents**: SEO Analyzer, Collector, Processor  
**Deliverables**: Multi-agent SEO system with comprehensive analysis capabilities

## Execution

### Interactive Mode (Recommended)
```bash
# Execute PRP with interactive Claude Code session
uv run PRPs/scripts/prp_runner.py --prp seo-automation-framework --interactive
```

### Headless Mode
```bash
# Execute PRP in headless mode with JSON output
uv run PRPs/scripts/prp_runner.py --prp seo-automation-framework --output-format json

# Execute with streaming JSON for real-time monitoring
uv run PRPs/scripts/prp_runner.py --prp seo-automation-framework --output-format stream-json
```

### Custom PRP Path
```bash
# Execute specific PRP file
uv run PRPs/scripts/prp_runner.py --prp-path PRPs/custom-feature.md --interactive
```

## PRP Development Guidelines

### Context Requirements
- **Complete Documentation**: All necessary API docs, patterns, and examples
- **Codebase Intelligence**: Existing patterns and architectural decisions
- **Implementation Blueprint**: Step-by-step tasks with dependencies
- **Validation Gates**: Comprehensive testing and quality checks

### Validation Levels
1. **Syntax & Style**: Ruff, MyPy, formatting
2. **Unit Tests**: Component-level validation
3. **Integration Tests**: System-level validation  
4. **Domain-Specific**: SEO analysis validation

### Success Criteria
- [ ] All validation levels pass
- [ ] Feature requirements met
- [ ] Code quality standards maintained
- [ ] Documentation updated
- [ ] Tests achieve 80%+ coverage

## AI Documentation

### Data for SEO Integration (`ai_docs/dataforseo_integration.md`)
- Complete API integration patterns
- Authentication and rate limiting
- Error handling strategies
- Caching and performance optimization
- Testing patterns

### SEO Analysis Patterns (`ai_docs/seo_analysis_patterns.md`)
- Multi-dimensional SEO analysis framework
- Technical SEO analysis patterns
- Content quality scoring algorithms
- Recommendation engine implementation
- Performance metrics and benchmarks

## Best Practices

### PRP Creation
1. **Start with clear goal and success criteria**
2. **Provide complete context and documentation**
3. **Break down into ordered, dependency-aware tasks**
4. **Include comprehensive validation gates**
5. **Specify anti-patterns to avoid**

### Execution
1. **Review PRP thoroughly before execution**
2. **Use interactive mode for complex implementations**
3. **Monitor validation gates throughout development**
4. **Move completed PRPs to `completed/` directory**

### Quality Assurance
1. **All code must pass validation levels 1-4**
2. **Follow Agent Factory patterns and conventions**
3. **Maintain comprehensive test coverage**
4. **Document architectural decisions**

## Integration with Agent Factory

This PRP framework follows the exact patterns established in Agent Factory:

- **Multi-Agent Coordination**: Specialized agents working together
- **Knowledge Management**: Persistent vector storage for SEO patterns
- **Validation Gates**: Comprehensive quality assurance
- **Async Patterns**: Full async/await implementation
- **Error Handling**: Robust error management and logging
- **Configuration Management**: Environment-based settings

## Next Steps

1. **Execute Main PRP**: Run `seo-automation-framework.md` to implement core system
2. **Extend Functionality**: Create additional PRPs for specific SEO features
3. **Optimize Performance**: Implement caching and performance improvements
4. **Add Monitoring**: Implement comprehensive monitoring and alerting

## Support

For questions or issues with PRP execution:
1. Review the PRP documentation thoroughly
2. Check validation gate outputs for specific errors
3. Ensure all prerequisites are met (Python 3.12+, dependencies installed)
4. Verify environment configuration (Data for SEO credentials, etc.)

---

*This PRP framework enables autonomous development of production-ready SEO automation capabilities using proven Agent Factory patterns and methodologies.*
