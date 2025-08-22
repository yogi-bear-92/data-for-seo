"""SEO Audit Workflow for comprehensive website SEO analysis."""

import asyncio
from typing import Any, Dict, List, Optional

from ..agents.base import SEOTaskMixin
from ..models.base import ExecutionResult, SEOTask
from .workflow_engine import WorkflowEngine


class SEOAuditWorkflow(WorkflowEngine, SEOTaskMixin):
    """Complete website SEO audit workflow orchestrating multiple agents."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the SEO audit workflow."""
        super().__init__(
            name="SEO Audit Workflow",
            description="Comprehensive SEO analysis covering technical, content, and performance aspects",
            config=config,
        )
        
        # Workflow configuration
        self.parallel_execution = self.config.get("parallel_execution", True)
        self.include_competitor_analysis = self.config.get("include_competitor_analysis", True)
        self.depth_level = self.config.get("depth_level", "standard")  # basic, standard, deep
        
    async def validate_parameters(self, parameters: Dict[str, Any]) -> ExecutionResult:
        """Validate SEO audit parameters."""
        required_params = ["url"]
        optional_params = ["keywords", "competitors", "pages_to_audit", "mobile_audit"]
        
        # Check required parameters
        missing_params = []
        for param in required_params:
            if param not in parameters:
                missing_params.append(param)
        
        if missing_params:
            return ExecutionResult.failure_result(
                message="Missing required parameters",
                errors=[f"Missing parameters: {', '.join(missing_params)}"]
            )
        
        # Validate URL format
        url = parameters.get("url")
        if not self.validate_url(url):
            return ExecutionResult.failure_result(
                message="Invalid URL format",
                errors=[f"URL '{url}' is not a valid URL"]
            )
        
        # Validate keywords if provided
        keywords = parameters.get("keywords", [])
        if keywords:
            invalid_keywords = [kw for kw in keywords if not self.validate_keyword(kw)]
            if invalid_keywords:
                return ExecutionResult.failure_result(
                    message="Invalid keywords found",
                    errors=[f"Invalid keywords: {', '.join(invalid_keywords)}"]
                )
        
        # Validate pages_to_audit if provided
        pages_to_audit = parameters.get("pages_to_audit", 10)
        if not isinstance(pages_to_audit, int) or pages_to_audit < 1 or pages_to_audit > 1000:
            return ExecutionResult.failure_result(
                message="Invalid pages_to_audit value",
                errors=["pages_to_audit must be an integer between 1 and 1000"]
            )
        
        return ExecutionResult.success_result("Parameters validated successfully")
    
    async def get_workflow_steps(self, parameters: Dict[str, Any]) -> List[str]:
        """Get the workflow steps based on configuration and parameters."""
        steps = [
            "technical_analysis",
            "content_analysis", 
            "performance_analysis",
            "mobile_analysis",
            "structure_analysis",
        ]
        
        # Add optional steps based on configuration
        if self.include_competitor_analysis and parameters.get("competitors"):
            steps.append("competitor_analysis")
        
        if parameters.get("keywords"):
            steps.append("keyword_analysis")
        
        if self.depth_level == "deep":
            steps.extend([
                "link_analysis",
                "schema_analysis",
                "accessibility_analysis",
            ])
        
        steps.append("result_aggregation")
        
        return steps
    
    async def execute_workflow(
        self, 
        parameters: Dict[str, Any], 
        steps: List[str]
    ) -> ExecutionResult:
        """Execute the SEO audit workflow."""
        results = {}
        
        try:
            url = parameters["url"]
            keywords = parameters.get("keywords", [])
            competitors = parameters.get("competitors", [])
            pages_to_audit = parameters.get("pages_to_audit", 10)
            mobile_audit = parameters.get("mobile_audit", True)
            
            # Execute workflow steps
            if self.parallel_execution:
                results = await self._execute_parallel_audit(
                    url, keywords, competitors, pages_to_audit, mobile_audit, steps
                )
            else:
                results = await self._execute_sequential_audit(
                    url, keywords, competitors, pages_to_audit, mobile_audit, steps
                )
            
            # Aggregate and return final results
            return await self._aggregate_audit_results(results)
            
        except Exception as e:
            return ExecutionResult.failure_result(
                message=f"SEO audit execution failed: {str(e)}",
                errors=[str(e)]
            )
    
    async def _execute_parallel_audit(
        self,
        url: str,
        keywords: List[str],
        competitors: List[str],
        pages_to_audit: int,
        mobile_audit: bool,
        steps: List[str],
    ) -> Dict[str, Any]:
        """Execute audit steps in parallel for better performance."""
        tasks = []
        results = {}
        
        # Create parallel tasks for independent analyses
        if "technical_analysis" in steps:
            tasks.append(self._run_technical_analysis(url, pages_to_audit))
        
        if "content_analysis" in steps:
            tasks.append(self._run_content_analysis(url, keywords))
        
        if "performance_analysis" in steps:
            tasks.append(self._run_performance_analysis(url))
        
        if "mobile_analysis" in steps and mobile_audit:
            tasks.append(self._run_mobile_analysis(url))
        
        if "structure_analysis" in steps:
            tasks.append(self._run_structure_analysis(url))
        
        # Execute parallel tasks
        parallel_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process parallel results
        step_names = []
        if "technical_analysis" in steps:
            step_names.append("technical_analysis")
        if "content_analysis" in steps:
            step_names.append("content_analysis")
        if "performance_analysis" in steps:
            step_names.append("performance_analysis")
        if "mobile_analysis" in steps and mobile_audit:
            step_names.append("mobile_analysis")
        if "structure_analysis" in steps:
            step_names.append("structure_analysis")
        
        for i, result in enumerate(parallel_results):
            if i < len(step_names):
                step_name = step_names[i]
                if isinstance(result, Exception):
                    self.logger.error(f"Parallel step {step_name} failed: {str(result)}")
                    results[step_name] = {"success": False, "error": str(result)}
                else:
                    results[step_name] = result
        
        # Execute remaining sequential steps
        if "competitor_analysis" in steps and competitors:
            results["competitor_analysis"] = await self._run_competitor_analysis(url, competitors)
        
        if "keyword_analysis" in steps and keywords:
            results["keyword_analysis"] = await self._run_keyword_analysis(url, keywords)
        
        if "link_analysis" in steps:
            results["link_analysis"] = await self._run_link_analysis(url)
        
        if "schema_analysis" in steps:
            results["schema_analysis"] = await self._run_schema_analysis(url)
        
        if "accessibility_analysis" in steps:
            results["accessibility_analysis"] = await self._run_accessibility_analysis(url)
        
        return results
    
    async def _execute_sequential_audit(
        self,
        url: str,
        keywords: List[str],
        competitors: List[str],
        pages_to_audit: int,
        mobile_audit: bool,
        steps: List[str],
    ) -> Dict[str, Any]:
        """Execute audit steps sequentially."""
        results = {}
        
        for step in steps:
            if step == "result_aggregation":
                continue
                
            step_result = await self.execute_step(
                step, 
                self._get_step_function(step),
                url, keywords, competitors, pages_to_audit, mobile_audit
            )
            
            if step_result.success and step_result.result:
                results[step] = step_result.result.data
            else:
                results[step] = {"success": False, "error": step_result.error_message}
        
        return results
    
    def _get_step_function(self, step: str):
        """Get the function for a specific workflow step."""
        step_functions = {
            "technical_analysis": self._run_technical_analysis,
            "content_analysis": self._run_content_analysis,
            "performance_analysis": self._run_performance_analysis,
            "mobile_analysis": self._run_mobile_analysis,
            "structure_analysis": self._run_structure_analysis,
            "competitor_analysis": self._run_competitor_analysis,
            "keyword_analysis": self._run_keyword_analysis,
            "link_analysis": self._run_link_analysis,
            "schema_analysis": self._run_schema_analysis,
            "accessibility_analysis": self._run_accessibility_analysis,
        }
        return step_functions.get(step)
    
    async def _run_technical_analysis(self, url: str, pages_to_audit: int = 10) -> Dict[str, Any]:
        """Run technical SEO analysis."""
        # This would integrate with actual SEO analysis agents
        return {
            "success": True,
            "url": url,
            "pages_analyzed": pages_to_audit,
            "technical_issues": [],
            "page_speed": {"score": 85, "recommendations": []},
            "https_status": True,
            "mobile_friendly": True,
            "crawlability": {"status": "good", "issues": []},
            "sitemap_status": True,
            "robots_txt_status": True,
        }
    
    async def _run_content_analysis(self, url: str, keywords: List[str]) -> Dict[str, Any]:
        """Run content SEO analysis."""
        return {
            "success": True,
            "url": url,
            "keywords_analyzed": len(keywords),
            "title_tags": {"optimized": True, "issues": []},
            "meta_descriptions": {"optimized": True, "issues": []},
            "header_structure": {"h1_count": 1, "h2_count": 3, "issues": []},
            "keyword_density": {"target_keywords": keywords, "density_scores": {}},
            "content_quality": {"score": 88, "word_count": 1500, "readability": "good"},
            "duplicate_content": {"issues": []},
        }
    
    async def _run_performance_analysis(self, url: str) -> Dict[str, Any]:
        """Run performance analysis."""
        return {
            "success": True,
            "url": url,
            "core_web_vitals": {
                "lcp": {"score": 2.1, "status": "good"},
                "fid": {"score": 95, "status": "good"},
                "cls": {"score": 0.08, "status": "good"},
            },
            "page_speed": {"desktop": 85, "mobile": 78},
            "optimization_opportunities": [],
        }
    
    async def _run_mobile_analysis(self, url: str) -> Dict[str, Any]:
        """Run mobile SEO analysis."""
        return {
            "success": True,
            "url": url,
            "mobile_friendly": True,
            "responsive_design": True,
            "mobile_speed": 78,
            "mobile_usability": {"issues": []},
            "amp_status": False,
        }
    
    async def _run_structure_analysis(self, url: str) -> Dict[str, Any]:
        """Run site structure analysis."""
        return {
            "success": True,
            "url": url,
            "url_structure": {"optimized": True, "issues": []},
            "internal_linking": {"score": 82, "recommendations": []},
            "navigation": {"breadcrumbs": True, "menu_structure": "good"},
            "pagination": {"implemented": True, "issues": []},
        }
    
    async def _run_competitor_analysis(self, url: str, competitors: List[str]) -> Dict[str, Any]:
        """Run competitor analysis."""
        return {
            "success": True,
            "analyzed_competitors": len(competitors),
            "competitor_insights": {},
            "competitive_gaps": [],
            "opportunities": [],
        }
    
    async def _run_keyword_analysis(self, url: str, keywords: List[str]) -> Dict[str, Any]:
        """Run keyword analysis."""
        return {
            "success": True,
            "keywords_analyzed": len(keywords),
            "ranking_positions": {},
            "keyword_opportunities": [],
            "search_intent_analysis": {},
        }
    
    async def _run_link_analysis(self, url: str) -> Dict[str, Any]:
        """Run link analysis."""
        return {
            "success": True,
            "url": url,
            "internal_links": {"count": 45, "quality": "good"},
            "external_links": {"count": 12, "quality": "good"},
            "broken_links": {"count": 0, "links": []},
            "link_quality": {"score": 85},
        }
    
    async def _run_schema_analysis(self, url: str) -> Dict[str, Any]:
        """Run schema markup analysis."""
        return {
            "success": True,
            "url": url,
            "schema_types": ["Organization", "WebPage"],
            "implementation_quality": "good",
            "recommendations": [],
        }
    
    async def _run_accessibility_analysis(self, url: str) -> Dict[str, Any]:
        """Run accessibility analysis."""
        return {
            "success": True,
            "url": url,
            "accessibility_score": 88,
            "wcag_compliance": "AA",
            "issues": [],
            "recommendations": [],
        }
    
    async def _aggregate_audit_results(self, results: Dict[str, Any]) -> ExecutionResult:
        """Aggregate all audit results into a comprehensive report."""
        try:
            # Calculate overall SEO score
            scores = []
            if "performance_analysis" in results and results["performance_analysis"].get("success"):
                scores.append(results["performance_analysis"].get("page_speed", {}).get("desktop", 0))
            
            if "content_analysis" in results and results["content_analysis"].get("success"):
                scores.append(results["content_analysis"].get("content_quality", {}).get("score", 0))
            
            if "accessibility_analysis" in results and results["accessibility_analysis"].get("success"):
                scores.append(results["accessibility_analysis"].get("accessibility_score", 0))
            
            overall_score = sum(scores) / len(scores) if scores else 0
            
            # Generate recommendations
            recommendations = []
            priority_issues = []
            
            for step_name, step_result in results.items():
                if not step_result.get("success", True):
                    priority_issues.append(f"Failed analysis: {step_name}")
                    continue
                
                # Extract recommendations from each analysis
                if "recommendations" in step_result:
                    recommendations.extend(step_result["recommendations"])
                
                if "issues" in step_result and step_result["issues"]:
                    priority_issues.extend(step_result["issues"])
            
            # Generate executive summary
            summary = {
                "overall_seo_score": round(overall_score, 1),
                "analyses_completed": len([r for r in results.values() if r.get("success", True)]),
                "priority_issues": priority_issues[:10],  # Top 10 issues
                "top_recommendations": recommendations[:15],  # Top 15 recommendations
                "audit_timestamp": self.created_at.isoformat(),
                "workflow_duration": self.get_duration(),
            }
            
            return ExecutionResult.success_result(
                message=f"SEO audit completed successfully. Overall score: {overall_score:.1f}/100",
                data={
                    "summary": summary,
                    "detailed_results": results,
                    "workflow_metrics": self.get_metrics(),
                }
            )
            
        except Exception as e:
            return ExecutionResult.failure_result(
                message=f"Failed to aggregate audit results: {str(e)}",
                errors=[str(e)]
            )