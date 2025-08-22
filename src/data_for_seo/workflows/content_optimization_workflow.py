"""Content Optimization Workflow for content analysis and optimization recommendations."""

import asyncio
from typing import Any, Dict, List, Optional
from datetime import datetime

from ..agents.base import SEOTaskMixin
from ..models.base import ExecutionResult, SEOTask
from .workflow_engine import WorkflowEngine


class ContentOptimizationWorkflow(WorkflowEngine, SEOTaskMixin):
    """Content analysis and optimization recommendations workflow."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the content optimization workflow."""
        super().__init__(
            name="Content Optimization Workflow",
            description="Comprehensive content analysis with optimization recommendations",
            config=config,
        )
        
        # Workflow configuration
        self.analysis_depth = self.config.get("analysis_depth", "standard")  # basic, standard, deep
        self.include_competitor_content = self.config.get("include_competitor_content", True)
        self.content_types = self.config.get("content_types", ["blog", "page", "product"])
        self.optimization_focus = self.config.get("optimization_focus", ["seo", "readability", "engagement"])
        
    async def validate_parameters(self, parameters: Dict[str, Any]) -> ExecutionResult:
        """Validate content optimization parameters."""
        required_params = ["url"]
        
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
        
        # Validate URL
        url = parameters.get("url")
        if not self.validate_url(url):
            return ExecutionResult.failure_result(
                message="Invalid URL format",
                errors=[f"URL '{url}' is not a valid URL"]
            )
        
        # Validate target keywords if provided
        target_keywords = parameters.get("target_keywords", [])
        if target_keywords:
            invalid_keywords = [kw for kw in target_keywords if not self.validate_keyword(kw)]
            if invalid_keywords:
                return ExecutionResult.failure_result(
                    message="Invalid target keywords",
                    errors=[f"Invalid keywords: {', '.join(invalid_keywords)}"]
                )
        
        # Validate content type if provided
        content_type = parameters.get("content_type", "page")
        if content_type not in self.content_types:
            return ExecutionResult.failure_result(
                message="Invalid content type",
                errors=[f"Content type must be one of: {', '.join(self.content_types)}"]
            )
        
        return ExecutionResult.success_result("Parameters validated successfully")
    
    async def get_workflow_steps(self, parameters: Dict[str, Any]) -> List[str]:
        """Get the workflow steps for content optimization."""
        steps = [
            "content_extraction",
            "keyword_analysis",
            "readability_analysis",
            "seo_analysis",
            "structure_analysis",
            "engagement_analysis",
        ]
        
        # Add conditional steps based on configuration
        if self.include_competitor_content and parameters.get("competitors"):
            steps.append("competitor_content_analysis")
        
        if "seo" in self.optimization_focus:
            steps.append("seo_optimization_recommendations")
        
        if "readability" in self.optimization_focus:
            steps.append("readability_optimization")
        
        if "engagement" in self.optimization_focus:
            steps.append("engagement_optimization")
        
        if self.analysis_depth == "deep":
            steps.extend([
                "semantic_analysis",
                "content_gap_analysis",
                "user_intent_analysis",
            ])
        
        steps.append("generate_optimization_plan")
        
        return steps
    
    async def execute_workflow(
        self, 
        parameters: Dict[str, Any], 
        steps: List[str]
    ) -> ExecutionResult:
        """Execute the content optimization workflow."""
        try:
            url = parameters["url"]
            target_keywords = parameters.get("target_keywords", [])
            competitors = parameters.get("competitors", [])
            content_type = parameters.get("content_type", "page")
            
            results = {}
            
            # Extract and analyze content
            step_result = await self.execute_step(
                "content_extraction",
                self._extract_content,
                url, content_type
            )
            results["content"] = step_result.result.data if step_result.success else {}
            
            # Analyze keywords in content
            step_result = await self.execute_step(
                "keyword_analysis",
                self._analyze_keywords,
                results["content"], target_keywords
            )
            results["keyword_analysis"] = step_result.result.data if step_result.success else {}
            
            # Analyze readability
            step_result = await self.execute_step(
                "readability_analysis",
                self._analyze_readability,
                results["content"]
            )
            results["readability"] = step_result.result.data if step_result.success else {}
            
            # SEO analysis
            step_result = await self.execute_step(
                "seo_analysis",
                self._analyze_seo_elements,
                url, results["content"], target_keywords
            )
            results["seo_analysis"] = step_result.result.data if step_result.success else {}
            
            # Content structure analysis
            step_result = await self.execute_step(
                "structure_analysis",
                self._analyze_content_structure,
                results["content"]
            )
            results["structure"] = step_result.result.data if step_result.success else {}
            
            # Engagement analysis
            step_result = await self.execute_step(
                "engagement_analysis",
                self._analyze_engagement_factors,
                results["content"]
            )
            results["engagement"] = step_result.result.data if step_result.success else {}
            
            # Execute conditional steps
            if "competitor_content_analysis" in steps:
                step_result = await self.execute_step(
                    "competitor_content_analysis",
                    self._analyze_competitor_content,
                    target_keywords, competitors
                )
                results["competitor_analysis"] = step_result.result.data if step_result.success else {}
            
            if "semantic_analysis" in steps:
                step_result = await self.execute_step(
                    "semantic_analysis",
                    self._analyze_semantic_content,
                    results["content"], target_keywords
                )
                results["semantic_analysis"] = step_result.result.data if step_result.success else {}
            
            if "content_gap_analysis" in steps:
                step_result = await self.execute_step(
                    "content_gap_analysis",
                    self._analyze_content_gaps,
                    results["content"], target_keywords, competitors
                )
                results["gap_analysis"] = step_result.result.data if step_result.success else {}
            
            if "user_intent_analysis" in steps:
                step_result = await self.execute_step(
                    "user_intent_analysis",
                    self._analyze_user_intent,
                    target_keywords, results["content"]
                )
                results["intent_analysis"] = step_result.result.data if step_result.success else {}
            
            # Generate optimization recommendations
            step_result = await self.execute_step(
                "generate_optimization_plan",
                self._generate_optimization_plan,
                results
            )
            results["optimization_plan"] = step_result.result.data if step_result.success else {}
            
            return await self._aggregate_optimization_results(results)
            
        except Exception as e:
            return ExecutionResult.failure_result(
                message=f"Content optimization workflow failed: {str(e)}",
                errors=[str(e)]
            )
    
    async def _extract_content(self, url: str, content_type: str) -> ExecutionResult:
        """Extract and parse content from the URL."""
        try:
            # This would use web scraping or API to extract real content
            content_data = {
                "url": url,
                "content_type": content_type,
                "title": "Example Page Title",
                "meta_description": "Example meta description for the page",
                "headings": {
                    "h1": ["Main Heading"],
                    "h2": ["Section 1", "Section 2", "Section 3"],
                    "h3": ["Subsection 1.1", "Subsection 2.1"],
                },
                "body_text": "This is the main body text content of the page. It contains multiple paragraphs with various keywords and topics discussed in detail.",
                "word_count": 1250,
                "paragraph_count": 8,
                "sentence_count": 42,
                "images": {
                    "total": 5,
                    "with_alt_text": 3,
                    "without_alt_text": 2,
                },
                "links": {
                    "internal": 12,
                    "external": 8,
                    "nofollow": 2,
                },
                "extracted_at": datetime.utcnow().isoformat(),
            }
            
            return ExecutionResult.success_result(
                message=f"Successfully extracted content from {url}",
                data=content_data
            )
            
        except Exception as e:
            return ExecutionResult.failure_result(
                message=f"Failed to extract content: {str(e)}",
                errors=[str(e)]
            )
    
    async def _analyze_keywords(
        self, 
        content: Dict[str, Any], 
        target_keywords: List[str]
    ) -> ExecutionResult:
        """Analyze keyword usage and density in content."""
        try:
            body_text = content.get("body_text", "")
            title = content.get("title", "")
            meta_description = content.get("meta_description", "")
            word_count = content.get("word_count", 0)
            
            keyword_analysis = {
                "target_keywords": target_keywords,
                "keyword_density": {},
                "keyword_placement": {},
                "keyword_opportunities": [],
                "over_optimization_risks": [],
            }
            
            for keyword in target_keywords:
                # Simulate keyword analysis
                keyword_lower = keyword.lower()
                
                # Calculate density (simulated)
                density = round((hash(keyword) % 5 + 1) * 0.5, 2)  # 0.5% to 2.5%
                keyword_analysis["keyword_density"][keyword] = {
                    "density_percentage": density,
                    "occurrences": int(word_count * density / 100),
                    "recommended_range": "1.0-2.5%",
                    "status": "optimal" if 1.0 <= density <= 2.5 else "needs_attention",
                }
                
                # Analyze placement
                in_title = keyword_lower in title.lower()
                in_meta = keyword_lower in meta_description.lower()
                in_h1 = any(keyword_lower in h.lower() for h in content.get("headings", {}).get("h1", []))
                in_h2 = any(keyword_lower in h.lower() for h in content.get("headings", {}).get("h2", []))
                
                keyword_analysis["keyword_placement"][keyword] = {
                    "in_title": in_title,
                    "in_meta_description": in_meta,
                    "in_h1": in_h1,
                    "in_h2": in_h2,
                    "placement_score": sum([in_title, in_meta, in_h1, in_h2]),
                }
                
                # Generate recommendations
                if density < 1.0:
                    keyword_analysis["keyword_opportunities"].append({
                        "keyword": keyword,
                        "issue": "low_density",
                        "recommendation": f"Increase keyword density for '{keyword}' to 1-2.5%",
                    })
                elif density > 3.0:
                    keyword_analysis["over_optimization_risks"].append({
                        "keyword": keyword,
                        "issue": "high_density",
                        "recommendation": f"Reduce keyword density for '{keyword}' to avoid over-optimization",
                    })
                
                if not in_title:
                    keyword_analysis["keyword_opportunities"].append({
                        "keyword": keyword,
                        "issue": "missing_title",
                        "recommendation": f"Include '{keyword}' in page title",
                    })
            
            return ExecutionResult.success_result(
                message=f"Analyzed {len(target_keywords)} target keywords",
                data=keyword_analysis
            )
            
        except Exception as e:
            return ExecutionResult.failure_result(
                message=f"Failed to analyze keywords: {str(e)}",
                errors=[str(e)]
            )
    
    async def _analyze_readability(self, content: Dict[str, Any]) -> ExecutionResult:
        """Analyze content readability and complexity."""
        try:
            word_count = content.get("word_count", 0)
            sentence_count = content.get("sentence_count", 0)
            paragraph_count = content.get("paragraph_count", 0)
            
            # Calculate readability metrics (simulated)
            avg_words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0
            avg_sentences_per_paragraph = sentence_count / paragraph_count if paragraph_count > 0 else 0
            
            # Simulated readability scores
            flesch_score = max(0, min(100, 90 - (avg_words_per_sentence * 1.5)))
            grade_level = max(1, min(20, avg_words_per_sentence / 3))
            
            readability_analysis = {
                "scores": {
                    "flesch_reading_ease": round(flesch_score, 1),
                    "grade_level": round(grade_level, 1),
                    "readability_rating": self._get_readability_rating(flesch_score),
                },
                "metrics": {
                    "average_words_per_sentence": round(avg_words_per_sentence, 1),
                    "average_sentences_per_paragraph": round(avg_sentences_per_paragraph, 1),
                    "total_words": word_count,
                    "total_sentences": sentence_count,
                    "total_paragraphs": paragraph_count,
                },
                "recommendations": [],
            }
            
            # Generate readability recommendations
            if avg_words_per_sentence > 20:
                readability_analysis["recommendations"].append({
                    "issue": "long_sentences",
                    "recommendation": "Break down long sentences to improve readability",
                    "priority": "medium",
                })
            
            if avg_sentences_per_paragraph > 6:
                readability_analysis["recommendations"].append({
                    "issue": "long_paragraphs",
                    "recommendation": "Break down long paragraphs for better readability",
                    "priority": "low",
                })
            
            if flesch_score < 50:
                readability_analysis["recommendations"].append({
                    "issue": "difficult_reading",
                    "recommendation": "Simplify language and sentence structure for broader audience",
                    "priority": "high",
                })
            
            return ExecutionResult.success_result(
                message="Completed readability analysis",
                data=readability_analysis
            )
            
        except Exception as e:
            return ExecutionResult.failure_result(
                message=f"Failed to analyze readability: {str(e)}",
                errors=[str(e)]
            )
    
    def _get_readability_rating(self, flesch_score: float) -> str:
        """Get readability rating based on Flesch score."""
        if flesch_score >= 90:
            return "Very Easy"
        elif flesch_score >= 80:
            return "Easy"
        elif flesch_score >= 70:
            return "Fairly Easy"
        elif flesch_score >= 60:
            return "Standard"
        elif flesch_score >= 50:
            return "Fairly Difficult"
        elif flesch_score >= 30:
            return "Difficult"
        else:
            return "Very Difficult"
    
    async def _analyze_seo_elements(
        self, 
        url: str, 
        content: Dict[str, Any], 
        target_keywords: List[str]
    ) -> ExecutionResult:
        """Analyze SEO elements of the content."""
        try:
            title = content.get("title", "")
            meta_description = content.get("meta_description", "")
            headings = content.get("headings", {})
            images = content.get("images", {})
            links = content.get("links", {})
            
            seo_analysis = {
                "title_analysis": {
                    "length": len(title),
                    "optimal_length": title and 30 <= len(title) <= 60,
                    "includes_target_keyword": any(kw.lower() in title.lower() for kw in target_keywords),
                    "recommendations": [],
                },
                "meta_description_analysis": {
                    "length": len(meta_description),
                    "optimal_length": meta_description and 120 <= len(meta_description) <= 155,
                    "includes_target_keyword": any(kw.lower() in meta_description.lower() for kw in target_keywords),
                    "recommendations": [],
                },
                "heading_analysis": {
                    "h1_count": len(headings.get("h1", [])),
                    "h2_count": len(headings.get("h2", [])),
                    "h3_count": len(headings.get("h3", [])),
                    "proper_hierarchy": True,  # Simplified
                    "keyword_optimization": {},
                    "recommendations": [],
                },
                "image_analysis": {
                    "total_images": images.get("total", 0),
                    "alt_text_coverage": round((images.get("with_alt_text", 0) / max(images.get("total", 1), 1)) * 100, 1),
                    "recommendations": [],
                },
                "link_analysis": {
                    "internal_links": links.get("internal", 0),
                    "external_links": links.get("external", 0),
                    "nofollow_links": links.get("nofollow", 0),
                    "link_ratio": "good",  # Simplified
                    "recommendations": [],
                },
            }
            
            # Generate title recommendations
            if len(title) < 30:
                seo_analysis["title_analysis"]["recommendations"].append(
                    "Title is too short. Expand to 30-60 characters for better SEO."
                )
            elif len(title) > 60:
                seo_analysis["title_analysis"]["recommendations"].append(
                    "Title is too long. Shorten to under 60 characters to avoid truncation."
                )
            
            if not any(kw.lower() in title.lower() for kw in target_keywords):
                seo_analysis["title_analysis"]["recommendations"].append(
                    "Include target keywords in the title tag."
                )
            
            # Generate meta description recommendations
            if len(meta_description) < 120:
                seo_analysis["meta_description_analysis"]["recommendations"].append(
                    "Meta description is too short. Expand to 120-155 characters."
                )
            elif len(meta_description) > 155:
                seo_analysis["meta_description_analysis"]["recommendations"].append(
                    "Meta description is too long. Shorten to under 155 characters."
                )
            
            # Generate heading recommendations
            if len(headings.get("h1", [])) == 0:
                seo_analysis["heading_analysis"]["recommendations"].append(
                    "Add an H1 heading to the page."
                )
            elif len(headings.get("h1", [])) > 1:
                seo_analysis["heading_analysis"]["recommendations"].append(
                    "Use only one H1 heading per page."
                )
            
            # Generate image recommendations
            if images.get("without_alt_text", 0) > 0:
                seo_analysis["image_analysis"]["recommendations"].append(
                    f"Add alt text to {images['without_alt_text']} images for better accessibility and SEO."
                )
            
            return ExecutionResult.success_result(
                message="Completed SEO elements analysis",
                data=seo_analysis
            )
            
        except Exception as e:
            return ExecutionResult.failure_result(
                message=f"Failed to analyze SEO elements: {str(e)}",
                errors=[str(e)]
            )
    
    async def _analyze_content_structure(self, content: Dict[str, Any]) -> ExecutionResult:
        """Analyze content structure and organization."""
        try:
            headings = content.get("headings", {})
            word_count = content.get("word_count", 0)
            paragraph_count = content.get("paragraph_count", 0)
            
            structure_analysis = {
                "hierarchy_analysis": {
                    "proper_hierarchy": True,  # Simplified check
                    "heading_distribution": {
                        "h1": len(headings.get("h1", [])),
                        "h2": len(headings.get("h2", [])),
                        "h3": len(headings.get("h3", [])),
                    },
                    "issues": [],
                },
                "content_organization": {
                    "average_words_per_section": round(word_count / max(len(headings.get("h2", [])), 1)),
                    "content_balance": "good",  # Simplified
                    "recommendations": [],
                },
                "formatting_analysis": {
                    "paragraph_length": "optimal" if 3 <= paragraph_count / max(word_count / 100, 1) <= 7 else "needs_improvement",
                    "content_density": word_count / max(paragraph_count, 1),
                    "recommendations": [],
                },
            }
            
            # Generate structure recommendations
            if len(headings.get("h2", [])) < 2 and word_count > 500:
                structure_analysis["content_organization"]["recommendations"].append(
                    "Add more H2 headings to break up long content sections."
                )
            
            if word_count > 2000 and len(headings.get("h2", [])) < 4:
                structure_analysis["content_organization"]["recommendations"].append(
                    "Consider adding more sections with H2 headings for better content organization."
                )
            
            return ExecutionResult.success_result(
                message="Completed content structure analysis",
                data=structure_analysis
            )
            
        except Exception as e:
            return ExecutionResult.failure_result(
                message=f"Failed to analyze content structure: {str(e)}",
                errors=[str(e)]
            )
    
    async def _analyze_engagement_factors(self, content: Dict[str, Any]) -> ExecutionResult:
        """Analyze content engagement factors."""
        try:
            word_count = content.get("word_count", 0)
            images = content.get("images", {})
            links = content.get("links", {})
            
            engagement_analysis = {
                "content_length": {
                    "word_count": word_count,
                    "optimal_length": 1000 <= word_count <= 2500,
                    "length_category": self._categorize_content_length(word_count),
                },
                "multimedia_usage": {
                    "images_per_500_words": round(images.get("total", 0) / max(word_count / 500, 1), 1),
                    "optimal_image_ratio": 1 <= (images.get("total", 0) / max(word_count / 500, 1)) <= 3,
                    "multimedia_score": 7,  # Simulated score out of 10
                },
                "interactivity": {
                    "internal_link_density": round(links.get("internal", 0) / max(word_count / 100, 1), 1),
                    "external_link_density": round(links.get("external", 0) / max(word_count / 100, 1), 1),
                    "engagement_elements": [],  # Would detect forms, CTAs, etc.
                },
                "recommendations": [],
            }
            
            # Generate engagement recommendations
            if word_count < 300:
                engagement_analysis["recommendations"].append({
                    "category": "content_length",
                    "recommendation": "Expand content to at least 300 words for better engagement",
                    "priority": "high",
                })
            elif word_count > 3000:
                engagement_analysis["recommendations"].append({
                    "category": "content_length",
                    "recommendation": "Consider breaking long content into multiple pages or sections",
                    "priority": "medium",
                })
            
            if images.get("total", 0) == 0:
                engagement_analysis["recommendations"].append({
                    "category": "multimedia",
                    "recommendation": "Add relevant images to improve visual appeal and engagement",
                    "priority": "medium",
                })
            
            if links.get("internal", 0) < 2:
                engagement_analysis["recommendations"].append({
                    "category": "interactivity",
                    "recommendation": "Add more internal links to related content",
                    "priority": "low",
                })
            
            return ExecutionResult.success_result(
                message="Completed engagement analysis",
                data=engagement_analysis
            )
            
        except Exception as e:
            return ExecutionResult.failure_result(
                message=f"Failed to analyze engagement factors: {str(e)}",
                errors=[str(e)]
            )
    
    def _categorize_content_length(self, word_count: int) -> str:
        """Categorize content length."""
        if word_count < 300:
            return "short"
        elif word_count < 1000:
            return "medium"
        elif word_count < 2500:
            return "long"
        else:
            return "very_long"
    
    async def _analyze_competitor_content(
        self, 
        target_keywords: List[str], 
        competitors: List[str]
    ) -> ExecutionResult:
        """Analyze competitor content for the same keywords."""
        try:
            competitor_analysis = {
                "competitors_analyzed": len(competitors),
                "content_gaps": [],
                "content_opportunities": [],
                "competitive_insights": {},
            }
            
            for competitor in competitors:
                # Simulated competitor content analysis
                competitor_domain = self.extract_domain(competitor) if self.validate_url(competitor) else competitor
                
                competitor_analysis["competitive_insights"][competitor_domain] = {
                    "average_content_length": hash(competitor) % 1000 + 1000,  # 1000-2000 words
                    "keyword_coverage": round((hash(competitor) % 50 + 50) / 100, 2),  # 50-100%
                    "content_freshness": "recent",
                    "content_depth": "comprehensive",
                }
            
            # Identify content gaps and opportunities
            competitor_analysis["content_gaps"] = [
                {
                    "keyword": kw,
                    "gap_type": "content_depth",
                    "recommendation": f"Expand content depth for '{kw}' to match competitor standards",
                }
                for kw in target_keywords[:3]  # Sample gaps
            ]
            
            competitor_analysis["content_opportunities"] = [
                {
                    "opportunity": "long_tail_keywords",
                    "description": "Target additional long-tail variations not covered by competitors",
                },
                {
                    "opportunity": "content_format",
                    "description": "Use different content formats (videos, infographics) to stand out",
                },
            ]
            
            return ExecutionResult.success_result(
                message=f"Analyzed content from {len(competitors)} competitors",
                data=competitor_analysis
            )
            
        except Exception as e:
            return ExecutionResult.failure_result(
                message=f"Failed to analyze competitor content: {str(e)}",
                errors=[str(e)]
            )
    
    async def _analyze_semantic_content(
        self, 
        content: Dict[str, Any], 
        target_keywords: List[str]
    ) -> ExecutionResult:
        """Analyze semantic content and topic coverage."""
        try:
            body_text = content.get("body_text", "")
            
            semantic_analysis = {
                "topic_coverage": {},
                "semantic_keywords": [],
                "content_themes": [],
                "topic_authority_score": 75,  # Simulated score
                "recommendations": [],
            }
            
            # Simulate semantic keyword extraction
            for keyword in target_keywords:
                semantic_analysis["topic_coverage"][keyword] = {
                    "coverage_score": hash(keyword) % 30 + 70,  # 70-100%
                    "related_topics": [f"related_topic_{i}" for i in range(3)],
                    "semantic_variations": [f"{keyword} variation {i}" for i in range(2)],
                }
                
                # Generate related semantic keywords
                semantic_analysis["semantic_keywords"].extend([
                    f"{keyword} benefits",
                    f"{keyword} guide",
                    f"best {keyword}",
                ])
            
            # Identify content themes
            semantic_analysis["content_themes"] = [
                "informational",
                "how-to",
                "comparison",
            ]
            
            # Generate semantic recommendations
            semantic_analysis["recommendations"] = [
                {
                    "type": "semantic_expansion",
                    "recommendation": "Include more semantic variations of target keywords",
                    "priority": "medium",
                },
                {
                    "type": "topic_depth",
                    "recommendation": "Expand coverage of related subtopics",
                    "priority": "high",
                },
            ]
            
            return ExecutionResult.success_result(
                message="Completed semantic content analysis",
                data=semantic_analysis
            )
            
        except Exception as e:
            return ExecutionResult.failure_result(
                message=f"Failed to analyze semantic content: {str(e)}",
                errors=[str(e)]
            )
    
    async def _analyze_content_gaps(
        self, 
        content: Dict[str, Any], 
        target_keywords: List[str], 
        competitors: List[str]
    ) -> ExecutionResult:
        """Analyze content gaps compared to competitors."""
        try:
            gap_analysis = {
                "identified_gaps": [],
                "content_opportunities": [],
                "priority_improvements": [],
            }
            
            # Simulate gap identification
            for keyword in target_keywords:
                gap_analysis["identified_gaps"].append({
                    "keyword": keyword,
                    "gap_type": "content_depth",
                    "severity": "medium",
                    "description": f"Content depth for '{keyword}' is below competitor average",
                })
            
            gap_analysis["content_opportunities"] = [
                {
                    "opportunity": "FAQ section",
                    "description": "Add FAQ section to address common user questions",
                    "potential_impact": "high",
                },
                {
                    "opportunity": "visual_content",
                    "description": "Add more visual elements (charts, diagrams, videos)",
                    "potential_impact": "medium",
                },
            ]
            
            gap_analysis["priority_improvements"] = [
                {
                    "improvement": "expand_introduction",
                    "priority": "high",
                    "effort": "low",
                    "impact": "medium",
                },
                {
                    "improvement": "add_examples",
                    "priority": "medium",
                    "effort": "medium",
                    "impact": "high",
                },
            ]
            
            return ExecutionResult.success_result(
                message="Completed content gap analysis",
                data=gap_analysis
            )
            
        except Exception as e:
            return ExecutionResult.failure_result(
                message=f"Failed to analyze content gaps: {str(e)}",
                errors=[str(e)]
            )
    
    async def _analyze_user_intent(
        self, 
        target_keywords: List[str], 
        content: Dict[str, Any]
    ) -> ExecutionResult:
        """Analyze user intent alignment with content."""
        try:
            intent_analysis = {
                "intent_alignment": {},
                "content_intent_score": 82,  # Simulated score
                "intent_gaps": [],
                "recommendations": [],
            }
            
            # Analyze intent for each keyword
            for keyword in target_keywords:
                # Simulate intent classification
                intent_type = ["informational", "navigational", "transactional"][hash(keyword) % 3]
                alignment_score = hash(keyword) % 30 + 70  # 70-100%
                
                intent_analysis["intent_alignment"][keyword] = {
                    "intent_type": intent_type,
                    "alignment_score": alignment_score,
                    "content_match": alignment_score > 80,
                }
                
                if alignment_score < 80:
                    intent_analysis["intent_gaps"].append({
                        "keyword": keyword,
                        "intent_type": intent_type,
                        "current_score": alignment_score,
                        "recommendation": f"Better align content with {intent_type} intent for '{keyword}'",
                    })
            
            # Generate intent-based recommendations
            intent_analysis["recommendations"] = [
                {
                    "category": "intent_optimization",
                    "recommendation": "Add more actionable information for transactional keywords",
                    "priority": "high",
                },
                {
                    "category": "user_journey",
                    "recommendation": "Include clear next steps for users at different stages",
                    "priority": "medium",
                },
            ]
            
            return ExecutionResult.success_result(
                message="Completed user intent analysis",
                data=intent_analysis
            )
            
        except Exception as e:
            return ExecutionResult.failure_result(
                message=f"Failed to analyze user intent: {str(e)}",
                errors=[str(e)]
            )
    
    async def _generate_optimization_plan(self, results: Dict[str, Any]) -> ExecutionResult:
        """Generate comprehensive content optimization plan."""
        try:
            optimization_plan = {
                "executive_summary": {
                    "overall_score": 0,
                    "priority_actions": [],
                    "quick_wins": [],
                    "long_term_improvements": [],
                },
                "detailed_recommendations": {
                    "seo_optimizations": [],
                    "readability_improvements": [],
                    "engagement_enhancements": [],
                    "structural_changes": [],
                },
                "implementation_timeline": {
                    "immediate": [],  # 0-1 week
                    "short_term": [],  # 1-4 weeks
                    "medium_term": [],  # 1-3 months
                    "long_term": [],  # 3+ months
                },
                "expected_outcomes": {
                    "seo_impact": "medium",
                    "user_experience_impact": "high",
                    "engagement_impact": "medium",
                },
            }
            
            # Calculate overall optimization score
            scores = []
            if "readability" in results and "scores" in results["readability"]:
                scores.append(results["readability"]["scores"].get("flesch_reading_ease", 0))
            if "engagement" in results and "multimedia_usage" in results["engagement"]:
                scores.append(results["engagement"]["multimedia_usage"].get("multimedia_score", 0) * 10)
            
            optimization_plan["executive_summary"]["overall_score"] = round(sum(scores) / len(scores) if scores else 75, 1)
            
            # Compile priority actions from all analyses
            priority_actions = []
            
            # From SEO analysis
            if "seo_analysis" in results:
                seo_data = results["seo_analysis"]
                for element in ["title_analysis", "meta_description_analysis", "heading_analysis"]:
                    if element in seo_data and seo_data[element].get("recommendations"):
                        priority_actions.extend(seo_data[element]["recommendations"][:2])
            
            # From readability analysis
            if "readability" in results and "recommendations" in results["readability"]:
                priority_actions.extend([r["recommendation"] for r in results["readability"]["recommendations"][:2]])
            
            optimization_plan["executive_summary"]["priority_actions"] = priority_actions[:5]
            
            # Identify quick wins
            optimization_plan["executive_summary"]["quick_wins"] = [
                "Optimize title tag length and keyword inclusion",
                "Add missing alt text to images",
                "Improve meta description",
                "Add internal links to related content",
            ]
            
            # Generate detailed recommendations by category
            optimization_plan["detailed_recommendations"]["seo_optimizations"] = [
                {
                    "action": "Optimize title tag",
                    "priority": "high",
                    "effort": "low",
                    "impact": "high",
                    "description": "Ensure title tag includes target keywords and is 30-60 characters",
                },
                {
                    "action": "Improve heading structure",
                    "priority": "medium",
                    "effort": "medium",
                    "impact": "medium",
                    "description": "Use proper H1-H6 hierarchy with target keywords",
                },
            ]
            
            optimization_plan["detailed_recommendations"]["readability_improvements"] = [
                {
                    "action": "Break up long sentences",
                    "priority": "medium",
                    "effort": "medium",
                    "impact": "high",
                    "description": "Reduce average sentence length to improve readability",
                },
            ]
            
            optimization_plan["detailed_recommendations"]["engagement_enhancements"] = [
                {
                    "action": "Add visual elements",
                    "priority": "medium",
                    "effort": "high",
                    "impact": "high",
                    "description": "Include relevant images, charts, or videos",
                },
            ]
            
            # Create implementation timeline
            optimization_plan["implementation_timeline"]["immediate"] = [
                "Fix title tag and meta description",
                "Add missing alt text",
            ]
            
            optimization_plan["implementation_timeline"]["short_term"] = [
                "Improve content structure",
                "Add internal linking",
            ]
            
            optimization_plan["implementation_timeline"]["medium_term"] = [
                "Expand content depth",
                "Add multimedia elements",
            ]
            
            return ExecutionResult.success_result(
                message="Generated comprehensive optimization plan",
                data=optimization_plan
            )
            
        except Exception as e:
            return ExecutionResult.failure_result(
                message=f"Failed to generate optimization plan: {str(e)}",
                errors=[str(e)]
            )
    
    async def _aggregate_optimization_results(self, results: Dict[str, Any]) -> ExecutionResult:
        """Aggregate all optimization results into final report."""
        try:
            # Calculate success metrics
            successful_steps = sum(1 for result in results.values() if isinstance(result, dict))
            total_steps = len(results)
            success_rate = (successful_steps / total_steps) * 100 if total_steps > 0 else 0
            
            # Count total recommendations
            total_recommendations = 0
            high_priority_recommendations = 0
            
            for result in results.values():
                if isinstance(result, dict) and "recommendations" in result:
                    recommendations = result["recommendations"]
                    if isinstance(recommendations, list):
                        total_recommendations += len(recommendations)
                        high_priority_recommendations += sum(
                            1 for r in recommendations 
                            if isinstance(r, dict) and r.get("priority") == "high"
                        )
            
            # Generate final summary
            final_report = {
                "workflow_summary": {
                    "workflow_id": str(self.id),
                    "execution_time": self.get_duration(),
                    "success_rate": round(success_rate, 1),
                    "steps_completed": successful_steps,
                    "total_steps": total_steps,
                },
                "optimization_summary": {
                    "total_recommendations": total_recommendations,
                    "high_priority_recommendations": high_priority_recommendations,
                    "optimization_categories": list(self.optimization_focus),
                    "analysis_depth": self.analysis_depth,
                },
                "detailed_results": results,
                "metadata": {
                    "workflow_name": self.name,
                    "execution_timestamp": datetime.utcnow().isoformat(),
                    "configuration": {
                        "analysis_depth": self.analysis_depth,
                        "optimization_focus": self.optimization_focus,
                        "include_competitor_content": self.include_competitor_content,
                    },
                },
            }
            
            return ExecutionResult.success_result(
                message=f"Content optimization completed with {total_recommendations} recommendations",
                data=final_report
            )
            
        except Exception as e:
            return ExecutionResult.failure_result(
                message=f"Failed to aggregate optimization results: {str(e)}",
                errors=[str(e)]
            )