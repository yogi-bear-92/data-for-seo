"""Competitor Analysis Workflow for competitive SEO intelligence gathering."""

import asyncio
from typing import Any, Dict, List, Optional
from datetime import datetime

from ..agents.base import SEOTaskMixin
from ..models.base import ExecutionResult, SEOTask
from .workflow_engine import WorkflowEngine


class CompetitorAnalysisWorkflow(WorkflowEngine, SEOTaskMixin):
    """Competitive SEO intelligence gathering and analysis workflow."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the competitor analysis workflow."""
        super().__init__(
            name="Competitor Analysis Workflow",
            description="Comprehensive competitive SEO intelligence gathering and analysis",
            config=config,
        )
        
        # Workflow configuration
        self.analysis_scope = self.config.get("analysis_scope", "comprehensive")  # basic, standard, comprehensive
        self.competitor_limit = self.config.get("competitor_limit", 5)
        self.keyword_limit = self.config.get("keyword_limit", 100)
        self.include_content_analysis = self.config.get("include_content_analysis", True)
        self.include_backlink_analysis = self.config.get("include_backlink_analysis", True)
        self.include_technical_analysis = self.config.get("include_technical_analysis", True)
        
    async def validate_parameters(self, parameters: Dict[str, Any]) -> ExecutionResult:
        """Validate competitor analysis parameters."""
        required_params = ["target_url", "competitors"]
        
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
        
        # Validate target URL
        target_url = parameters.get("target_url")
        if not self.validate_url(target_url):
            return ExecutionResult.failure_result(
                message="Invalid target URL format",
                errors=[f"URL '{target_url}' is not a valid URL"]
            )
        
        # Validate competitors
        competitors = parameters.get("competitors", [])
        if not competitors or not isinstance(competitors, list):
            return ExecutionResult.failure_result(
                message="Competitors must be provided as a non-empty list",
                errors=["Competitors parameter is required and must be a list"]
            )
        
        if len(competitors) > self.competitor_limit:
            return ExecutionResult.failure_result(
                message="Too many competitors",
                errors=[f"Maximum {self.competitor_limit} competitors allowed"]
            )
        
        invalid_competitors = [comp for comp in competitors if not self.validate_url(comp)]
        if invalid_competitors:
            return ExecutionResult.failure_result(
                message="Invalid competitor URLs",
                errors=[f"Invalid URLs: {', '.join(invalid_competitors)}"]
            )
        
        # Validate keywords if provided
        keywords = parameters.get("keywords", [])
        if keywords and len(keywords) > self.keyword_limit:
            return ExecutionResult.failure_result(
                message="Too many keywords",
                errors=[f"Maximum {self.keyword_limit} keywords allowed"]
            )
        
        return ExecutionResult.success_result("Parameters validated successfully")
    
    async def get_workflow_steps(self, parameters: Dict[str, Any]) -> List[str]:
        """Get the workflow steps for competitor analysis."""
        steps = [
            "initialize_analysis",
            "competitor_discovery",
            "keyword_gap_analysis",
            "ranking_comparison",
        ]
        
        # Add conditional steps based on configuration
        if self.include_content_analysis:
            steps.append("content_analysis")
        
        if self.include_backlink_analysis:
            steps.append("backlink_analysis")
        
        if self.include_technical_analysis:
            steps.append("technical_comparison")
        
        if self.analysis_scope == "comprehensive":
            steps.extend([
                "serp_feature_analysis",
                "market_share_analysis",
                "opportunity_identification",
            ])
        
        steps.append("generate_competitive_intelligence")
        
        return steps
    
    async def execute_workflow(
        self, 
        parameters: Dict[str, Any], 
        steps: List[str]
    ) -> ExecutionResult:
        """Execute the competitor analysis workflow."""
        try:
            target_url = parameters["target_url"]
            competitors = parameters["competitors"]
            keywords = parameters.get("keywords", [])
            
            results = {}
            
            # Initialize analysis
            step_result = await self.execute_step(
                "initialize_analysis",
                self._initialize_analysis,
                target_url, competitors, keywords
            )
            results["initialization"] = step_result.result.data if step_result.success else {}
            
            # Discover additional competitors if needed
            step_result = await self.execute_step(
                "competitor_discovery",
                self._discover_competitors,
                target_url, competitors, keywords
            )
            results["competitor_discovery"] = step_result.result.data if step_result.success else {}
            
            # Keyword gap analysis
            step_result = await self.execute_step(
                "keyword_gap_analysis",
                self._analyze_keyword_gaps,
                target_url, competitors, keywords
            )
            results["keyword_gaps"] = step_result.result.data if step_result.success else {}
            
            # Ranking comparison
            step_result = await self.execute_step(
                "ranking_comparison",
                self._compare_rankings,
                target_url, competitors, keywords
            )
            results["ranking_comparison"] = step_result.result.data if step_result.success else {}
            
            # Execute conditional steps
            if "content_analysis" in steps:
                step_result = await self.execute_step(
                    "content_analysis",
                    self._analyze_competitor_content,
                    target_url, competitors
                )
                results["content_analysis"] = step_result.result.data if step_result.success else {}
            
            if "backlink_analysis" in steps:
                step_result = await self.execute_step(
                    "backlink_analysis",
                    self._analyze_backlinks,
                    target_url, competitors
                )
                results["backlink_analysis"] = step_result.result.data if step_result.success else {}
            
            if "technical_comparison" in steps:
                step_result = await self.execute_step(
                    "technical_comparison",
                    self._compare_technical_seo,
                    target_url, competitors
                )
                results["technical_comparison"] = step_result.result.data if step_result.success else {}
            
            if "serp_feature_analysis" in steps:
                step_result = await self.execute_step(
                    "serp_feature_analysis",
                    self._analyze_serp_features,
                    target_url, competitors, keywords
                )
                results["serp_features"] = step_result.result.data if step_result.success else {}
            
            if "market_share_analysis" in steps:
                step_result = await self.execute_step(
                    "market_share_analysis",
                    self._analyze_market_share,
                    target_url, competitors, keywords
                )
                results["market_share"] = step_result.result.data if step_result.success else {}
            
            if "opportunity_identification" in steps:
                step_result = await self.execute_step(
                    "opportunity_identification",
                    self._identify_opportunities,
                    target_url, competitors, results
                )
                results["opportunities"] = step_result.result.data if step_result.success else {}
            
            # Generate final competitive intelligence report
            step_result = await self.execute_step(
                "generate_competitive_intelligence",
                self._generate_intelligence_report,
                results
            )
            results["intelligence_report"] = step_result.result.data if step_result.success else {}
            
            return await self._aggregate_analysis_results(results)
            
        except Exception as e:
            return ExecutionResult.failure_result(
                message=f"Competitor analysis workflow failed: {str(e)}",
                errors=[str(e)]
            )
    
    async def _initialize_analysis(
        self,
        target_url: str,
        competitors: List[str],
        keywords: List[str],
    ) -> ExecutionResult:
        """Initialize competitor analysis session."""
        try:
            target_domain = self.extract_domain(target_url)
            competitor_domains = [self.extract_domain(comp) for comp in competitors]
            
            analysis_config = {
                "analysis_id": str(self.id),
                "target_domain": target_domain,
                "target_url": target_url,
                "competitor_count": len(competitors),
                "competitor_domains": competitor_domains,
                "keyword_count": len(keywords),
                "analysis_scope": self.analysis_scope,
                "start_time": datetime.utcnow().isoformat(),
            }
            
            return ExecutionResult.success_result(
                message=f"Initialized competitor analysis for {target_domain} vs {len(competitors)} competitors",
                data=analysis_config
            )
            
        except Exception as e:
            return ExecutionResult.failure_result(
                message=f"Failed to initialize analysis: {str(e)}",
                errors=[str(e)]
            )
    
    async def _discover_competitors(
        self,
        target_url: str,
        existing_competitors: List[str],
        keywords: List[str],
    ) -> ExecutionResult:
        """Discover additional competitors based on keyword overlap."""
        try:
            target_domain = self.extract_domain(target_url)
            
            # Simulate competitor discovery based on keyword research
            discovered_competitors = []
            
            # Generate some simulated competitor domains
            potential_competitors = [
                f"competitor-{i}.com" for i in range(1, 6)
            ]
            
            for potential in potential_competitors:
                if potential not in [self.extract_domain(comp) for comp in existing_competitors]:
                    # Simulate relevance scoring
                    relevance_score = hash(f"{target_domain}{potential}") % 40 + 60  # 60-100%
                    
                    if relevance_score > 75:  # Only include highly relevant competitors
                        discovered_competitors.append({
                            "domain": potential,
                            "relevance_score": relevance_score,
                            "overlap_keywords": hash(potential) % 20 + 10,  # 10-30 keywords
                            "discovery_method": "keyword_overlap",
                        })
            
            discovery_results = {
                "discovered_competitors": discovered_competitors,
                "total_discovered": len(discovered_competitors),
                "existing_competitors": len(existing_competitors),
                "discovery_methods": ["keyword_overlap", "serp_analysis"],
            }
            
            return ExecutionResult.success_result(
                message=f"Discovered {len(discovered_competitors)} additional competitors",
                data=discovery_results
            )
            
        except Exception as e:
            return ExecutionResult.failure_result(
                message=f"Failed to discover competitors: {str(e)}",
                errors=[str(e)]
            )
    
    async def _analyze_keyword_gaps(
        self,
        target_url: str,
        competitors: List[str],
        keywords: List[str],
    ) -> ExecutionResult:
        """Analyze keyword gaps between target and competitors."""
        try:
            target_domain = self.extract_domain(target_url)
            
            gap_analysis = {
                "target_domain": target_domain,
                "keyword_gaps": {},
                "opportunity_keywords": [],
                "competitive_keywords": [],
                "gap_summary": {
                    "total_gaps": 0,
                    "high_opportunity": 0,
                    "medium_opportunity": 0,
                    "low_opportunity": 0,
                },
            }
            
            for competitor in competitors:
                competitor_domain = self.extract_domain(competitor)
                
                # Simulate keyword gap analysis
                competitor_keywords = []
                gap_keywords = []
                
                # Generate simulated competitor keywords
                for i in range(20):  # Simulate 20 competitor keywords
                    keyword = f"competitor_{competitor_domain}_keyword_{i}"
                    search_volume = hash(keyword) % 5000 + 100  # 100-5100
                    difficulty = hash(keyword) % 100 + 1  # 1-100
                    
                    competitor_keywords.append({
                        "keyword": keyword,
                        "search_volume": search_volume,
                        "difficulty": difficulty,
                        "position": hash(keyword) % 10 + 1,  # Position 1-10
                    })
                    
                    # Check if it's a gap (target doesn't rank for it)
                    if hash(f"{target_domain}{keyword}") % 3 == 0:  # 33% chance of gap
                        opportunity_level = "high" if search_volume > 1000 and difficulty < 50 else "medium" if search_volume > 500 else "low"
                        
                        gap_keywords.append({
                            "keyword": keyword,
                            "search_volume": search_volume,
                            "difficulty": difficulty,
                            "competitor_position": hash(keyword) % 10 + 1,
                            "opportunity_level": opportunity_level,
                        })
                        
                        gap_analysis["gap_summary"][f"{opportunity_level}_opportunity"] += 1
                
                gap_analysis["keyword_gaps"][competitor_domain] = {
                    "total_keywords": len(competitor_keywords),
                    "gap_keywords": gap_keywords,
                    "gap_count": len(gap_keywords),
                }
                
                gap_analysis["opportunity_keywords"].extend(gap_keywords)
            
            # Remove duplicates and sort by opportunity
            unique_opportunities = {}
            for kw in gap_analysis["opportunity_keywords"]:
                if kw["keyword"] not in unique_opportunities:
                    unique_opportunities[kw["keyword"]] = kw
            
            gap_analysis["opportunity_keywords"] = sorted(
                unique_opportunities.values(),
                key=lambda x: (x["search_volume"], -x["difficulty"]),
                reverse=True
            )[:50]  # Top 50 opportunities
            
            gap_analysis["gap_summary"]["total_gaps"] = len(gap_analysis["opportunity_keywords"])
            
            return ExecutionResult.success_result(
                message=f"Identified {gap_analysis['gap_summary']['total_gaps']} keyword gaps",
                data=gap_analysis
            )
            
        except Exception as e:
            return ExecutionResult.failure_result(
                message=f"Failed to analyze keyword gaps: {str(e)}",
                errors=[str(e)]
            )
    
    async def _compare_rankings(
        self,
        target_url: str,
        competitors: List[str],
        keywords: List[str],
    ) -> ExecutionResult:
        """Compare rankings across target and competitor websites."""
        try:
            target_domain = self.extract_domain(target_url)
            
            ranking_comparison = {
                "target_domain": target_domain,
                "keyword_comparison": {},
                "ranking_summary": {
                    "target_wins": 0,
                    "competitor_wins": 0,
                    "total_keywords": len(keywords),
                },
                "position_analysis": {
                    "average_position": {},
                    "top_10_count": {},
                    "top_3_count": {},
                },
            }
            
            for keyword in keywords:
                keyword_data = {
                    "keyword": keyword,
                    "positions": {},
                    "best_performer": "",
                    "target_position": None,
                }
                
                # Generate target position
                target_position = hash(f"{target_domain}{keyword}") % 100 + 1
                keyword_data["positions"][target_domain] = target_position
                keyword_data["target_position"] = target_position
                
                best_position = target_position
                best_performer = target_domain
                
                # Generate competitor positions
                for competitor in competitors:
                    competitor_domain = self.extract_domain(competitor)
                    competitor_position = hash(f"{competitor_domain}{keyword}") % 100 + 1
                    keyword_data["positions"][competitor_domain] = competitor_position
                    
                    if competitor_position < best_position:
                        best_position = competitor_position
                        best_performer = competitor_domain
                
                keyword_data["best_performer"] = best_performer
                
                # Update summary
                if best_performer == target_domain:
                    ranking_comparison["ranking_summary"]["target_wins"] += 1
                else:
                    ranking_comparison["ranking_summary"]["competitor_wins"] += 1
                
                ranking_comparison["keyword_comparison"][keyword] = keyword_data
            
            # Calculate position analysis
            all_domains = [target_domain] + [self.extract_domain(comp) for comp in competitors]
            
            for domain in all_domains:
                positions = [
                    data["positions"].get(domain, 101)
                    for data in ranking_comparison["keyword_comparison"].values()
                ]
                
                valid_positions = [p for p in positions if p <= 100]
                
                ranking_comparison["position_analysis"]["average_position"][domain] = (
                    round(sum(valid_positions) / len(valid_positions), 1) if valid_positions else 0
                )
                ranking_comparison["position_analysis"]["top_10_count"][domain] = len([p for p in valid_positions if p <= 10])
                ranking_comparison["position_analysis"]["top_3_count"][domain] = len([p for p in valid_positions if p <= 3])
            
            return ExecutionResult.success_result(
                message=f"Compared rankings for {len(keywords)} keywords across {len(competitors) + 1} domains",
                data=ranking_comparison
            )
            
        except Exception as e:
            return ExecutionResult.failure_result(
                message=f"Failed to compare rankings: {str(e)}",
                errors=[str(e)]
            )
    
    async def _analyze_competitor_content(
        self,
        target_url: str,
        competitors: List[str],
    ) -> ExecutionResult:
        """Analyze competitor content strategies."""
        try:
            target_domain = self.extract_domain(target_url)
            
            content_analysis = {
                "target_domain": target_domain,
                "competitor_analysis": {},
                "content_gaps": [],
                "content_opportunities": [],
                "benchmark_metrics": {},
            }
            
            # Analyze each competitor's content
            all_word_counts = []
            all_update_frequencies = []
            
            for competitor in competitors:
                competitor_domain = self.extract_domain(competitor)
                
                # Simulate content analysis
                competitor_data = {
                    "domain": competitor_domain,
                    "content_metrics": {
                        "average_word_count": hash(competitor_domain) % 1000 + 1000,  # 1000-2000
                        "content_freshness": hash(competitor_domain) % 30 + 1,  # Days since update
                        "content_depth_score": hash(competitor_domain) % 30 + 70,  # 70-100
                        "multimedia_usage": hash(competitor_domain) % 40 + 60,  # 60-100%
                    },
                    "content_types": {
                        "blog_posts": hash(f"{competitor_domain}_blog") % 100 + 50,
                        "product_pages": hash(f"{competitor_domain}_products") % 50 + 20,
                        "guides": hash(f"{competitor_domain}_guides") % 30 + 10,
                        "case_studies": hash(f"{competitor_domain}_cases") % 20 + 5,
                    },
                    "content_strategy": {
                        "update_frequency": "weekly" if hash(competitor_domain) % 3 == 0 else "monthly",
                        "content_focus": ["educational", "promotional"][hash(competitor_domain) % 2],
                        "target_audience": "professional" if hash(competitor_domain) % 2 == 0 else "general",
                    },
                }
                
                all_word_counts.append(competitor_data["content_metrics"]["average_word_count"])
                all_update_frequencies.append(competitor_data["content_metrics"]["content_freshness"])
                
                content_analysis["competitor_analysis"][competitor_domain] = competitor_data
            
            # Calculate benchmark metrics
            content_analysis["benchmark_metrics"] = {
                "average_word_count": round(sum(all_word_counts) / len(all_word_counts)) if all_word_counts else 0,
                "average_update_frequency": round(sum(all_update_frequencies) / len(all_update_frequencies)) if all_update_frequencies else 0,
                "content_volume_leader": max(content_analysis["competitor_analysis"].keys(), 
                                           key=lambda x: sum(content_analysis["competitor_analysis"][x]["content_types"].values())) if content_analysis["competitor_analysis"] else "",
            }
            
            # Identify content gaps and opportunities
            content_analysis["content_gaps"] = [
                {
                    "gap_type": "content_depth",
                    "description": "Competitors have longer, more comprehensive content",
                    "recommendation": "Increase average content length and depth",
                },
                {
                    "gap_type": "multimedia_usage",
                    "description": "Competitors use more visual content",
                    "recommendation": "Add more images, videos, and interactive elements",
                },
            ]
            
            content_analysis["content_opportunities"] = [
                {
                    "opportunity": "content_frequency",
                    "description": "Opportunity to publish more frequently than competitors",
                    "potential_impact": "medium",
                },
                {
                    "opportunity": "content_format",
                    "description": "Underutilized content formats in the competitive landscape",
                    "potential_impact": "high",
                },
            ]
            
            return ExecutionResult.success_result(
                message=f"Analyzed content strategies for {len(competitors)} competitors",
                data=content_analysis
            )
            
        except Exception as e:
            return ExecutionResult.failure_result(
                message=f"Failed to analyze competitor content: {str(e)}",
                errors=[str(e)]
            )
    
    async def _analyze_backlinks(
        self,
        target_url: str,
        competitors: List[str],
    ) -> ExecutionResult:
        """Analyze backlink profiles of target and competitors."""
        try:
            target_domain = self.extract_domain(target_url)
            
            backlink_analysis = {
                "target_domain": target_domain,
                "backlink_comparison": {},
                "link_opportunities": [],
                "competitive_insights": {},
            }
            
            # Analyze target's backlink profile
            target_backlinks = {
                "total_backlinks": hash(target_domain) % 10000 + 1000,  # 1000-11000
                "referring_domains": hash(target_domain) % 1000 + 100,  # 100-1100
                "domain_authority": hash(target_domain) % 40 + 40,  # 40-80
                "average_link_quality": hash(target_domain) % 30 + 70,  # 70-100
                "link_growth_rate": hash(target_domain) % 20 + 5,  # 5-25% monthly
            }
            
            backlink_analysis["backlink_comparison"][target_domain] = target_backlinks
            
            # Analyze competitors' backlink profiles
            for competitor in competitors:
                competitor_domain = self.extract_domain(competitor)
                
                competitor_backlinks = {
                    "total_backlinks": hash(competitor_domain) % 15000 + 500,
                    "referring_domains": hash(competitor_domain) % 1500 + 50,
                    "domain_authority": hash(competitor_domain) % 50 + 30,
                    "average_link_quality": hash(competitor_domain) % 40 + 60,
                    "link_growth_rate": hash(competitor_domain) % 25 + 5,
                }
                
                backlink_analysis["backlink_comparison"][competitor_domain] = competitor_backlinks
                
                # Identify link opportunities (domains linking to competitors but not target)
                if competitor_backlinks["domain_authority"] > target_backlinks["domain_authority"]:
                    for i in range(5):  # Simulate 5 link opportunities per competitor
                        opportunity = {
                            "domain": f"linking-domain-{competitor_domain}-{i}.com",
                            "domain_authority": hash(f"link{competitor_domain}{i}") % 50 + 30,
                            "relevance_score": hash(f"rel{competitor_domain}{i}") % 30 + 70,
                            "link_type": ["article", "directory", "resource"][hash(f"type{i}") % 3],
                            "competitor_linked": competitor_domain,
                        }
                        backlink_analysis["link_opportunities"].append(opportunity)
            
            # Generate competitive insights
            best_backlink_profile = max(
                backlink_analysis["backlink_comparison"].items(),
                key=lambda x: x[1]["domain_authority"]
            )
            
            backlink_analysis["competitive_insights"] = {
                "strongest_competitor": best_backlink_profile[0],
                "target_ranking": sorted(
                    backlink_analysis["backlink_comparison"].items(),
                    key=lambda x: x[1]["domain_authority"],
                    reverse=True
                ).index((target_domain, target_backlinks)) + 1,
                "improvement_potential": {
                    "authority_gap": best_backlink_profile[1]["domain_authority"] - target_backlinks["domain_authority"],
                    "link_gap": best_backlink_profile[1]["total_backlinks"] - target_backlinks["total_backlinks"],
                },
            }
            
            return ExecutionResult.success_result(
                message=f"Analyzed backlink profiles and found {len(backlink_analysis['link_opportunities'])} link opportunities",
                data=backlink_analysis
            )
            
        except Exception as e:
            return ExecutionResult.failure_result(
                message=f"Failed to analyze backlinks: {str(e)}",
                errors=[str(e)]
            )
    
    async def _compare_technical_seo(
        self,
        target_url: str,
        competitors: List[str],
    ) -> ExecutionResult:
        """Compare technical SEO factors across competitors."""
        try:
            target_domain = self.extract_domain(target_url)
            
            technical_comparison = {
                "target_domain": target_domain,
                "technical_metrics": {},
                "performance_comparison": {},
                "technical_gaps": [],
                "technical_advantages": [],
            }
            
            all_domains = [target_url] + competitors
            
            for url in all_domains:
                domain = self.extract_domain(url)
                
                # Simulate technical metrics
                metrics = {
                    "page_speed": {
                        "desktop": hash(f"{domain}_desktop") % 40 + 60,  # 60-100
                        "mobile": hash(f"{domain}_mobile") % 40 + 50,    # 50-90
                    },
                    "core_web_vitals": {
                        "lcp": round((hash(f"{domain}_lcp") % 30 + 15) / 10, 1),  # 1.5-4.5s
                        "fid": hash(f"{domain}_fid") % 50 + 50,                    # 50-100ms
                        "cls": round((hash(f"{domain}_cls") % 20) / 100, 2),      # 0.00-0.20
                    },
                    "technical_seo": {
                        "https": hash(f"{domain}_https") % 10 > 1,  # 90% chance
                        "mobile_friendly": hash(f"{domain}_mobile_friendly") % 10 > 0,  # 100% chance
                        "sitemap": hash(f"{domain}_sitemap") % 10 > 1,  # 90% chance
                        "robots_txt": hash(f"{domain}_robots") % 10 > 2,  # 80% chance
                        "structured_data": hash(f"{domain}_structured") % 10 > 3,  # 70% chance
                    },
                    "crawlability": {
                        "crawl_errors": hash(f"{domain}_errors") % 20,  # 0-20 errors
                        "indexability": hash(f"{domain}_index") % 20 + 80,  # 80-100%
                        "internal_linking": hash(f"{domain}_linking") % 30 + 70,  # 70-100 score
                    },
                }
                
                technical_comparison["technical_metrics"][domain] = metrics
            
            # Compare performance
            target_metrics = technical_comparison["technical_metrics"][target_domain]
            
            for competitor in competitors:
                competitor_domain = self.extract_domain(competitor)
                competitor_metrics = technical_comparison["technical_metrics"][competitor_domain]
                
                # Identify gaps where competitor is better
                if competitor_metrics["page_speed"]["desktop"] > target_metrics["page_speed"]["desktop"]:
                    technical_comparison["technical_gaps"].append({
                        "area": "page_speed_desktop",
                        "competitor": competitor_domain,
                        "gap": competitor_metrics["page_speed"]["desktop"] - target_metrics["page_speed"]["desktop"],
                        "recommendation": "Optimize desktop page speed",
                    })
                
                if competitor_metrics["core_web_vitals"]["lcp"] < target_metrics["core_web_vitals"]["lcp"]:
                    technical_comparison["technical_gaps"].append({
                        "area": "largest_contentful_paint",
                        "competitor": competitor_domain,
                        "gap": target_metrics["core_web_vitals"]["lcp"] - competitor_metrics["core_web_vitals"]["lcp"],
                        "recommendation": "Improve Largest Contentful Paint timing",
                    })
                
                # Identify advantages where target is better
                if target_metrics["page_speed"]["mobile"] > competitor_metrics["page_speed"]["mobile"]:
                    technical_comparison["technical_advantages"].append({
                        "area": "mobile_page_speed",
                        "advantage": target_metrics["page_speed"]["mobile"] - competitor_metrics["page_speed"]["mobile"],
                        "competitor": competitor_domain,
                    })
            
            # Calculate overall technical score
            for domain, metrics in technical_comparison["technical_metrics"].items():
                score = 0
                score += metrics["page_speed"]["desktop"] * 0.2
                score += metrics["page_speed"]["mobile"] * 0.3
                score += (5 - metrics["core_web_vitals"]["lcp"]) * 20 * 0.2  # Convert to 0-100 scale
                score += metrics["crawlability"]["indexability"] * 0.3
                
                technical_comparison["performance_comparison"][domain] = round(score, 1)
            
            return ExecutionResult.success_result(
                message=f"Compared technical SEO across {len(all_domains)} domains",
                data=technical_comparison
            )
            
        except Exception as e:
            return ExecutionResult.failure_result(
                message=f"Failed to compare technical SEO: {str(e)}",
                errors=[str(e)]
            )
    
    async def _analyze_serp_features(
        self,
        target_url: str,
        competitors: List[str],
        keywords: List[str],
    ) -> ExecutionResult:
        """Analyze SERP feature presence across competitors."""
        try:
            target_domain = self.extract_domain(target_url)
            
            serp_analysis = {
                "target_domain": target_domain,
                "feature_analysis": {},
                "competitive_serp_presence": {},
                "serp_opportunities": [],
            }
            
            # Define SERP features to analyze
            serp_features = [
                "featured_snippet",
                "local_pack",
                "image_pack",
                "video_results",
                "people_also_ask",
                "knowledge_panel",
                "shopping_results",
            ]
            
            all_domains = [target_domain] + [self.extract_domain(comp) for comp in competitors]
            
            # Initialize feature tracking
            for domain in all_domains:
                serp_analysis["competitive_serp_presence"][domain] = {
                    feature: 0 for feature in serp_features
                }
            
            # Analyze each keyword for SERP features
            for keyword in keywords:
                keyword_features = []
                
                # Simulate SERP feature presence
                for feature in serp_features:
                    if hash(f"{keyword}_{feature}") % 10 < 3:  # 30% chance
                        keyword_features.append(feature)
                        
                        # Determine which domain owns this feature
                        feature_owner = all_domains[hash(f"{keyword}_{feature}_owner") % len(all_domains)]
                        serp_analysis["competitive_serp_presence"][feature_owner][feature] += 1
                
                serp_analysis["feature_analysis"][keyword] = {
                    "features_present": keyword_features,
                    "feature_count": len(keyword_features),
                    "opportunity_level": "high" if len(keyword_features) > 0 else "low",
                }
            
            # Identify SERP opportunities
            target_presence = serp_analysis["competitive_serp_presence"][target_domain]
            
            for feature in serp_features:
                # Find competitors who dominate this feature
                competitor_counts = [
                    (domain, serp_analysis["competitive_serp_presence"][domain][feature])
                    for domain in all_domains
                    if domain != target_domain
                ]
                
                if competitor_counts:
                    best_competitor = max(competitor_counts, key=lambda x: x[1])
                    
                    if best_competitor[1] > target_presence[feature]:
                        serp_analysis["serp_opportunities"].append({
                            "feature": feature,
                            "target_count": target_presence[feature],
                            "competitor_count": best_competitor[1],
                            "leading_competitor": best_competitor[0],
                            "opportunity_score": best_competitor[1] - target_presence[feature],
                            "recommendation": f"Optimize content to capture {feature} opportunities",
                        })
            
            return ExecutionResult.success_result(
                message=f"Analyzed SERP features for {len(keywords)} keywords across {len(all_domains)} domains",
                data=serp_analysis
            )
            
        except Exception as e:
            return ExecutionResult.failure_result(
                message=f"Failed to analyze SERP features: {str(e)}",
                errors=[str(e)]
            )
    
    async def _analyze_market_share(
        self,
        target_url: str,
        competitors: List[str],
        keywords: List[str],
    ) -> ExecutionResult:
        """Analyze market share and visibility metrics."""
        try:
            target_domain = self.extract_domain(target_url)
            
            market_analysis = {
                "target_domain": target_domain,
                "visibility_metrics": {},
                "market_share": {},
                "growth_potential": {},
            }
            
            all_domains = [target_domain] + [self.extract_domain(comp) for comp in competitors]
            
            # Calculate visibility and market share for each domain
            total_visibility = 0
            
            for domain in all_domains:
                # Simulate visibility score based on rankings
                visibility_score = hash(f"{domain}_visibility") % 1000 + 500  # 500-1500
                total_visibility += visibility_score
                
                market_analysis["visibility_metrics"][domain] = {
                    "visibility_score": visibility_score,
                    "estimated_traffic": visibility_score * 10,  # Rough traffic estimate
                    "keyword_positions": {
                        "top_3": hash(f"{domain}_top3") % 10 + 5,  # 5-15 keywords
                        "top_10": hash(f"{domain}_top10") % 20 + 15,  # 15-35 keywords
                        "top_100": hash(f"{domain}_top100") % 50 + 30,  # 30-80 keywords
                    },
                }
            
            # Calculate market share percentages
            for domain in all_domains:
                visibility = market_analysis["visibility_metrics"][domain]["visibility_score"]
                market_share_percent = round((visibility / total_visibility) * 100, 1)
                
                market_analysis["market_share"][domain] = {
                    "share_percentage": market_share_percent,
                    "ranking": 0,  # Will be calculated below
                    "competitive_position": "",
                }
            
            # Rank domains by market share
            sorted_domains = sorted(
                market_analysis["market_share"].items(),
                key=lambda x: x[1]["share_percentage"],
                reverse=True
            )
            
            for i, (domain, data) in enumerate(sorted_domains):
                market_analysis["market_share"][domain]["ranking"] = i + 1
                
                if i == 0:
                    market_analysis["market_share"][domain]["competitive_position"] = "market_leader"
                elif i <= len(sorted_domains) // 3:
                    market_analysis["market_share"][domain]["competitive_position"] = "strong_competitor"
                elif i <= 2 * len(sorted_domains) // 3:
                    market_analysis["market_share"][domain]["competitive_position"] = "emerging_player"
                else:
                    market_analysis["market_share"][domain]["competitive_position"] = "niche_player"
            
            # Calculate growth potential
            target_share = market_analysis["market_share"][target_domain]["share_percentage"]
            leader_share = max(data["share_percentage"] for data in market_analysis["market_share"].values())
            
            market_analysis["growth_potential"] = {
                "current_position": market_analysis["market_share"][target_domain]["ranking"],
                "market_gap": round(leader_share - target_share, 1),
                "growth_opportunity": "high" if target_share < 20 else "medium" if target_share < 35 else "low",
                "potential_traffic_gain": int((leader_share - target_share) / 100 * sum(
                    data["estimated_traffic"] for data in market_analysis["visibility_metrics"].values()
                )),
            }
            
            return ExecutionResult.success_result(
                message=f"Analyzed market share across {len(all_domains)} competitors",
                data=market_analysis
            )
            
        except Exception as e:
            return ExecutionResult.failure_result(
                message=f"Failed to analyze market share: {str(e)}",
                errors=[str(e)]
            )
    
    async def _identify_opportunities(
        self,
        target_url: str,
        competitors: List[str],
        analysis_results: Dict[str, Any],
    ) -> ExecutionResult:
        """Identify competitive opportunities based on all analyses."""
        try:
            target_domain = self.extract_domain(target_url)
            
            opportunities = {
                "keyword_opportunities": [],
                "content_opportunities": [],
                "technical_opportunities": [],
                "link_opportunities": [],
                "serp_opportunities": [],
                "prioritized_actions": [],
            }
            
            # Extract keyword opportunities
            if "keyword_gaps" in analysis_results:
                keyword_data = analysis_results["keyword_gaps"]
                high_value_keywords = [
                    kw for kw in keyword_data.get("opportunity_keywords", [])
                    if kw.get("opportunity_level") == "high"
                ][:10]  # Top 10 high-value opportunities
                
                opportunities["keyword_opportunities"] = [
                    {
                        "keyword": kw["keyword"],
                        "search_volume": kw["search_volume"],
                        "difficulty": kw["difficulty"],
                        "priority": "high",
                        "action": "Create targeted content",
                    }
                    for kw in high_value_keywords
                ]
            
            # Extract content opportunities
            if "content_analysis" in analysis_results:
                content_data = analysis_results["content_analysis"]
                opportunities["content_opportunities"] = content_data.get("content_opportunities", [])
            
            # Extract technical opportunities
            if "technical_comparison" in analysis_results:
                tech_data = analysis_results["technical_comparison"]
                opportunities["technical_opportunities"] = [
                    {
                        "area": gap["area"],
                        "priority": "high" if gap.get("gap", 0) > 10 else "medium",
                        "action": gap["recommendation"],
                        "impact": "performance_improvement",
                    }
                    for gap in tech_data.get("technical_gaps", [])[:5]
                ]
            
            # Extract link opportunities
            if "backlink_analysis" in analysis_results:
                link_data = analysis_results["backlink_analysis"]
                high_value_links = [
                    link for link in link_data.get("link_opportunities", [])
                    if link.get("domain_authority", 0) > 50
                ][:10]
                
                opportunities["link_opportunities"] = [
                    {
                        "domain": link["domain"],
                        "domain_authority": link["domain_authority"],
                        "relevance": link["relevance_score"],
                        "priority": "high" if link["domain_authority"] > 70 else "medium",
                        "action": "Outreach for link building",
                    }
                    for link in high_value_links
                ]
            
            # Extract SERP opportunities
            if "serp_features" in analysis_results:
                serp_data = analysis_results["serp_features"]
                opportunities["serp_opportunities"] = [
                    {
                        "feature": opp["feature"],
                        "opportunity_score": opp["opportunity_score"],
                        "priority": "high" if opp["opportunity_score"] > 5 else "medium",
                        "action": opp["recommendation"],
                    }
                    for opp in serp_data.get("serp_opportunities", [])[:5]
                ]
            
            # Prioritize all opportunities
            all_opportunities = []
            
            # Add all opportunities with scores
            for category, opps in opportunities.items():
                if category != "prioritized_actions":
                    for opp in opps:
                        priority_score = 3 if opp.get("priority") == "high" else 2 if opp.get("priority") == "medium" else 1
                        
                        all_opportunities.append({
                            "category": category,
                            "opportunity": opp,
                            "priority_score": priority_score,
                            "estimated_effort": self._estimate_effort(category, opp),
                            "estimated_impact": self._estimate_impact(category, opp),
                        })
            
            # Sort by priority score and impact/effort ratio
            all_opportunities.sort(
                key=lambda x: (x["priority_score"], x["estimated_impact"] / max(x["estimated_effort"], 1)),
                reverse=True
            )
            
            opportunities["prioritized_actions"] = all_opportunities[:15]  # Top 15 prioritized actions
            
            return ExecutionResult.success_result(
                message=f"Identified {sum(len(opps) for opps in opportunities.values() if isinstance(opps, list))} total opportunities",
                data=opportunities
            )
            
        except Exception as e:
            return ExecutionResult.failure_result(
                message=f"Failed to identify opportunities: {str(e)}",
                errors=[str(e)]
            )
    
    def _estimate_effort(self, category: str, opportunity: Dict[str, Any]) -> int:
        """Estimate effort required for an opportunity (1-5 scale)."""
        effort_map = {
            "keyword_opportunities": 3,  # Medium effort - content creation
            "content_opportunities": 4,  # High effort - comprehensive content work
            "technical_opportunities": 2,  # Low-medium effort - technical fixes
            "link_opportunities": 4,     # High effort - outreach and relationship building
            "serp_opportunities": 3,     # Medium effort - content optimization
        }
        return effort_map.get(category, 3)
    
    def _estimate_impact(self, category: str, opportunity: Dict[str, Any]) -> int:
        """Estimate potential impact of an opportunity (1-5 scale)."""
        impact_map = {
            "keyword_opportunities": 4,  # High impact - direct traffic gain
            "content_opportunities": 3,  # Medium impact - engagement improvement
            "technical_opportunities": 3, # Medium impact - performance boost
            "link_opportunities": 5,     # Very high impact - authority boost
            "serp_opportunities": 4,     # High impact - visibility increase
        }
        
        # Adjust based on opportunity specifics
        base_impact = impact_map.get(category, 3)
        
        if opportunity.get("priority") == "high":
            return min(5, base_impact + 1)
        elif opportunity.get("priority") == "low":
            return max(1, base_impact - 1)
        
        return base_impact
    
    async def _generate_intelligence_report(self, results: Dict[str, Any]) -> ExecutionResult:
        """Generate comprehensive competitive intelligence report."""
        try:
            report = {
                "executive_summary": {
                    "analysis_date": datetime.utcnow().isoformat(),
                    "competitors_analyzed": 0,
                    "total_opportunities": 0,
                    "key_insights": [],
                    "competitive_position": "",
                },
                "competitive_landscape": {},
                "strategic_recommendations": [],
                "action_plan": {
                    "immediate_actions": [],
                    "short_term_goals": [],
                    "long_term_strategy": [],
                },
            }
            
            # Extract summary data
            if "initialization" in results:
                report["executive_summary"]["competitors_analyzed"] = results["initialization"].get("competitor_count", 0)
            
            if "opportunities" in results:
                opportunities_data = results["opportunities"]
                report["executive_summary"]["total_opportunities"] = sum(
                    len(opps) for opps in opportunities_data.values() if isinstance(opps, list)
                )
            
            # Generate key insights
            insights = []
            
            if "keyword_gaps" in results:
                gap_count = results["keyword_gaps"].get("gap_summary", {}).get("total_gaps", 0)
                insights.append(f"Identified {gap_count} keyword gaps with potential for traffic growth")
            
            if "ranking_comparison" in results:
                ranking_data = results["ranking_comparison"]
                win_rate = ranking_data.get("ranking_summary", {}).get("target_wins", 0)
                total_keywords = ranking_data.get("ranking_summary", {}).get("total_keywords", 1)
                win_percentage = round((win_rate / total_keywords) * 100, 1)
                insights.append(f"Currently winning {win_percentage}% of competitive keyword battles")
            
            if "market_share" in results:
                market_data = results["market_share"]
                position = market_data.get("growth_potential", {}).get("current_position", "N/A")
                insights.append(f"Ranked #{position} in competitive market share analysis")
            
            report["executive_summary"]["key_insights"] = insights
            
            # Generate strategic recommendations
            recommendations = [
                {
                    "category": "keyword_strategy",
                    "recommendation": "Focus on high-value keyword gaps with strong search volume",
                    "priority": "high",
                    "timeline": "1-3 months",
                },
                {
                    "category": "content_strategy",
                    "recommendation": "Develop comprehensive content to match competitor depth",
                    "priority": "high",
                    "timeline": "2-6 months",
                },
                {
                    "category": "technical_optimization",
                    "recommendation": "Address technical SEO gaps to improve search performance",
                    "priority": "medium",
                    "timeline": "1-2 months",
                },
                {
                    "category": "link_building",
                    "recommendation": "Target high-authority domains linking to competitors",
                    "priority": "high",
                    "timeline": "3-12 months",
                },
            ]
            
            report["strategic_recommendations"] = recommendations
            
            # Create action plan
            if "opportunities" in results and "prioritized_actions" in results["opportunities"]:
                prioritized = results["opportunities"]["prioritized_actions"]
                
                report["action_plan"]["immediate_actions"] = [
                    action["opportunity"] for action in prioritized[:5]
                    if action.get("estimated_effort", 5) <= 2
                ]
                
                report["action_plan"]["short_term_goals"] = [
                    action["opportunity"] for action in prioritized[5:10]
                    if 2 < action.get("estimated_effort", 5) <= 4
                ]
                
                report["action_plan"]["long_term_strategy"] = [
                    action["opportunity"] for action in prioritized[10:]
                    if action.get("estimated_effort", 5) > 4
                ]
            
            return ExecutionResult.success_result(
                message="Generated comprehensive competitive intelligence report",
                data=report
            )
            
        except Exception as e:
            return ExecutionResult.failure_result(
                message=f"Failed to generate intelligence report: {str(e)}",
                errors=[str(e)]
            )
    
    async def _aggregate_analysis_results(self, results: Dict[str, Any]) -> ExecutionResult:
        """Aggregate all competitor analysis results into final report."""
        try:
            # Calculate success metrics
            successful_steps = sum(1 for result in results.values() if isinstance(result, dict))
            total_steps = len(results)
            success_rate = (successful_steps / total_steps) * 100 if total_steps > 0 else 0
            
            # Count total insights and opportunities
            total_opportunities = 0
            total_insights = 0
            
            if "opportunities" in results and isinstance(results["opportunities"], dict):
                for category, opps in results["opportunities"].items():
                    if isinstance(opps, list):
                        total_opportunities += len(opps)
            
            if "intelligence_report" in results and isinstance(results["intelligence_report"], dict):
                insights = results["intelligence_report"].get("executive_summary", {}).get("key_insights", [])
                total_insights = len(insights)
            
            # Generate final summary
            final_report = {
                "workflow_summary": {
                    "workflow_id": str(self.id),
                    "execution_time": self.get_duration(),
                    "success_rate": round(success_rate, 1),
                    "steps_completed": successful_steps,
                    "total_steps": total_steps,
                },
                "analysis_summary": {
                    "total_opportunities": total_opportunities,
                    "total_insights": total_insights,
                    "analysis_scope": self.analysis_scope,
                    "competitors_analyzed": self.competitor_limit,
                },
                "detailed_results": results,
                "metadata": {
                    "workflow_name": self.name,
                    "execution_timestamp": datetime.utcnow().isoformat(),
                    "configuration": {
                        "analysis_scope": self.analysis_scope,
                        "competitor_limit": self.competitor_limit,
                        "include_content_analysis": self.include_content_analysis,
                        "include_backlink_analysis": self.include_backlink_analysis,
                        "include_technical_analysis": self.include_technical_analysis,
                    },
                },
            }
            
            return ExecutionResult.success_result(
                message=f"Competitor analysis completed with {total_opportunities} opportunities identified",
                data=final_report
            )
            
        except Exception as e:
            return ExecutionResult.failure_result(
                message=f"Failed to aggregate analysis results: {str(e)}",
                errors=[str(e)]
            )