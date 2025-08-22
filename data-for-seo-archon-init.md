name: "Data for SEO Archon Project Initialization"
description: "Initialize an Archon MCP project for data-for-seo integration within the Agent Factory framework"

---

## Goal

**Feature Goal**: Initialize and configure an Archon MCP project specifically for data-for-seo operations, enabling the Agent Factory to leverage Archon's advanced AI workflows for SEO data analysis and automation.

**Deliverable**: A fully configured Archon project container with data-for-seo specific features, task management, and knowledge base integration, incorporating comprehensive Agent Factory project knowledge.

**Success Definition**: The Archon project is successfully initialized, configured with data-for-seo context, populated with Agent Factory knowledge, and ready to manage SEO-related development tasks with proper task tracking and knowledge management.

## User Persona (if applicable)

**Target User**: DevOps engineers and AI workflow specialists setting up data-for-seo automation within the Agent Factory framework

**Use Case**: Initial setup of Archon project for managing SEO data analysis workflows and development tasks, with full integration into the existing Agent Factory knowledge ecosystem

**User Journey**: 
1. Initialize Archon project with data-for-seo context
2. Integrate comprehensive Agent Factory project knowledge
3. Configure project features and task management for SEO automation
4. Set up knowledge base for SEO-related documentation and Agent Factory patterns
5. Begin task creation and management for SEO automation features

**Pain Points Addressed**: 
- Manual setup of Archon projects for specific domains
- Lack of structured task management for SEO automation
- Missing context for SEO-related development workflows
- Integration challenges with existing Agent Factory knowledge systems

## Why

- **Business Value**: Enables systematic development of SEO automation features through structured task management within the Agent Factory ecosystem
- **Integration Benefits**: Leverages Archon's advanced AI workflows for complex SEO data analysis tasks while maintaining consistency with existing Agent Factory patterns
- **Problem Solving**: Provides organized task tracking and knowledge management for SEO development teams, with full access to existing framework knowledge
- **Scalability**: Creates foundation for managing multiple SEO-related features and improvements, building on proven Agent Factory architecture
- **Knowledge Continuity**: Ensures SEO automation development follows established patterns and leverages existing expertise

## What

[User-visible behavior and technical requirements]

### Success Criteria

- [ ] Archon project successfully created with data-for-seo context
- [ ] Project features configured for SEO automation workflows
- [ ] Initial tasks created for SEO integration development
- [ ] Knowledge base populated with relevant SEO documentation AND Agent Factory project knowledge
- [ ] Project ready for task management and development coordination
- [ ] Full integration with existing Agent Factory knowledge ecosystem
- [ ] SEO-specific patterns and workflows established
- [ ] Development team can leverage both SEO expertise and Agent Factory patterns

## All Needed Context

### Context Completeness Check

_Before writing this PRP, validate: "If someone knew nothing about this codebase, would they have everything needed to implement this successfully?"_

### Documentation & References

```yaml
# MUST READ - Include these in your context window
- url: https://modelcontextprotocol.io/introduction
  why: Understanding MCP protocol for Archon server integration
  critical: MCP is the foundation for Archon server communication

- url: https://dataforseo.com/apis
  why: Data for SEO API documentation for integration requirements
  critical: Understanding the target API for SEO data operations

- file: PRPs/ai_docs/cc_mcp.md
  why: MCP configuration patterns for Claude Code integration
  pattern: MCP server setup and configuration
  gotcha: MCP tools must be explicitly allowed using --allowedTools

- file: src/config/settings.py
  why: Configuration patterns for external service integration
  pattern: Settings class structure and environment variable handling
  gotcha: Use Field validation and proper type hints

- file: src/models.py
  why: Core data structures for task and project management
  pattern: Pydantic model structure and validation
  gotcha: All models must inherit from BaseModel and use proper type hints

- file: PRPs/templates/prp_base.md
  why: PRP structure and implementation patterns
  pattern: Complete PRP template with all required sections
  gotcha: Must pass "No Prior Knowledge" test for implementation success

# AGENT FACTORY PROJECT KNOWLEDGE - CRITICAL FOR INTEGRATION
- file: ONBOARDING.md
  why: Comprehensive project overview, architecture, and development patterns
  pattern: Multi-agent system architecture and workflow patterns
  critical: Understanding the existing framework before extending it

- file: QUICKSTART.md
  why: Essential setup and workflow patterns
  pattern: Quick start commands and project structure
  critical: Fast onboarding for new team members

- file: .cursor/rules/project-overview.mdc
  why: High-level project architecture and entry points
  pattern: Project structure and component organization
  critical: Understanding where to integrate new features

- file: .cursor/rules/python-coding-standards.mdc
  why: Python coding standards and conventions
  pattern: Code style, type hints, and validation patterns
  critical: Maintaining consistency with existing codebase

- file: .cursor/rules/agent-development-patterns.mdc
  why: Agent development patterns and best practices
  pattern: Agent interface, message handling, and task execution
  critical: Following established agent patterns

- file: .cursor/rules/architecture-patterns.mdc
  why: Architecture patterns and system design
  pattern: Design patterns, data flow, and integration points
  critical: Architectural consistency and scalability

- file: .cursor/rules/testing-quality-standards.mdc
  why: Testing and quality assurance standards
  pattern: Test structure, mocking, and validation approaches
  critical: Maintaining code quality and reliability
```

### Current Codebase tree (run `tree` in the root of the project) to get an overview of the codebase

```bash
agent-factory/
├── .claude/                    # Claude Code configuration
│   ├── commands/              # 35+ pre-configured commands
│   │   ├── prp-commands/      # PRP creation and execution workflows
│   │   ├── development/       # Core development utilities
│   │   ├── code-quality/      # Review and refactoring commands
│   │   ├── rapid-development/ # Parallel PRP creation tools
│   │   ├── git-operations/    # Git workflows
│   │   └── typescript/        # TypeScript-specific commands
├── .cursor/                    # Cursor IDE rules and configuration
│   └── rules/                 # Comprehensive coding standards and patterns
├── PRPs/                      # Product Requirement Prompts
│   ├── templates/             # PRP templates
│   ├── scripts/               # Execution scripts
│   ├── ai_docs/              # AI documentation
│   └── *.md                  # Active PRPs
├── src/                       # Source code
│   ├── agent_factory/         # Main package with core framework
│   ├── agents/               # Specialized agents (coder, planner, tester, etc.)
│   ├── api/                  # REST and streaming interfaces
│   ├── communication/        # Redis pub/sub messaging system
│   ├── knowledge/            # Vector store and RAG implementation
│   ├── workflows/            # Process orchestration and monitoring
│   └── config/               # Settings and configuration
├── docker-compose.yml         # Production services
├── docker-compose.dev.yml     # Development overrides
├── scripts/dev-start.sh       # Development startup
└── pyproject.toml            # Python project configuration
```

### Desired Codebase tree with files to be added and responsibility of file

```bash
agent-factory/
├── .claude/commands/          # Existing Claude commands
├── .cursor/rules/             # Existing Cursor rules
├── PRPs/                      # Existing PRP structure
├── src/                       # Existing source code
├── archon-projects/           # NEW: Archon project containers
│   └── data-for-seo/         # NEW: Data for SEO project
│       ├── project.json       # NEW: Project configuration and metadata
│       ├── tasks/             # NEW: Task definitions and workflows
│       │   ├── seo-analysis/  # NEW: SEO analysis task templates
│       │   ├── data-integration/ # NEW: Data integration workflows
│       │   └── automation/    # NEW: Automation task patterns
│       ├── knowledge/         # NEW: Project-specific knowledge
│       │   ├── agent-factory/ # NEW: Agent Factory framework knowledge
│       │   ├── seo-patterns/  # NEW: SEO-specific patterns and best practices
│       │   └── integration/   # NEW: Integration patterns and examples
│       ├── features/          # NEW: Feature specifications
│       │   ├── seo-api/       # NEW: SEO API integration features
│       │   ├── data-processing/ # NEW: Data processing features
│       │   └── reporting/     # NEW: Reporting and analytics features
│       └── workflows/         # NEW: SEO-specific workflow definitions
├── config/                    # NEW: Archon project configs
│   └── archon-projects.yml   # NEW: Project registry and configuration
└── scripts/                   # Existing scripts
    └── archon-init.sh         # NEW: Project initialization script
```

### Known Gotchas of our codebase & Library Quirks

```python
# CRITICAL: Archon MCP server requires specific configuration
# Example: Must use HTTP transport for localhost:8051
# Example: MCP tools must be explicitly allowed with --allowedTools

# CRITICAL: Data for SEO API requires authentication
# Example: API credentials must be stored securely in environment variables
# Example: Rate limiting and quota management required

# CRITICAL: Project initialization must follow existing patterns
# Example: Use existing settings.py patterns for configuration
# Example: Follow existing model.py patterns for data structures

# CRITICAL: Task management must integrate with existing workflow
# Example: Tasks must use ExecutionResult pattern for consistency
# Example: Error handling must follow existing patterns

# CRITICAL: Agent Factory integration requirements
# Example: Must follow existing agent patterns and interfaces
# Example: Must integrate with existing knowledge management system
# Example: Must use existing communication patterns (Redis pub/sub)
# Example: Must follow existing validation and testing patterns

# CRITICAL: Knowledge base integration
# Example: Must populate Chroma vector database with relevant knowledge
# Example: Must follow existing RAG patterns and workflows
# Example: Must integrate with existing agent memory systems
```

## Implementation Blueprint

### Data models and structure

Create the core data models, we ensure type safety and consistency.

```python
Examples:
 - orm models
 - pydantic models
 - pydantic schemas
 - pydantic validators
```

### Implementation Tasks (ordered by dependencies)

```yaml
Task 1: CREATE src/models/archon_project.py
  - IMPLEMENT: ArchonProject, ArchonTask, ArchonFeature, ArchonKnowledge Pydantic models
  - FOLLOW pattern: src/models.py (field validation approach, ExecutionResult pattern)
  - NAMING: PascalCase for classes, snake_case for fields
  - PLACEMENT: Domain-specific model file in src/models/
  - INTEGRATION: Include AgentFactory knowledge integration fields

Task 2: CREATE src/config/archon_settings.py
  - IMPLEMENT: ArchonSettings class with project configuration
  - FOLLOW pattern: src/config/settings.py (settings structure, validation, environment variables)
  - NAMING: ArchonSettings class, environment variable handling
  - DEPENDENCIES: Import models from Task 1
  - PLACEMENT: Configuration layer in src/config/
  - INTEGRATION: Include Agent Factory service configuration

Task 3: CREATE src/services/archon_project_service.py
  - IMPLEMENT: ArchonProjectService class with async methods
  - FOLLOW pattern: src/services/database_service.py (service structure, error handling)
  - NAMING: ArchonProjectService class, async def create_*, get_*, update_* methods
  - DEPENDENCIES: Import models from Task 1 and settings from Task 2
  - PLACEMENT: Service layer in src/services/
  - INTEGRATION: Include Agent Factory knowledge management integration

Task 4: CREATE src/tools/archon_project_init.py
  - IMPLEMENT: MCP tool wrapper for project initialization
  - FOLLOW pattern: src/tools/existing_tool.py (FastMCP tool structure)
  - NAMING: snake_case file name, descriptive tool function name
  - DEPENDENCIES: Import service from Task 3
  - PLACEMENT: Tool layer in src/tools/
  - INTEGRATION: Include Agent Factory knowledge population

Task 5: CREATE scripts/archon-init.sh
  - IMPLEMENT: Shell script for project initialization
  - FOLLOW pattern: scripts/dev-start.sh (script structure, error handling)
  - NAMING: Descriptive script name with .sh extension
  - DEPENDENCIES: Import and use tools from Task 4
  - PLACEMENT: Scripts directory for easy execution
  - INTEGRATION: Include Agent Factory service startup

Task 6: CREATE config/archon-projects.yml
  - IMPLEMENT: YAML configuration for project registry
  - FOLLOW pattern: docker-compose.yml (YAML structure, configuration)
  - NAMING: Descriptive config file with .yml extension
  - DEPENDENCIES: Reference models and settings from Tasks 1-2
  - PLACEMENT: Config directory for centralized configuration
  - INTEGRATION: Include Agent Factory project templates

Task 7: CREATE archon-projects/data-for-seo/project.json
  - IMPLEMENT: Project configuration with comprehensive metadata
  - FOLLOW pattern: Standard JSON configuration format
  - NAMING: Descriptive project configuration
  - DEPENDENCIES: Reference models and settings from Tasks 1-2
  - PLACEMENT: Project-specific configuration
  - INTEGRATION: Include Agent Factory knowledge references

Task 8: CREATE archon-projects/data-for-seo/knowledge/agent-factory/
  - IMPLEMENT: Agent Factory knowledge integration files
  - FOLLOW pattern: Existing documentation structure
  - NAMING: Descriptive knowledge files with .md extension
  - DEPENDENCIES: Extract knowledge from existing documentation
  - PLACEMENT: Project knowledge directory
  - INTEGRATION: Include comprehensive framework knowledge

Task 9: CREATE src/services/tests/test_archon_project_service.py
  - IMPLEMENT: Unit tests for all service methods (happy path, edge cases, error handling)
  - FOLLOW pattern: src/services/tests/test_existing_service.py (fixture usage, assertion patterns)
  - NAMING: test_{method}_{scenario} function naming
  - COVERAGE: All public methods with positive and negative test cases
  - PLACEMENT: Tests alongside the code they test
  - INTEGRATION: Test Agent Factory integration points

Task 10: CREATE src/tools/tests/test_archon_project_init.py
  - IMPLEMENT: Unit tests for MCP tool functionality
  - FOLLOW pattern: src/tools/tests/test_existing_tool.py (MCP tool testing approach)
  - MOCK: External service dependencies
  - COVERAGE: Tool input validation, success responses, error handling
  - PLACEMENT: Tool tests in src/tools/tests/
  - INTEGRATION: Test knowledge population and integration
```

### Implementation Patterns & Key Details

```python
# Show critical patterns and gotchas - keep concise, focus on non-obvious details

# Example: Archon project model pattern with Agent Factory integration
class ArchonProject(BaseModel):
    id: str = Field(..., description="Unique project identifier")
    name: str = Field(..., description="Project display name")
    description: str = Field(..., description="Project description")
    features: List[ArchonFeature] = Field(default_factory=list)
    tasks: List[ArchonTask] = Field(default_factory=list)
    agent_factory_integration: AgentFactoryIntegration = Field(default_factory=AgentFactoryIntegration)
    
    # PATTERN: Use Field validation and descriptions (follow src/models.py)
    # GOTCHA: All fields must have proper type hints and validation
    # CRITICAL: Use default_factory for mutable defaults
    # INTEGRATION: Include Agent Factory specific fields

# Example: Agent Factory integration model
class AgentFactoryIntegration(BaseModel):
    knowledge_base: List[str] = Field(default_factory=list, description="Agent Factory knowledge references")
    agent_patterns: List[str] = Field(default_factory=list, description="Relevant agent patterns")
    workflow_templates: List[str] = Field(default_factory=list, description="Workflow templates")
    validation_gates: List[str] = Field(default_factory=list, description="Validation patterns")
    
    # PATTERN: Follow existing model patterns for consistency
    # CRITICAL: Reference existing Agent Factory knowledge and patterns

# Example: Archon settings pattern with Agent Factory integration
class ArchonSettings(BaseSettings):
    server_url: str = Field(default="http://localhost:8051", description="Archon server URL")
    api_key: Optional[str] = Field(default=None, description="Archon API key if required")
    project_directory: str = Field(default="./archon-projects", description="Projects storage directory")
    agent_factory_services: AgentFactoryServices = Field(default_factory=AgentFactoryServices)
    
    # PATTERN: Settings inheritance from BaseSettings (follow src/config/settings.py)
    # GOTCHA: Sensitive fields should be Optional and loaded from environment
    # CRITICAL: Use descriptive Field descriptions for configuration clarity
    # INTEGRATION: Include Agent Factory service configuration

# Example: Project service pattern with knowledge integration
class ArchonProjectService:
    async def create_project(self, project_data: ArchonProjectCreate) -> ExecutionResult:
        # PATTERN: Return ExecutionResult for consistency (follow existing service pattern)
        # GOTCHA: Handle async operations properly with try/catch
        # CRITICAL: Validate input data before processing
        # INTEGRATION: Populate Agent Factory knowledge during creation
        
        try:
            project = ArchonProject(**project_data.dict())
            
            # INTEGRATION: Populate with Agent Factory knowledge
            await self._populate_agent_factory_knowledge(project)
            
            # Implementation logic here
            return ExecutionResult.success("Project created successfully", data=project)
        except Exception as e:
            return ExecutionResult.failure(f"Project creation failed: {str(e)}")
    
    async def _populate_agent_factory_knowledge(self, project: ArchonProject):
        # PATTERN: Follow existing knowledge management patterns
        # CRITICAL: Integrate with existing Chroma vector store
        # INTEGRATION: Populate project with relevant framework knowledge

# Example: MCP tool pattern with knowledge integration
@app.tool()
async def initialize_archon_project(project_name: str, description: str) -> str:
    # PATTERN: Tool validation and service delegation (see src/tools/existing_tool.py)
    # RETURN: JSON string with standardized response format
    # CRITICAL: Validate inputs and handle errors gracefully
    # INTEGRATION: Include Agent Factory knowledge population
    
    # Validate inputs
    if not project_name or not description:
        return json.dumps({"success": False, "error": "Project name and description required"})
    
    # Create project with knowledge integration
    result = await project_service.create_project_with_knowledge(project_name, description)
    return json.dumps(result.dict())
```

### Integration Points

```yaml
CONFIGURATION:
  - add to: src/config/settings.py
  - pattern: "archon: ArchonSettings = Field(default_factory=ArchonSettings)"

ENVIRONMENT:
  - add to: .env.example
  - pattern: "ARCHON_SERVER_URL=http://localhost:8051"
  - pattern: "ARCHON_API_KEY=your-api-key-here"
  - pattern: "ARCHON_PROJECT_DIR=./archon-projects"
  - pattern: "AGENT_FACTORY_KNOWLEDGE_INTEGRATION=true"

DOCKER:
  - add to: docker-compose.dev.yml
  - pattern: "archon-server: image: archon/server:latest"

SCRIPTS:
  - add to: scripts/dev-start.sh
  - pattern: "echo 'Starting Archon server...'"

KNOWLEDGE INTEGRATION:
  - add to: src/knowledge/vector_store/
  - pattern: "Integrate with existing Chroma vector store"
  - pattern: "Follow existing RAG patterns and workflows"

AGENT INTEGRATION:
  - add to: src/agents/
  - pattern: "Follow existing agent interface patterns"
  - pattern: "Integrate with existing message bus (Redis)"
```

## Validation Loop

### Level 1: Syntax & Style (Immediate Feedback)

```bash
# Run after each file creation - fix before proceeding
ruff check src/{new_files} --fix     # Auto-format and fix linting issues
mypy src/{new_files}                 # Type checking with specific files
ruff format src/{new_files}          # Ensure consistent formatting

# Project-wide validation
ruff check src/ --fix
mypy src/
ruff format src/

# Expected: Zero errors. If errors exist, READ output and fix before proceeding.
```

### Level 2: Unit Tests (Component Validation)

```bash
# Test each component as it's created
uv run pytest src/services/tests/test_archon_project_service.py -v
uv run pytest src/tools/tests/test_archon_project_init.py -v

# Full test suite for affected areas
uv run pytest src/services/tests/ -v
uv run pytest src/tools/tests/ -v

# Coverage validation (if coverage tools available)
uv run pytest src/ --cov=src --cov-report=term-missing

# Expected: All tests pass. If failing, debug root cause and fix implementation.
```

### Level 3: Integration Testing (System Validation)

```bash
# Service startup validation
uv run python main.py &
sleep 3  # Allow startup time

# Health check validation
curl -f http://localhost:8000/health || echo "Service health check failed"

# Archon project initialization testing
uv run python -c "
from src.tools.archon_project_init import initialize_archon_project
import asyncio
result = asyncio.run(initialize_archon_project('data-for-seo', 'SEO automation project'))
print(result)
"

# MCP server validation (if MCP-based)
# Test MCP tool functionality
echo '{"method": "tools/call", "params": {"name": "initialize_archon_project", "arguments": {"project_name": "test", "description": "test"}}}' | \
  uv run python -m src.main

# Agent Factory integration validation
uv run python -c "
from src.services.archon_project_service import ArchonProjectService
import asyncio

async def test_integration():
    service = ArchonProjectService()
    # Test knowledge integration
    knowledge = await service.get_agent_factory_knowledge()
    print(f'Knowledge integration: {knowledge}')

asyncio.run(test_integration())
"

# Expected: All integrations working, proper responses, no connection errors
```

### Level 4: Creative & Domain-Specific Validation

```bash
# Archon Project Validation Examples:

# Project Creation Validation with Knowledge Integration
python -c "
from src.services.archon_project_service import ArchonProjectService
from src.models.archon_project import ArchonProjectCreate
import asyncio

async def test_project_creation_with_knowledge():
    service = ArchonProjectService()
    project_data = ArchonProjectCreate(
        name='data-for-seo',
        description='SEO automation project'
    )
    result = await service.create_project(project_data)
    print(f'Project creation result: {result}')
    
    # Validate knowledge integration
    if result.success:
        project = result.data
        print(f'Agent Factory knowledge: {project.agent_factory_integration}')

asyncio.run(test_project_creation_with_knowledge())
"

# Configuration Validation
python -c "
from src.config.archon_settings import ArchonSettings
settings = ArchonSettings()
print(f'Archon settings: {settings.dict()}')
print(f'Agent Factory integration: {settings.agent_factory_services}')
"

# Knowledge Base Validation
python -c "
from src.knowledge.vector_store import ChromaVectorStore
store = ChromaVectorStore()
# Test knowledge retrieval
results = store.query_similar('Agent Factory patterns', limit=5)
print(f'Knowledge base results: {len(results)} items found')
"

# File Structure Validation
ls -la archon-projects/data-for-seo/ || echo "Project directory not created"
ls -la archon-projects/data-for-seo/knowledge/agent-factory/ || echo "Knowledge directory not created"
ls -la config/archon-projects.yml || echo "Config file not created"

# Agent Factory Pattern Validation
python -c "
from src.agents.base.agent_interface import BaseAgent
from src.models import ExecutionResult
# Test that new models follow existing patterns
print('Pattern validation: Models follow existing BaseAgent and ExecutionResult patterns')
"

# Expected: All creative validations pass, project structure created correctly, knowledge integration working
```

## Final Validation Checklist

### Technical Validation

- [ ] All 4 validation levels completed successfully
- [ ] All tests pass: `uv run pytest src/ -v`
- [ ] No linting errors: `uv run ruff check src/`
- [ ] No type errors: `uv run mypy src/`
- [ ] No formatting issues: `uv run ruff format src/ --check`

### Feature Validation

- [ ] All success criteria from "What" section met
- [ ] Manual testing successful: [specific commands from Level 3]
- [ ] Error cases handled gracefully with proper error messages
- [ ] Integration points work as specified
- [ ] User persona requirements satisfied (if applicable)
- [ ] Agent Factory knowledge integration working
- [ ] SEO-specific patterns established

### Code Quality Validation

- [ ] Follows existing codebase patterns and naming conventions
- [ ] File placement matches desired codebase tree structure
- [ ] Anti-patterns avoided (check against Anti-Patterns section)
- [ ] Dependencies properly managed and imported
- [ ] Configuration changes properly integrated
- [ ] Agent Factory integration patterns followed
- [ ] Knowledge management patterns consistent

### Documentation & Deployment

- [ ] Code is self-documenting with clear variable/function names
- [ ] Logs are informative but not verbose
- [ ] Environment variables documented if new ones added
- [ ] Agent Factory knowledge properly documented
- [ ] SEO-specific patterns documented

---

## Anti-Patterns to Avoid

- ❌ Don't create new patterns when existing ones work
- ❌ Don't skip validation because "it should work"
- ❌ Don't ignore failing tests - fix them
- ❌ Don't use sync functions in async context
- ❌ Don't hardcode values that should be config
- ❌ Don't catch all exceptions - be specific
- ❌ Don't skip MCP tool validation
- ❌ Don't ignore environment variable security
- ❌ Don't ignore Agent Factory integration patterns
- ❌ Don't create isolated knowledge systems - integrate with existing
- ❌ Don't skip knowledge population during project creation
