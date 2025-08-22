"""SEO Processor Agent implementation."""

import asyncio
import logging
from datetime import datetime
from statistics import mean, median
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse

from ..knowledge.vector_store import SEOVectorStore
from ..models.base import ExecutionResult, SEOTask, KnowledgeEntry
from ..models.seo import (
    KeywordData,
    RankingData,
    SEOAnalysis,
    ContentOptimization,
    TechnicalAudit,
    SearchEngine,
    KeywordDifficulty,
    ContentType,
)
from .base import BaseSEOAgent, SEOTaskMixin

logger = logging.getLogger(__name__)


class SEOProcessorAgent(BaseSEOAgent, SEOTaskMixin):
    """Agent responsible for processing and analyzing collected SEO data."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the SEO Processor Agent."""
        super().__init__(
            name="SEO Processor",
            description="Processes and analyzes collected SEO data",
            agent_type="seo_processor",
            config=config or {},
        )
        
        # Initialize vector store for knowledge management
        self.vector_store: Optional[SEOVectorStore] = None
        
        # Processing statistics
        self.processing_stats = {
            "tasks_processed": 0,
            "patterns_identified": 0,
            "recommendations_generated": 0,
            "knowledge_entries_created": 0,
        }
        
    async def _get_vector_store(self) -> SEOVectorStore:
        """Get or create vector store instance."""
        if not self.vector_store:
            self.vector_store = SEOVectorStore()
            await self.vector_store.initialize()
        return self.vector_store
    
    def get_supported_task_types(self) -> List[str]:
        """Get list of supported task types."""
        return [
            "data_analysis",
            "pattern_recognition",
            "recommendation_generation",
            "report_compilation",
        ]
    
    async def _execute_task_impl(self, task: SEOTask) -> ExecutionResult:
        """Implement the actual task execution logic."""
        try:
            # Route to appropriate handler based on task type
            if task.task_type == "data_analysis":
                return await self._analyze_seo_data(task)
            elif task.task_type == "pattern_recognition":
                return await self._identify_patterns(task)
            elif task.task_type == "recommendation_generation":
                return await self._generate_recommendations(task)
            elif task.task_type == "report_compilation":
                return await self._compile_report(task)
            else:
                return ExecutionResult.failure_result(
                    message=f"Unsupported task type: {task.task_type}",
                    errors=[f"Task type '{task.task_type}' is not supported by SEO Processor Agent"],
                )
                
        except Exception as e:
            self.logger.exception(f"Unexpected error in task execution: {e}")
            return ExecutionResult.failure_result(
                message="Unexpected error during data processing",
                errors=[str(e)],
            )
    
    async def _analyze_seo_data(self, task: SEOTask) -> ExecutionResult:
        """Analyze collected SEO data."""
        self.logger.info(f"Analyzing SEO data for task: {task.name}")
        
        # Extract parameters
        data_source = task.parameters.get("data_source")  # collector output, vector store, etc.
        analysis_type = task.parameters.get("analysis_type", "comprehensive")
        store_results = task.parameters.get("store_results", True)
        
        if not data_source:
            return ExecutionResult.failure_result(
                message="No data source provided for analysis",
                errors=["Parameter 'data_source' is required"],
            )
        
        analysis_results = {
            "analysis_type": analysis_type,
            "data_source": data_source,
            "processed_at": datetime.utcnow().isoformat(),
            "keyword_analysis": {},
            "ranking_analysis": {},
            "serp_analysis": {},
            "competitor_analysis": {},
            "insights": [],
            "performance_metrics": {},
        }
        
        try:
            # Analyze different types of data based on data_source structure
            if isinstance(data_source, dict):
                # Process keyword data
                if "keyword_data" in data_source:
                    keyword_analysis = await self._process_keyword_data(data_source["keyword_data"])
                    analysis_results["keyword_analysis"] = keyword_analysis
                    
                    # Store keyword insights in vector store if requested
                    if store_results:
                        vector_store = await self._get_vector_store()
                        for keyword_info in data_source["keyword_data"]:
                            if keyword_info.get("keyword"):
                                await vector_store.store_keyword_data(
                                    keyword=keyword_info["keyword"],
                                    keyword_data=keyword_info
                                )
                                self.processing_stats["knowledge_entries_created"] += 1
                
                # Process ranking data
                if "ranking_data" in data_source:
                    ranking_analysis = await self._process_ranking_data(data_source["ranking_data"])
                    analysis_results["ranking_analysis"] = ranking_analysis
                
                # Process SERP data
                if "serp_results" in data_source:
                    serp_analysis = await self._process_serp_data(data_source["serp_results"])
                    analysis_results["serp_analysis"] = serp_analysis
                
                # Process competitor data
                if "competitor_keywords" in data_source or "domain_analytics" in data_source:
                    competitor_analysis = await self._process_competitor_data(data_source)
                    analysis_results["competitor_analysis"] = competitor_analysis
                    
                    # Store competitor insights
                    if store_results and "target_url" in data_source:
                        vector_store = await self._get_vector_store()
                        await vector_store.store_competitor_analysis(
                            target_url=data_source["target_url"],
                            competitor_data=data_source
                        )
                        self.processing_stats["knowledge_entries_created"] += 1
                
                # Generate insights based on analysis
                insights = await self._generate_insights(analysis_results)
                analysis_results["insights"] = insights
                
                # Calculate performance metrics
                performance_metrics = await self._calculate_performance_metrics(analysis_results)
                analysis_results["performance_metrics"] = performance_metrics
            
            else:
                return ExecutionResult.failure_result(
                    message="Invalid data source format",
                    errors=["Data source must be a dictionary with SEO data"],
                )
            
            self.processing_stats["tasks_processed"] += 1
            
            self.logger.info(
                f"Successfully analyzed SEO data: "
                f"{len(analysis_results.get('insights', []))} insights generated"
            )
            
            return ExecutionResult.success_result(
                message=f"Successfully analyzed SEO data ({analysis_type} analysis)",
                data=analysis_results,
            )
            
        except Exception as e:
            self.logger.error(f"Error analyzing SEO data: {e}")
            raise
    
    async def _process_keyword_data(self, keyword_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process keyword research data."""
        if not keyword_data:
            return {}
        
        # Extract metrics
        search_volumes = []
        cpc_values = []
        competition_scores = []
        keyword_difficulties = []
        
        processed_keywords = []
        
        for keyword_info in keyword_data:
            if isinstance(keyword_info, dict):
                # Extract search volume
                if "search_volume" in keyword_info and keyword_info["search_volume"]:
                    search_volumes.append(keyword_info["search_volume"])
                
                # Extract CPC
                if "cpc" in keyword_info and keyword_info["cpc"]:
                    cpc_values.append(keyword_info["cpc"])
                
                # Extract competition
                if "competition" in keyword_info and keyword_info["competition"]:
                    competition_scores.append(keyword_info["competition"])
                
                # Extract difficulty
                if "keyword_difficulty" in keyword_info:
                    keyword_difficulties.append(keyword_info["keyword_difficulty"])
                
                # Store processed keyword info
                processed_keywords.append({
                    "keyword": keyword_info.get("keyword", ""),
                    "search_volume": keyword_info.get("search_volume"),
                    "cpc": keyword_info.get("cpc"),
                    "competition": keyword_info.get("competition"),
                    "difficulty": keyword_info.get("keyword_difficulty"),
                    "potential_score": self._calculate_keyword_potential(keyword_info),
                })
        
        # Calculate statistics
        analysis = {
            "total_keywords": len(keyword_data),
            "processed_keywords": processed_keywords,
            "metrics": {
                "search_volume": {
                    "average": mean(search_volumes) if search_volumes else 0,
                    "median": median(search_volumes) if search_volumes else 0,
                    "min": min(search_volumes) if search_volumes else 0,
                    "max": max(search_volumes) if search_volumes else 0,
                },
                "cpc": {
                    "average": mean(cpc_values) if cpc_values else 0,
                    "median": median(cpc_values) if cpc_values else 0,
                    "min": min(cpc_values) if cpc_values else 0,
                    "max": max(cpc_values) if cpc_values else 0,
                },
                "competition": {
                    "average": mean(competition_scores) if competition_scores else 0,
                    "median": median(competition_scores) if competition_scores else 0,
                },
            },
            "difficulty_distribution": self._analyze_difficulty_distribution(keyword_difficulties),
            "top_opportunities": self._identify_keyword_opportunities(processed_keywords),
        }
        
        return analysis
    
    def _calculate_keyword_potential(self, keyword_info: Dict[str, Any]) -> float:
        """Calculate keyword potential score (0-100)."""
        score = 0.0
        
        # Base score from search volume (30% weight)
        search_volume = keyword_info.get("search_volume", 0)
        if search_volume:
            # Normalize search volume (log scale)
            import math
            volume_score = min(30, (math.log10(search_volume + 1) / 5) * 30)
            score += volume_score
        
        # Competition score (25% weight) - lower competition is better
        competition = keyword_info.get("competition", 1.0)
        if competition is not None:
            competition_score = (1.0 - competition) * 25
            score += competition_score
        
        # CPC value (20% weight) - higher CPC indicates commercial value
        cpc = keyword_info.get("cpc", 0)
        if cpc:
            cpc_score = min(20, (cpc / 5) * 20)  # Normalize against $5 CPC
            score += cpc_score
        
        # Keyword difficulty (25% weight) - easier keywords are better
        difficulty = keyword_info.get("keyword_difficulty")
        if difficulty:
            difficulty_map = {
                "very_easy": 25,
                "easy": 20,
                "medium": 15,
                "hard": 10,
                "very_hard": 5,
            }
            score += difficulty_map.get(difficulty, 10)
        else:
            score += 15  # Default medium score
        
        return min(100, score)
    
    def _analyze_difficulty_distribution(self, difficulties: List[str]) -> Dict[str, int]:
        """Analyze keyword difficulty distribution."""
        distribution = {
            "very_easy": 0,
            "easy": 0,
            "medium": 0,
            "hard": 0,
            "very_hard": 0,
        }
        
        for difficulty in difficulties:
            if difficulty in distribution:
                distribution[difficulty] += 1
        
        return distribution
    
    def _identify_keyword_opportunities(self, keywords: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify top keyword opportunities."""
        # Sort by potential score
        sorted_keywords = sorted(
            keywords,
            key=lambda x: x.get("potential_score", 0),
            reverse=True
        )
        
        # Return top 10 opportunities
        return sorted_keywords[:10]
    
    async def _process_ranking_data(self, ranking_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process ranking position data."""
        if not ranking_data:
            return {}
        
        positions = []
        keywords_ranking = []
        
        for ranking_info in ranking_data:
            if isinstance(ranking_info, dict) and "position" in ranking_info:
                positions.append(ranking_info["position"])
                keywords_ranking.append({
                    "keyword": ranking_info.get("keyword", ""),
                    "position": ranking_info["position"],
                    "url": ranking_info.get("url", ""),
                    "title": ranking_info.get("title", ""),
                })
        
        # Calculate ranking statistics
        analysis = {
            "total_rankings": len(ranking_data),
            "keywords_ranking": keywords_ranking,
            "position_stats": {
                "average_position": mean(positions) if positions else 0,
                "median_position": median(positions) if positions else 0,
                "best_position": min(positions) if positions else 0,
                "worst_position": max(positions) if positions else 0,
            },
            "distribution": {
                "top_3": len([p for p in positions if p <= 3]),
                "top_10": len([p for p in positions if p <= 10]),
                "top_20": len([p for p in positions if p <= 20]),
                "beyond_20": len([p for p in positions if p > 20]),
            },
            "improvement_opportunities": self._identify_ranking_opportunities(keywords_ranking),
        }
        
        return analysis
    
    def _identify_ranking_opportunities(self, rankings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify ranking improvement opportunities."""
        opportunities = []
        
        for ranking in rankings:
            position = ranking.get("position", 100)
            
            # Identify opportunities for improvement
            if 11 <= position <= 20:
                # Keywords on page 2 - good opportunity for page 1
                opportunities.append({
                    **ranking,
                    "opportunity_type": "page_1_potential",
                    "improvement_potential": "high",
                    "target_position": "1-10",
                })
            elif 4 <= position <= 10:
                # Keywords on page 1 but not top 3
                opportunities.append({
                    **ranking,
                    "opportunity_type": "top_3_potential",
                    "improvement_potential": "medium",
                    "target_position": "1-3",
                })
            elif position > 20:
                # Keywords beyond page 2 - need significant work
                opportunities.append({
                    **ranking,
                    "opportunity_type": "major_improvement_needed",
                    "improvement_potential": "low",
                    "target_position": "1-20",
                })
        
        # Sort by improvement potential and current position
        opportunities.sort(key=lambda x: (
            {"high": 0, "medium": 1, "low": 2}[x["improvement_potential"]],
            x["position"]
        ))
        
        return opportunities[:15]  # Top 15 opportunities
    
    async def _process_serp_data(self, serp_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process SERP analysis data."""
        if not serp_data:
            return {}
        
        # Analyze SERP features and results
        organic_results = []
        featured_snippets = []
        local_packs = []
        image_results = []
        video_results = []
        
        for result in serp_data:
            if isinstance(result, dict):
                result_type = result.get("type", "organic")
                
                if result_type == "organic":
                    organic_results.append(result)
                elif result_type == "featured_snippet":
                    featured_snippets.append(result)
                elif result_type == "local_pack":
                    local_packs.append(result)
                elif result_type == "images":
                    image_results.append(result)
                elif result_type == "video":
                    video_results.append(result)
        
        # Analyze organic results
        domains = {}
        for result in organic_results:
            url = result.get("url", "")
            domain = self.extract_domain(url)
            if domain:
                domains[domain] = domains.get(domain, 0) + 1
        
        analysis = {
            "total_results": len(serp_data),
            "organic_results": len(organic_results),
            "serp_features": {
                "featured_snippets": len(featured_snippets),
                "local_packs": len(local_packs),
                "image_results": len(image_results),
                "video_results": len(video_results),
            },
            "domain_distribution": dict(sorted(domains.items(), key=lambda x: x[1], reverse=True)[:10]),
            "content_analysis": self._analyze_serp_content(organic_results),
            "feature_opportunities": self._identify_serp_opportunities(serp_data),
        }
        
        return analysis
    
    def _analyze_serp_content(self, organic_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze content patterns in SERP results."""
        titles = []
        descriptions = []
        title_lengths = []
        desc_lengths = []
        
        for result in organic_results:
            title = result.get("title", "")
            description = result.get("description", "")
            
            if title:
                titles.append(title)
                title_lengths.append(len(title))
            
            if description:
                descriptions.append(description)
                desc_lengths.append(len(description))
        
        return {
            "title_stats": {
                "average_length": mean(title_lengths) if title_lengths else 0,
                "median_length": median(title_lengths) if title_lengths else 0,
                "min_length": min(title_lengths) if title_lengths else 0,
                "max_length": max(title_lengths) if title_lengths else 0,
            },
            "description_stats": {
                "average_length": mean(desc_lengths) if desc_lengths else 0,
                "median_length": median(desc_lengths) if desc_lengths else 0,
                "min_length": min(desc_lengths) if desc_lengths else 0,
                "max_length": max(desc_lengths) if desc_lengths else 0,
            },
            "common_title_patterns": self._extract_common_patterns(titles),
            "common_desc_patterns": self._extract_common_patterns(descriptions),
        }
    
    def _extract_common_patterns(self, texts: List[str]) -> List[str]:
        """Extract common patterns from text content."""
        # Simple pattern extraction - look for common words/phrases
        words = {}
        for text in texts:
            # Simple word extraction (could be enhanced with NLP)
            text_words = text.lower().split()
            for word in text_words:
                if len(word) > 3:  # Skip short words
                    words[word] = words.get(word, 0) + 1
        
        # Return most common words that appear in multiple texts
        common_patterns = [
            word for word, count in words.items()
            if count >= max(2, len(texts) * 0.2)  # At least 20% frequency
        ]
        
        return sorted(common_patterns, key=lambda w: words[w], reverse=True)[:10]
    
    def _identify_serp_opportunities(self, serp_data: List[Dict[str, Any]]) -> List[str]:
        """Identify SERP feature opportunities."""
        opportunities = []
        
        # Check for different SERP features
        has_featured_snippet = any(r.get("type") == "featured_snippet" for r in serp_data)
        has_local_pack = any(r.get("type") == "local_pack" for r in serp_data)
        has_image_pack = any(r.get("type") == "images" for r in serp_data)
        has_video_results = any(r.get("type") == "video" for r in serp_data)
        
        if has_featured_snippet:
            opportunities.append("Featured snippet optimization opportunity")
        if has_local_pack:
            opportunities.append("Local SEO optimization opportunity")
        if has_image_pack:
            opportunities.append("Image optimization opportunity")
        if has_video_results:
            opportunities.append("Video content optimization opportunity")
        
        return opportunities
    
    async def _process_competitor_data(self, competitor_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process competitor analysis data."""
        analysis = {
            "target_url": competitor_data.get("target_url", ""),
            "competitor_count": len(competitor_data.get("competitor_urls", [])),
            "competitor_keywords": {},
            "domain_analytics": {},
            "competitive_gaps": [],
            "strengths_weaknesses": {},
        }
        
        # Process competitor keywords
        if "competitor_keywords" in competitor_data:
            keywords = competitor_data["competitor_keywords"]
            analysis["competitor_keywords"] = {
                "total_keywords": len(keywords),
                "top_keywords": keywords[:20] if keywords else [],
                "keyword_categories": self._categorize_competitor_keywords(keywords),
            }
        
        # Process domain analytics
        if "domain_analytics" in competitor_data:
            analytics = competitor_data["domain_analytics"]
            analysis["domain_analytics"] = self._analyze_domain_metrics(analytics)
        
        # Identify competitive gaps and opportunities
        analysis["competitive_gaps"] = self._identify_competitive_gaps(competitor_data)
        analysis["strengths_weaknesses"] = self._analyze_competitive_position(competitor_data)
        
        return analysis
    
    def _categorize_competitor_keywords(self, keywords: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Categorize competitor keywords by type/intent."""
        categories = {
            "high_volume": [],
            "commercial": [],
            "informational": [],
            "branded": [],
            "long_tail": [],
        }
        
        for keyword_info in keywords:
            keyword = keyword_info.get("keyword", "")
            search_volume = keyword_info.get("search_volume", 0)
            
            if not keyword:
                continue
            
            # High volume keywords
            if search_volume > 10000:
                categories["high_volume"].append(keyword)
            
            # Commercial intent keywords
            commercial_terms = ["buy", "price", "cost", "cheap", "deal", "discount", "review"]
            if any(term in keyword.lower() for term in commercial_terms):
                categories["commercial"].append(keyword)
            
            # Informational keywords
            info_terms = ["how", "what", "why", "guide", "tutorial", "tips"]
            if any(term in keyword.lower() for term in info_terms):
                categories["informational"].append(keyword)
            
            # Long tail keywords (3+ words)
            if len(keyword.split()) >= 3:
                categories["long_tail"].append(keyword)
        
        # Limit each category to top 10
        return {k: v[:10] for k, v in categories.items()}
    
    def _analyze_domain_metrics(self, analytics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze domain analytics data."""
        # This would process domain authority, backlinks, traffic, etc.
        # Simplified for this implementation
        return {
            "domains_analyzed": len(analytics),
            "metrics_summary": analytics,  # Would be processed further in real implementation
        }
    
    def _identify_competitive_gaps(self, competitor_data: Dict[str, Any]) -> List[str]:
        """Identify competitive gaps and opportunities."""
        gaps = []
        
        # Analyze competitor keywords vs target
        competitor_keywords = competitor_data.get("competitor_keywords", [])
        if competitor_keywords:
            # Look for high-value keywords competitors rank for
            high_value_keywords = [
                kw for kw in competitor_keywords
                if kw.get("search_volume", 0) > 5000
            ]
            
            if high_value_keywords:
                gaps.append(f"Competitors ranking for {len(high_value_keywords)} high-volume keywords")
        
        # Add more gap analysis logic here
        gaps.append("Content gap analysis needed")
        gaps.append("Technical SEO comparison required")
        
        return gaps
    
    def _analyze_competitive_position(self, competitor_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Analyze competitive strengths and weaknesses."""
        return {
            "strengths": [
                "Need more data for detailed analysis",
                "Current data provides foundation for comparison",
            ],
            "weaknesses": [
                "Limited competitive intelligence",
                "Need more comprehensive competitor data",
            ],
            "opportunities": [
                "Expand competitor keyword tracking",
                "Implement content gap analysis",
                "Monitor competitor backlink strategies",
            ],
        }
    
    async def _generate_insights(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Generate insights from analysis results."""
        insights = []
        
        # Keyword insights
        keyword_analysis = analysis_results.get("keyword_analysis", {})
        if keyword_analysis:
            metrics = keyword_analysis.get("metrics", {})
            volume_stats = metrics.get("search_volume", {})
            
            if volume_stats.get("average", 0) > 0:
                insights.append(
                    f"Average search volume is {volume_stats['average']:.0f} with "
                    f"maximum opportunity of {volume_stats['max']:.0f} searches/month"
                )
            
            opportunities = keyword_analysis.get("top_opportunities", [])
            if opportunities:
                top_keyword = opportunities[0]
                insights.append(
                    f"Top keyword opportunity: '{top_keyword.get('keyword', '')}' "
                    f"(potential score: {top_keyword.get('potential_score', 0):.1f})"
                )
        
        # Ranking insights
        ranking_analysis = analysis_results.get("ranking_analysis", {})
        if ranking_analysis:
            position_stats = ranking_analysis.get("position_stats", {})
            distribution = ranking_analysis.get("distribution", {})
            
            if position_stats.get("average_position"):
                insights.append(
                    f"Average ranking position is {position_stats['average_position']:.1f} "
                    f"with {distribution.get('top_10', 0)} keywords in top 10"
                )
            
            opportunities = ranking_analysis.get("improvement_opportunities", [])
            if opportunities:
                high_potential = [o for o in opportunities if o.get("improvement_potential") == "high"]
                insights.append(
                    f"{len(high_potential)} keywords have high improvement potential for page 1"
                )
        
        # SERP insights
        serp_analysis = analysis_results.get("serp_analysis", {})
        if serp_analysis:
            features = serp_analysis.get("serp_features", {})
            opportunities = serp_analysis.get("feature_opportunities", [])
            
            if opportunities:
                insights.append(f"SERP opportunities identified: {', '.join(opportunities)}")
        
        # Competitor insights
        competitor_analysis = analysis_results.get("competitor_analysis", {})
        if competitor_analysis:
            gaps = competitor_analysis.get("competitive_gaps", [])
            if gaps:
                insights.append(f"Competitive analysis reveals: {gaps[0]}")
        
        return insights
    
    async def _calculate_performance_metrics(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall performance metrics."""
        metrics = {
            "overall_score": 0.0,
            "keyword_performance": 0.0,
            "ranking_performance": 0.0,
            "serp_performance": 0.0,
            "competitive_performance": 0.0,
        }
        
        scores = []
        
        # Keyword performance score
        keyword_analysis = analysis_results.get("keyword_analysis", {})
        if keyword_analysis:
            opportunities = keyword_analysis.get("top_opportunities", [])
            if opportunities:
                avg_potential = mean([kw.get("potential_score", 0) for kw in opportunities[:5]])
                metrics["keyword_performance"] = avg_potential
                scores.append(avg_potential)
        
        # Ranking performance score
        ranking_analysis = analysis_results.get("ranking_analysis", {})
        if ranking_analysis:
            distribution = ranking_analysis.get("distribution", {})
            total_rankings = ranking_analysis.get("total_rankings", 1)
            
            # Calculate ranking score based on distribution
            top_10_ratio = distribution.get("top_10", 0) / total_rankings
            ranking_score = top_10_ratio * 100
            metrics["ranking_performance"] = ranking_score
            scores.append(ranking_score)
        
        # SERP performance score
        serp_analysis = analysis_results.get("serp_analysis", {})
        if serp_analysis:
            features = serp_analysis.get("serp_features", {})
            feature_count = sum(features.values())
            # Score based on SERP feature presence (more features = more opportunities)
            serp_score = min(100, feature_count * 20)
            metrics["serp_performance"] = serp_score
            scores.append(serp_score)
        
        # Overall score
        if scores:
            metrics["overall_score"] = mean(scores)
        
        return metrics
    
    async def _identify_patterns(self, task: SEOTask) -> ExecutionResult:
        """Identify SEO patterns and trends."""
        self.logger.info(f"Identifying patterns for task: {task.name}")
        
        # Extract parameters
        data_source = task.parameters.get("data_source")
        pattern_types = task.parameters.get("pattern_types", ["keyword", "ranking", "content"])
        time_range = task.parameters.get("time_range", "30d")
        
        if not data_source:
            return ExecutionResult.failure_result(
                message="No data source provided for pattern recognition",
                errors=["Parameter 'data_source' is required"],
            )
        
        try:
            vector_store = await self._get_vector_store()
            
            patterns_identified = {
                "pattern_types": pattern_types,
                "time_range": time_range,
                "identified_at": datetime.utcnow().isoformat(),
                "keyword_patterns": [],
                "ranking_patterns": [],
                "content_patterns": [],
                "seasonal_patterns": [],
                "competitive_patterns": [],
            }
            
            # Identify keyword patterns
            if "keyword" in pattern_types:
                keyword_patterns = await self._identify_keyword_patterns(vector_store)
                patterns_identified["keyword_patterns"] = keyword_patterns
            
            # Identify ranking patterns
            if "ranking" in pattern_types:
                ranking_patterns = await self._identify_ranking_patterns(vector_store)
                patterns_identified["ranking_patterns"] = ranking_patterns
            
            # Identify content patterns
            if "content" in pattern_types:
                content_patterns = await self._identify_content_patterns(vector_store)
                patterns_identified["content_patterns"] = content_patterns
            
            self.processing_stats["patterns_identified"] += len(
                patterns_identified["keyword_patterns"] +
                patterns_identified["ranking_patterns"] +
                patterns_identified["content_patterns"]
            )
            
            self.logger.info(f"Successfully identified {self.processing_stats['patterns_identified']} patterns")
            
            return ExecutionResult.success_result(
                message=f"Successfully identified patterns ({len(pattern_types)} types analyzed)",
                data=patterns_identified,
            )
            
        except Exception as e:
            self.logger.error(f"Error identifying patterns: {e}")
            raise
    
    async def _identify_keyword_patterns(self, vector_store: SEOVectorStore) -> List[Dict[str, Any]]:
        """Identify keyword-related patterns."""
        patterns = []
        
        # Query for keyword-related knowledge
        keyword_entries = await vector_store.query_knowledge(
            query="keyword research search volume competition",
            n_results=50,
            tags=["keyword_research"]
        )
        
        if keyword_entries:
            # Analyze for patterns (simplified)
            patterns.append({
                "pattern_type": "keyword_volume_trend",
                "description": f"Analyzed {len(keyword_entries)} keyword entries",
                "confidence": 0.8,
                "details": "Pattern analysis based on historical keyword data",
            })
        
        return patterns
    
    async def _identify_ranking_patterns(self, vector_store: SEOVectorStore) -> List[Dict[str, Any]]:
        """Identify ranking-related patterns."""
        patterns = []
        
        # This would analyze ranking trends over time
        patterns.append({
            "pattern_type": "ranking_volatility",
            "description": "Ranking position volatility analysis",
            "confidence": 0.7,
            "details": "Need more historical data for comprehensive analysis",
        })
        
        return patterns
    
    async def _identify_content_patterns(self, vector_store: SEOVectorStore) -> List[Dict[str, Any]]:
        """Identify content-related patterns."""
        patterns = []
        
        # Query for SEO analysis entries
        seo_entries = await vector_store.query_knowledge(
            query="seo analysis content title meta description",
            n_results=30,
            tags=["seo_analysis"]
        )
        
        if seo_entries:
            patterns.append({
                "pattern_type": "content_structure",
                "description": f"Content patterns from {len(seo_entries)} analyzed pages",
                "confidence": 0.8,
                "details": "Title and meta description optimization patterns identified",
            })
        
        return patterns
    
    async def _generate_recommendations(self, task: SEOTask) -> ExecutionResult:
        """Generate SEO optimization recommendations."""
        self.logger.info(f"Generating recommendations for task: {task.name}")
        
        # Extract parameters
        analysis_data = task.parameters.get("analysis_data")
        recommendation_types = task.parameters.get("recommendation_types", ["keyword", "content", "technical"])
        priority_level = task.parameters.get("priority_level", "all")
        
        if not analysis_data:
            return ExecutionResult.failure_result(
                message="No analysis data provided for recommendations",
                errors=["Parameter 'analysis_data' is required"],
            )
        
        try:
            recommendations = {
                "recommendation_types": recommendation_types,
                "priority_level": priority_level,
                "generated_at": datetime.utcnow().isoformat(),
                "keyword_recommendations": [],
                "content_recommendations": [],
                "technical_recommendations": [],
                "competitive_recommendations": [],
                "quick_wins": [],
                "long_term_strategies": [],
            }
            
            # Generate keyword recommendations
            if "keyword" in recommendation_types:
                keyword_recs = await self._generate_keyword_recommendations(analysis_data)
                recommendations["keyword_recommendations"] = keyword_recs
            
            # Generate content recommendations
            if "content" in recommendation_types:
                content_recs = await self._generate_content_recommendations(analysis_data)
                recommendations["content_recommendations"] = content_recs
            
            # Generate technical recommendations
            if "technical" in recommendation_types:
                technical_recs = await self._generate_technical_recommendations(analysis_data)
                recommendations["technical_recommendations"] = technical_recs
            
            # Categorize by implementation timeline
            all_recs = (
                recommendations["keyword_recommendations"] +
                recommendations["content_recommendations"] +
                recommendations["technical_recommendations"]
            )
            
            recommendations["quick_wins"] = [r for r in all_recs if r.get("effort", "medium") == "low"]
            recommendations["long_term_strategies"] = [r for r in all_recs if r.get("effort", "medium") == "high"]
            
            self.processing_stats["recommendations_generated"] += len(all_recs)
            
            self.logger.info(f"Successfully generated {len(all_recs)} recommendations")
            
            return ExecutionResult.success_result(
                message=f"Successfully generated {len(all_recs)} SEO recommendations",
                data=recommendations,
            )
            
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {e}")
            raise
    
    async def _generate_keyword_recommendations(self, analysis_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate keyword-specific recommendations."""
        recommendations = []
        
        keyword_analysis = analysis_data.get("keyword_analysis", {})
        if keyword_analysis:
            opportunities = keyword_analysis.get("top_opportunities", [])
            
            for opportunity in opportunities[:5]:  # Top 5 opportunities
                keyword = opportunity.get("keyword", "")
                potential_score = opportunity.get("potential_score", 0)
                
                recommendations.append({
                    "type": "keyword_optimization",
                    "title": f"Target high-potential keyword: {keyword}",
                    "description": f"Focus on keyword '{keyword}' with potential score of {potential_score:.1f}",
                    "priority": "high" if potential_score > 70 else "medium",
                    "effort": "medium",
                    "impact": "high" if potential_score > 70 else "medium",
                    "action_items": [
                        f"Create content targeting '{keyword}'",
                        f"Optimize existing pages for '{keyword}'",
                        f"Build internal links with '{keyword}' anchor text",
                    ],
                })
        
        return recommendations
    
    async def _generate_content_recommendations(self, analysis_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate content-specific recommendations."""
        recommendations = []
        
        serp_analysis = analysis_data.get("serp_analysis", {})
        if serp_analysis:
            opportunities = serp_analysis.get("feature_opportunities", [])
            
            for opportunity in opportunities:
                if "featured snippet" in opportunity.lower():
                    recommendations.append({
                        "type": "content_optimization",
                        "title": "Optimize for featured snippets",
                        "description": "Structure content to target featured snippet opportunities",
                        "priority": "high",
                        "effort": "medium",
                        "impact": "high",
                        "action_items": [
                            "Use question-based headings",
                            "Provide concise, direct answers",
                            "Use structured formatting (lists, tables)",
                            "Target 40-60 word answer snippets",
                        ],
                    })
        
        # Add general content recommendations
        recommendations.append({
            "type": "content_optimization",
            "title": "Improve content depth and quality",
            "description": "Enhance content comprehensiveness and user value",
            "priority": "medium",
            "effort": "high",
            "impact": "high",
            "action_items": [
                "Conduct content gap analysis",
                "Add more comprehensive sections",
                "Include relevant internal links",
                "Update outdated information",
            ],
        })
        
        return recommendations
    
    async def _generate_technical_recommendations(self, analysis_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate technical SEO recommendations."""
        recommendations = []
        
        # Add standard technical recommendations
        recommendations.extend([
            {
                "type": "technical_seo",
                "title": "Improve page loading speed",
                "description": "Optimize Core Web Vitals and page performance",
                "priority": "high",
                "effort": "medium",
                "impact": "high",
                "action_items": [
                    "Optimize images and implement lazy loading",
                    "Minimize CSS and JavaScript",
                    "Enable compression and caching",
                    "Optimize server response times",
                ],
            },
            {
                "type": "technical_seo",
                "title": "Enhance mobile usability",
                "description": "Ensure optimal mobile user experience",
                "priority": "high",
                "effort": "medium",
                "impact": "high",
                "action_items": [
                    "Implement responsive design",
                    "Optimize mobile page speed",
                    "Ensure touch-friendly navigation",
                    "Test mobile usability regularly",
                ],
            },
        ])
        
        return recommendations
    
    async def _compile_report(self, task: SEOTask) -> ExecutionResult:
        """Compile comprehensive SEO analysis report."""
        self.logger.info(f"Compiling report for task: {task.name}")
        
        # Extract parameters
        analysis_data = task.parameters.get("analysis_data")
        recommendations = task.parameters.get("recommendations")
        patterns = task.parameters.get("patterns")
        report_format = task.parameters.get("format", "comprehensive")
        
        if not analysis_data:
            return ExecutionResult.failure_result(
                message="No analysis data provided for report compilation",
                errors=["Parameter 'analysis_data' is required"],
            )
        
        try:
            report = {
                "report_format": report_format,
                "generated_at": datetime.utcnow().isoformat(),
                "executive_summary": {},
                "detailed_analysis": analysis_data,
                "recommendations": recommendations or [],
                "patterns": patterns or [],
                "action_plan": {},
                "performance_metrics": {},
                "appendices": {},
            }
            
            # Generate executive summary
            report["executive_summary"] = await self._generate_executive_summary(
                analysis_data, recommendations, patterns
            )
            
            # Generate action plan
            report["action_plan"] = await self._generate_action_plan(recommendations or [])
            
            # Extract performance metrics
            report["performance_metrics"] = analysis_data.get("performance_metrics", {})
            
            # Add appendices with raw data
            report["appendices"] = {
                "data_sources": "SEO Collector Agent",
                "analysis_methods": "SEO Processor Agent automated analysis",
                "report_version": "1.0",
            }
            
            self.logger.info("Successfully compiled comprehensive SEO report")
            
            return ExecutionResult.success_result(
                message="Successfully compiled SEO analysis report",
                data=report,
            )
            
        except Exception as e:
            self.logger.error(f"Error compiling report: {e}")
            raise
    
    async def _generate_executive_summary(
        self,
        analysis_data: Dict[str, Any],
        recommendations: Optional[List[Dict[str, Any]]],
        patterns: Optional[List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """Generate executive summary for the report."""
        summary = {
            "overall_performance": "needs_assessment",
            "key_findings": [],
            "priority_actions": [],
            "estimated_impact": "medium",
        }
        
        # Analyze overall performance
        performance_metrics = analysis_data.get("performance_metrics", {})
        overall_score = performance_metrics.get("overall_score", 0)
        
        if overall_score > 80:
            summary["overall_performance"] = "excellent"
        elif overall_score > 60:
            summary["overall_performance"] = "good"
        elif overall_score > 40:
            summary["overall_performance"] = "needs_improvement"
        else:
            summary["overall_performance"] = "poor"
        
        # Extract key findings
        insights = analysis_data.get("insights", [])
        summary["key_findings"] = insights[:5]  # Top 5 insights
        
        # Extract priority actions from recommendations
        if recommendations:
            high_priority = [r for r in recommendations if r.get("priority") == "high"]
            summary["priority_actions"] = [r["title"] for r in high_priority[:3]]
        
        return summary
    
    async def _generate_action_plan(self, recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate prioritized action plan."""
        action_plan = {
            "immediate_actions": [],  # 0-2 weeks
            "short_term_actions": [],  # 2-8 weeks
            "long_term_actions": [],  # 2+ months
            "ongoing_monitoring": [],
        }
        
        for rec in recommendations:
            effort = rec.get("effort", "medium")
            priority = rec.get("priority", "medium")
            
            action_item = {
                "title": rec.get("title", ""),
                "description": rec.get("description", ""),
                "action_items": rec.get("action_items", []),
                "priority": priority,
                "estimated_effort": effort,
            }
            
            # Categorize by timeline
            if priority == "high" and effort == "low":
                action_plan["immediate_actions"].append(action_item)
            elif effort == "medium":
                action_plan["short_term_actions"].append(action_item)
            else:
                action_plan["long_term_actions"].append(action_item)
        
        # Add ongoing monitoring tasks
        action_plan["ongoing_monitoring"] = [
            "Monitor keyword rankings weekly",
            "Track Core Web Vitals monthly",
            "Review competitor activities monthly",
            "Update content quarterly",
        ]
        
        return action_plan
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get agent performance metrics."""
        base_metrics = await super().get_metrics()
        
        # Add processor-specific metrics
        processor_metrics = {
            "processing_stats": self.processing_stats,
            "vector_store_status": "connected" if self.vector_store else "disconnected",
            "supported_task_types": len(self.get_supported_task_types()),
        }
        
        base_metrics.update(processor_metrics)
        return base_metrics
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check."""
        health_info = await super().health_check()
        
        # Check vector store connectivity
        vector_store_status = "unknown"
        try:
            if self.vector_store:
                stats = await self.vector_store.get_collection_stats()
                vector_store_status = f"connected ({stats.get('total_entries', 0)} entries)"
            else:
                vector_store_status = "not_initialized"
        except Exception as e:
            vector_store_status = f"error: {str(e)}"
        
        health_info.update({
            "vector_store_status": vector_store_status,
            "processing_stats": self.processing_stats,
            "supported_tasks": self.get_supported_task_types(),
        })
        
        return health_info
    
    async def shutdown(self) -> None:
        """Gracefully shutdown the agent."""
        self.logger.info("Shutting down SEO Processor Agent")
        
        # Close vector store connection
        if self.vector_store:
            await self.vector_store.close()
        
        # Clear processing stats
        self.processing_stats = {
            "tasks_processed": 0,
            "patterns_identified": 0,
            "recommendations_generated": 0,
            "knowledge_entries_created": 0,
        }
        
        await super().shutdown()