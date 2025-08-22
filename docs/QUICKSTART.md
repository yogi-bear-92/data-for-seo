# Data for SEO - Quick Start Guide

Get up and running with SEO automation using the Agent Factory framework in 5 minutes.

> **📖 Common Setup Steps**: For detailed prerequisites and installation steps, see [Agent Factory Shared Components](../agent-factory/docs/SHARED_COMPONENTS.md#prerequisites)

## Quick Setup (1 minute)

Follow the [standard installation steps](../agent-factory/docs/SHARED_COMPONENTS.md#installation-steps) with these SEO-specific additions:

1. **Configure SEO API credentials**:
   ```bash
   cp .env.example .env
   # Edit .env with your Data for SEO API credentials
   ```

## Your First SEO PRP (2 minutes)

1. **Create a PRP for SEO automation**:
   ```bash
   claude /prp-base-create "implement SEO keyword analysis automation"
   ```

2. **Execute the PRP** (interactive mode):
   ```bash
   uv run PRPs/scripts/prp_runner.py --prp seo-keyword-analysis --interactive
   ```

3. **Review what was created**:
   ```bash
   # Check the generated PRP
   cat PRPs/seo-keyword-analysis.md
   
   # Review any changes made
   claude /review-staged-unstaged
   ```

## Essential Commands

> **📖 Complete Command Reference**: See [Agent Factory Shared Components - Essential Commands](../agent-factory/docs/SHARED_COMPONENTS.md#essential-commands) for core commands.

### SEO-Specific Commands
```bash
# SEO automation commands
claude /seo-analyze                   # SEO analysis commands
claude /seo-keyword-research          # Keyword research automation
claude /seo-rank-tracking             # Rank tracking setup
```

## Project Structure Overview

```
data-for-seo/
├── .claude/commands/     # Pre-configured Claude commands
├── .cursor/rules/        # Comprehensive coding standards and patterns
├── PRPs/                 # Product Requirement Prompts
│   ├── templates/        # PRP templates (start here)
│   ├── scripts/          # PRP execution scripts  
│   ├── ai_docs/          # Curated AI documentation
│   └── README.md         # PRP methodology (read this!)
├── src/                  # Source code
│   ├── agents/           # Multi-agent system (SEO analyst, content optimizer, etc.)
│   ├── communication/    # Redis pub/sub messaging
│   ├── knowledge/        # Vector database and RAG
│   ├── workflows/        # Process orchestration
│   └── tools/seo/        # SEO-specific tools and utilities
├── tests/                # Test suite
├── docker-compose.dev.yml # Development services
├── claude_md_files/      # Framework-specific examples
└── CLAUDE.md             # Project instructions
```

## SEO Capabilities

### Data for SEO APIs
- **Keyword Research**: Comprehensive keyword analysis and suggestions
- **Rank Tracking**: Monitor search engine rankings
- **Site Audit**: Technical SEO analysis and recommendations
- **Competitor Analysis**: Competitive intelligence and insights
- **Local SEO**: Location-based optimization tools

### Automation Features
- **Keyword Monitoring**: Automated keyword performance tracking
- **Content Optimization**: AI-driven content improvement suggestions
- **Technical SEO**: Automated technical issue detection and resolution
- **Reporting**: Comprehensive SEO performance reports
- **Alerting**: Proactive notification of SEO issues and opportunities

## Multi-Agent System

> **📖 Core Agent Details**: See [Agent Factory Shared Components - Agent Descriptions](../agent-factory/docs/SHARED_COMPONENTS.md#agent-descriptions) for base agent roles.

### SEO-Specific Agents
- **SEO Analyst**: Keyword research and analysis
- **Content Optimizer**: Content improvement and optimization
- **Technical Auditor**: Technical SEO analysis and fixes
- **Performance Monitor**: SEO performance tracking and reporting
- **Automation Engineer**: Workflow automation and integration

## Knowledge Management

- **Vector Database**: Chroma for storing and retrieving knowledge
- **RAG System**: Retrieval-augmented generation for context-aware decisions
- **Redis Message Bus**: Inter-agent communication and coordination
- **SEO Patterns**: Comprehensive SEO best practices and automation patterns

## Next Steps

1. **Read the methodology**: `cat PRPs/README.md`
2. **Study templates**: `cat PRPs/templates/prp_seo.md`
3. **Browse commands**: `ls .claude/commands/*/`
4. **Understand agents**: Explore `src/agents/` directory
5. **Read full onboarding**: `cat docs/ONBOARDING.md`

## Key Concepts

> **📖 Core Concepts**: See [Agent Factory Shared Components - Core Concepts](../agent-factory/docs/SHARED_COMPONENTS.md#core-concepts) for detailed explanations of PRPs, workflows, and architecture.

### SEO-Specific Concepts
- **SEO Focus**: Domain-specific patterns and workflows for SEO automation
- **Data for SEO Integration**: Comprehensive API integration for SEO data and analysis

## Getting Help

- **Commands**: Browse `.claude/commands/` directory
- **Templates**: Check `PRPs/templates/` for examples  
- **Methodology**: Read `PRPs/README.md`
- **Coding Standards**: Check `.cursor/rules/` for guidelines
- **Agent Patterns**: Study `src/agents/` for multi-agent system
- **Full guide**: See `docs/ONBOARDING.md`

You're ready to start automating SEO with the Agent Factory framework! Begin with a simple feature and work your way up to more complex SEO automation implementations.
