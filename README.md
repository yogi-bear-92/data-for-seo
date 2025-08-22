# Data for SEO - Agent Factory Integration

A comprehensive SEO automation project built on the Agent Factory framework, leveraging Archon MCP for advanced AI workflows and data analysis.

## Overview

This project integrates Data for SEO APIs with the Agent Factory multi-agent system, enabling autonomous development of SEO automation features through structured PRP workflows and comprehensive knowledge management.

## Core Concept

**SEO Automation + Agent Factory + Archon MCP** - designed to enable AI agents to develop and deploy SEO automation features with production-ready code on the first pass.

## Features

- **SEO API Integration**: Comprehensive Data for SEO API integration
- **Multi-Agent Development**: Specialized agents for SEO analysis, data processing, and automation
- **Knowledge Management**: Vector database with RAG for SEO context-aware decisions
- **PRP-Driven Workflows**: Structured task execution with validation gates
- **Agent Coordination**: Redis pub/sub messaging for seamless communication
- **Self-Learning System**: Continuous improvement from development outcomes

## Quick Start

> **📖 Complete Setup Guide**: See [docs/QUICKSTART.md](docs/QUICKSTART.md) for detailed 5-minute setup guide.

**Essential Steps:**
1. Navigate to directory: `cd data-for-seo`
2. Initialize context: `claude /prime-core`
3. Create SEO PRP: `claude /prp-base-create "implement SEO keyword analysis"`
4. Execute with agents: `uv run PRPs/scripts/prp_runner.py --prp seo-keyword-analysis --interactive`

## Architecture

- **Agent Framework**: LangChain + LangGraph for stateful workflows
- **Vector Database**: Chroma for knowledge storage and retrieval
- **Communication**: Redis pub/sub for agent coordination
- **API Layer**: FastAPI for external interfaces
- **SEO Integration**: Data for SEO APIs for comprehensive SEO data

## Project Structure

```
data-for-seo/
├── docs/                    # Project documentation
├── src/                     # Source code
├── PRPs/                    # Product Requirement Prompts
├── archon-projects/         # Archon project containers
├── scripts/                 # Automation scripts
└── tests/                   # Test suite
```

## Getting Started

1. **Read the documentation**: Start with `docs/ONBOARDING.md`
2. **Set up environment**: Configure API keys and services
3. **Initialize project**: Run `scripts/init-project.sh`
4. **Create first PRP**: Define your SEO automation feature
5. **Execute with agents**: Let the multi-agent system build your feature

## License

MIT License - see LICENSE file for details.

---

**Ready to automate SEO?** Start with a simple feature and let the AI agents build your SEO automation empire!
