"""SEO Collector Agent implementation."""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from ..models.base import ExecutionResult, SEOTask
from ..models.seo import KeywordData, RankingData, SearchEngine
from ..tools.dataforseo_client import (
    DataForSEOClient,
    DataForSEOError,
    AuthenticationError,
    RateLimitError,
    InsufficientCreditsError,
)
from .base import BaseSEOAgent, SEOTaskMixin

logger = logging.getLogger(__name__)


class SEOCollectorAgent(BaseSEOAgent, SEOTaskMixin):
    """Agent responsible for collecting SEO data from Data for SEO APIs."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the SEO Collector Agent."""
        super().__init__(
            name="SEO Collector",
            description="Collects SEO data from Data for SEO APIs",
            agent_type="seo_collector",
            config=config or {},
        )
        
        # Initialize Data for SEO client
        object.__setattr__(self, 'client', None)
        
        # Cache for recent results to avoid duplicate API calls
        object.__setattr__(self, '_cache', {})
        object.__setattr__(self, '_cache_ttl', self.settings.cache_ttl)
        
    async def _get_client(self) -> DataForSEOClient:
        """Get or create Data for SEO client."""
        if not self.client:
            self.client = DataForSEOClient(
                username=self.settings.dataforseo_username,
                password=self.settings.dataforseo_password
            )
        return self.client
    
    def get_supported_task_types(self) -> List[str]:
        """Get list of supported task types."""
        return [
            "keyword_research",
            "serp_analysis", 
            "ranking_data",
            "competitor_analysis",
        ]
    
    async def _execute_task_impl(self, task: SEOTask) -> ExecutionResult:
        """Implement the actual task execution logic."""
        try:
            # Route to appropriate handler based on task type
            if task.task_type == "keyword_research":
                return await self._collect_keyword_data(task)
            elif task.task_type == "serp_analysis":
                return await self._collect_serp_data(task)
            elif task.task_type == "ranking_data":
                return await self._collect_ranking_data(task)
            elif task.task_type == "competitor_analysis":
                return await self._collect_competitor_data(task)
            else:
                return ExecutionResult.failure_result(
                    message=f"Unsupported task type: {task.task_type}",
                    errors=[f"Task type '{task.task_type}' is not supported by SEO Collector Agent"],
                )
                
        except AuthenticationError as e:
            self.logger.error(f"Authentication error: {e}")
            return ExecutionResult.failure_result(
                message="Data for SEO authentication failed",
                errors=[str(e)],
            )
        except InsufficientCreditsError as e:
            self.logger.error(f"Insufficient credits: {e}")
            return ExecutionResult.failure_result(
                message="Insufficient Data for SEO API credits",
                errors=[str(e)],
            )
        except RateLimitError as e:
            self.logger.warning(f"Rate limit exceeded: {e}")
            return ExecutionResult.failure_result(
                message="Data for SEO API rate limit exceeded",
                errors=[str(e)],
            )
        except DataForSEOError as e:
            self.logger.error(f"Data for SEO API error: {e}")
            return ExecutionResult.failure_result(
                message="Data for SEO API error",
                errors=[str(e)],
            )
        except Exception as e:
            self.logger.exception(f"Unexpected error in task execution: {e}")
            return ExecutionResult.failure_result(
                message="Unexpected error during data collection",
                errors=[str(e)],
            )
    
    async def _collect_keyword_data(self, task: SEOTask) -> ExecutionResult:
        """Collect keyword research data."""
        self.logger.info(f"Collecting keyword data for task: {task.name}")
        
        # Extract parameters
        keywords = task.parameters.get("keywords", [])
        location = task.parameters.get("location", self.settings.default_location)
        language = task.parameters.get("language", self.settings.default_language)
        include_metrics = task.parameters.get("include_metrics", True)
        include_ideas = task.parameters.get("include_ideas", True)
        
        if not keywords:
            return ExecutionResult.failure_result(
                message="No keywords provided for research",
                errors=["Parameter 'keywords' is required and cannot be empty"],
            )
        
        # Validate keywords
        invalid_keywords = [kw for kw in keywords if not self.validate_keyword(kw)]
        if invalid_keywords:
            return ExecutionResult.failure_result(
                message="Invalid keywords provided",
                errors=[f"Invalid keywords: {invalid_keywords}"],
            )
        
        collected_data = {
            "keywords": keywords,
            "location": location,
            "language": language,
            "keyword_data": [],
            "keyword_ideas": [],
            "collected_at": datetime.utcnow().isoformat(),
        }
        
        try:
            client = await self._get_client()
            
            async with client:
                # Collect keyword metrics if requested
                if include_metrics:
                    self.logger.debug(f"Collecting metrics for {len(keywords)} keywords")
                    metrics_response = await client.get_keyword_metrics(
                        keywords=keywords,
                        location=location,
                        language=language
                    )
                    
                    # Process metrics response
                    if metrics_response.get("tasks"):
                        for task_data in metrics_response["tasks"]:
                            if task_data.get("result"):
                                for keyword_info in task_data["result"]:
                                    if keyword_info.get("keyword_data"):
                                        collected_data["keyword_data"].extend(
                                            keyword_info["keyword_data"]
                                        )
                
                # Collect keyword ideas if requested
                if include_ideas:
                    self.logger.debug(f"Collecting ideas for {len(keywords)} keywords")
                    ideas_response = await client.get_keyword_ideas(
                        keywords=keywords,
                        location=location,
                        language=language
                    )
                    
                    # Process ideas response
                    if ideas_response.get("tasks"):
                        for task_data in ideas_response["tasks"]:
                            if task_data.get("result"):
                                for keyword_info in task_data["result"]:
                                    if keyword_info.get("items"):
                                        collected_data["keyword_ideas"].extend(
                                            keyword_info["items"]
                                        )
            
            # Cache the results
            cache_key = f"keyword_research:{':'.join(keywords)}:{location}:{language}"
            self._cache[cache_key] = {
                "data": collected_data,
                "timestamp": datetime.utcnow()
            }
            
            self.logger.info(
                f"Successfully collected data for {len(keywords)} keywords: "
                f"{len(collected_data['keyword_data'])} metrics, "
                f"{len(collected_data['keyword_ideas'])} ideas"
            )
            
            return ExecutionResult.success_result(
                message=f"Successfully collected keyword data for {len(keywords)} keywords",
                data=collected_data,
            )
            
        except Exception as e:
            self.logger.error(f"Error collecting keyword data: {e}")
            raise
    
    async def _collect_serp_data(self, task: SEOTask) -> ExecutionResult:
        """Collect SERP (Search Engine Results Page) analysis data."""
        self.logger.info(f"Collecting SERP data for task: {task.name}")
        
        # Extract parameters
        keyword = task.parameters.get("keyword")
        location = task.parameters.get("location", self.settings.default_location)
        language = task.parameters.get("language", self.settings.default_language)
        device = task.parameters.get("device", "desktop")
        
        if not keyword:
            return ExecutionResult.failure_result(
                message="No keyword provided for SERP analysis",
                errors=["Parameter 'keyword' is required"],
            )
        
        if not self.validate_keyword(keyword):
            return ExecutionResult.failure_result(
                message="Invalid keyword provided",
                errors=[f"Keyword '{keyword}' is not valid"],
            )
        
        collected_data = {
            "keyword": keyword,
            "location": location,
            "language": language,
            "device": device,
            "serp_results": [],
            "features": {},
            "collected_at": datetime.utcnow().isoformat(),
        }
        
        try:
            client = await self._get_client()
            
            async with client:
                self.logger.debug(f"Collecting SERP data for keyword: {keyword}")
                serp_response = await client.get_serp_data(
                    keyword=keyword,
                    location=location,
                    language=language,
                    device=device
                )
                
                # Process SERP response
                if serp_response.get("tasks"):
                    for task_data in serp_response["tasks"]:
                        if task_data.get("result"):
                            for serp_info in task_data["result"]:
                                if serp_info.get("items"):
                                    collected_data["serp_results"] = serp_info["items"]
                                
                                # Extract SERP features
                                collected_data["features"] = {
                                    "featured_snippet": any(
                                        item.get("type") == "featured_snippet" 
                                        for item in serp_info.get("items", [])
                                    ),
                                    "local_pack": any(
                                        item.get("type") == "local_pack" 
                                        for item in serp_info.get("items", [])
                                    ),
                                    "image_pack": any(
                                        item.get("type") == "images" 
                                        for item in serp_info.get("items", [])
                                    ),
                                    "video_results": any(
                                        item.get("type") == "video" 
                                        for item in serp_info.get("items", [])
                                    ),
                                    "total_results": len(serp_info.get("items", [])),
                                }
            
            # Cache the results
            cache_key = f"serp_analysis:{keyword}:{location}:{language}:{device}"
            self._cache[cache_key] = {
                "data": collected_data,
                "timestamp": datetime.utcnow()
            }
            
            results_count = len(collected_data["serp_results"])
            self.logger.info(f"Successfully collected SERP data: {results_count} results")
            
            return ExecutionResult.success_result(
                message=f"Successfully collected SERP data for '{keyword}' ({results_count} results)",
                data=collected_data,
            )
            
        except Exception as e:
            self.logger.error(f"Error collecting SERP data: {e}")
            raise
    
    async def _collect_ranking_data(self, task: SEOTask) -> ExecutionResult:
        """Collect ranking position data."""
        self.logger.info(f"Collecting ranking data for task: {task.name}")
        
        # Extract parameters
        keywords = task.parameters.get("keywords", [])
        target_url = task.parameters.get("target_url")
        location = task.parameters.get("location", self.settings.default_location)
        language = task.parameters.get("language", self.settings.default_language)
        
        if not keywords:
            return ExecutionResult.failure_result(
                message="No keywords provided for ranking analysis",
                errors=["Parameter 'keywords' is required and cannot be empty"],
            )
        
        if not target_url:
            return ExecutionResult.failure_result(
                message="No target URL provided for ranking analysis",
                errors=["Parameter 'target_url' is required"],
            )
        
        # Validate URL
        try:
            parsed_url = urlparse(target_url)
            if not parsed_url.netloc:
                raise ValueError("Invalid URL format")
        except Exception:
            return ExecutionResult.failure_result(
                message="Invalid target URL provided",
                errors=[f"URL '{target_url}' is not valid"],
            )
        
        # Validate keywords
        invalid_keywords = [kw for kw in keywords if not self.validate_keyword(kw)]
        if invalid_keywords:
            return ExecutionResult.failure_result(
                message="Invalid keywords provided",
                errors=[f"Invalid keywords: {invalid_keywords}"],
            )
        
        collected_data = {
            "keywords": keywords,
            "target_url": target_url,
            "location": location,
            "language": language,
            "ranking_data": [],
            "collected_at": datetime.utcnow().isoformat(),
        }
        
        try:
            client = await self._get_client()
            
            async with client:
                self.logger.debug(f"Collecting ranking data for {len(keywords)} keywords")
                ranking_response = await client.get_ranking_data(
                    keywords=keywords,
                    target_url=target_url,
                    location=location,
                    language=language
                )
                
                # Process ranking response
                if ranking_response.get("tasks"):
                    for task_data in ranking_response["tasks"]:
                        if task_data.get("result"):
                            for ranking_info in task_data["result"]:
                                if ranking_info.get("items"):
                                    # Extract ranking positions for our target URL
                                    for item in ranking_info["items"]:
                                        if item.get("type") == "organic":
                                            for result in item.get("items", []):
                                                if target_url in result.get("url", ""):
                                                    ranking_data = {
                                                        "keyword": ranking_info.get("keyword"),
                                                        "position": result.get("rank_group"),
                                                        "url": result.get("url"),
                                                        "title": result.get("title"),
                                                        "description": result.get("description"),
                                                        "timestamp": datetime.utcnow().isoformat(),
                                                    }
                                                    collected_data["ranking_data"].append(ranking_data)
            
            # Cache the results
            cache_key = f"ranking_data:{':'.join(keywords)}:{target_url}:{location}"
            self._cache[cache_key] = {
                "data": collected_data,
                "timestamp": datetime.utcnow()
            }
            
            rankings_found = len(collected_data["ranking_data"])
            self.logger.info(f"Successfully collected ranking data: {rankings_found} positions found")
            
            return ExecutionResult.success_result(
                message=f"Successfully collected ranking data ({rankings_found} positions found)",
                data=collected_data,
            )
            
        except Exception as e:
            self.logger.error(f"Error collecting ranking data: {e}")
            raise
    
    async def _collect_competitor_data(self, task: SEOTask) -> ExecutionResult:
        """Collect competitor analysis data."""
        self.logger.info(f"Collecting competitor data for task: {task.name}")
        
        # Extract parameters
        target_url = task.parameters.get("target_url")
        competitor_urls = task.parameters.get("competitor_urls", [])
        location = task.parameters.get("location", self.settings.default_location)
        language = task.parameters.get("language", self.settings.default_language)
        include_keywords = task.parameters.get("include_keywords", True)
        include_analytics = task.parameters.get("include_analytics", True)
        
        if not target_url:
            return ExecutionResult.failure_result(
                message="No target URL provided for competitor analysis",
                errors=["Parameter 'target_url' is required"],
            )
        
        # Validate URLs
        all_urls = [target_url] + competitor_urls
        for url in all_urls:
            try:
                parsed_url = urlparse(url)
                if not parsed_url.netloc:
                    raise ValueError("Invalid URL format")
            except Exception:
                return ExecutionResult.failure_result(
                    message="Invalid URL provided",
                    errors=[f"URL '{url}' is not valid"],
                )
        
        collected_data = {
            "target_url": target_url,
            "competitor_urls": competitor_urls,
            "location": location,
            "language": language,
            "competitor_keywords": [],
            "domain_analytics": {},
            "collected_at": datetime.utcnow().isoformat(),
        }
        
        try:
            client = await self._get_client()
            
            async with client:
                # Collect competitor keywords if requested
                if include_keywords:
                    self.logger.debug("Collecting competitor keywords")
                    domain = self.extract_domain(target_url)
                    if domain:
                        keywords_response = await client.get_competitor_keywords(
                            target_url=target_url,
                            location=location,
                            language=language
                        )
                        
                        # Process competitor keywords response
                        if keywords_response.get("tasks"):
                            for task_data in keywords_response["tasks"]:
                                if task_data.get("result"):
                                    for competitor_info in task_data["result"]:
                                        if competitor_info.get("items"):
                                            collected_data["competitor_keywords"].extend(
                                                competitor_info["items"]
                                            )
                
                # Collect domain analytics if requested
                if include_analytics:
                    self.logger.debug("Collecting domain analytics")
                    for url in all_urls:
                        domain = self.extract_domain(url)
                        if domain:
                            analytics_response = await client.get_domain_analytics(
                                domain=domain,
                                location=location,
                                language=language
                            )
                            
                            # Process domain analytics response
                            if analytics_response.get("tasks"):
                                for task_data in analytics_response["tasks"]:
                                    if task_data.get("result"):
                                        collected_data["domain_analytics"][domain] = task_data["result"]
            
            # Cache the results
            cache_key = f"competitor_analysis:{target_url}:{':'.join(competitor_urls)}"
            self._cache[cache_key] = {
                "data": collected_data,
                "timestamp": datetime.utcnow()
            }
            
            keywords_found = len(collected_data["competitor_keywords"])
            domains_analyzed = len(collected_data["domain_analytics"])
            
            self.logger.info(
                f"Successfully collected competitor data: "
                f"{keywords_found} competitor keywords, {domains_analyzed} domains analyzed"
            )
            
            return ExecutionResult.success_result(
                message=f"Successfully collected competitor data ({keywords_found} keywords, {domains_analyzed} domains)",
                data=collected_data,
            )
            
        except Exception as e:
            self.logger.error(f"Error collecting competitor data: {e}")
            raise
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get agent performance metrics."""
        base_metrics = await super().get_metrics()
        
        # Add collector-specific metrics
        collector_metrics = {
            "cache_size": len(self._cache),
            "supported_task_types": len(self.get_supported_task_types()),
            "api_client_status": "connected" if self.client else "disconnected",
        }
        
        base_metrics.update(collector_metrics)
        return base_metrics
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check."""
        health_info = await super().health_check()
        
        # Check Data for SEO API connectivity
        api_status = "unknown"
        try:
            if self.settings.dataforseo_username and self.settings.dataforseo_password:
                # Simple API test - this would ideally be a lightweight endpoint
                api_status = "configured"
            else:
                api_status = "not_configured"
        except Exception as e:
            api_status = f"error: {str(e)}"
        
        health_info.update({
            "api_status": api_status,
            "cache_size": len(self._cache),
            "supported_tasks": self.get_supported_task_types(),
        })
        
        return health_info
    
    async def shutdown(self) -> None:
        """Gracefully shutdown the agent."""
        self.logger.info("Shutting down SEO Collector Agent")
        
        # Close Data for SEO client if initialized
        if self.client and hasattr(self.client, 'session') and self.client.session:
            await self.client.session.close()
        
        # Clear cache
        self._cache.clear()
        
        await super().shutdown()