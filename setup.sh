#!/bin/bash

# Data for SEO - Simple Setup Script

echo "🚀 Setting up Data for SEO project..."

# Create basic project structure
mkdir -p .claude/commands/{prp-commands,seo-specific}
mkdir -p .cursor/rules
mkdir -p PRPs/{templates,scripts,ai_docs}
mkdir -p src/{agent_factory,agents/{base,seo_analyst,content_optimizer,technical_auditor,performance_monitor,automation_engineer,coordinator},api/{rest,streaming,ui},communication/{message_bus,protocols,coordination},knowledge/{memory,rag,vector_store},workflows/{monitoring,prp_engine,validation},tools/{deployment,git,testing,seo},config}
mkdir -p tests
mkdir -p docker
mkdir -p claude_md_files
mkdir -p archon-projects/seo-automation/{tasks/{seo-analysis,data-integration,automation},knowledge/{agent-factory,seo-patterns,integration},features/{seo-api,data-processing,reporting},workflows}

# Create __init__.py files
find src -type d -exec touch {}/__init__.py \;
touch tests/__init__.py

echo "✅ Project structure created successfully!"
echo ""
echo "📁 Project Structure:"
echo "  - docs/ - Comprehensive documentation"
echo "  - src/ - Source code with multi-agent system"
echo "  - PRPs/ - Product Requirement Prompts"
echo "  - archon-projects/ - Archon project containers"
echo "  - scripts/ - Automation and setup scripts"
echo "  - tests/ - Test suite"
echo "  - docker/ - Docker configuration"
echo ""
echo "🚀 Next steps:"
echo "  1. Review the documentation in docs/"
echo "  2. Customize configuration files"
echo "  3. Start building your SEO automation features!"
