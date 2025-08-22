"""SEO Analyzer Agent - Performs comprehensive SEO analysis."""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin, urlparse

import aiohttp
from bs4 import BeautifulSoup

from ..models.base import ExecutionResult, SEOTask
from ..models.seo import SEOAnalysis, AuditSeverity
from .base import BaseSEOAgent, SEOTaskMixin

logger = logging.getLogger(__name__)


class SEOAnalyzerAgent(BaseSEOAgent, SEOTaskMixin):
    """Agent responsible for performing comprehensive SEO analysis."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the SEO Analyzer Agent."""
        super().__init__(
            name="SEO Analyzer",
            description="Performs comprehensive SEO analysis including content, technical, and performance metrics",
            agent_type="seo_analyzer",
            config=config or {},
        )
    
    def get_supported_task_types(self) -> List[str]:
        """Get supported task types."""
        return [
            "seo_analysis",
            "page_analysis", 
            "content_analysis",
            "technical_analysis",
            "performance_analysis",
        ]
    
    async def _execute_task_impl(self, task: SEOTask) -> ExecutionResult:
        """Execute SEO analysis task."""
        task_type = task.task_type
        
        if task_type == "seo_analysis":
            return await self._perform_comprehensive_analysis(task)
        elif task_type == "page_analysis":
            return await self._analyze_single_page(task)
        elif task_type == "content_analysis":
            return await self._analyze_content(task)
        elif task_type == "technical_analysis":
            return await self._analyze_technical_seo(task)
        elif task_type == "performance_analysis":
            return await self._analyze_performance(task)
        else:
            return ExecutionResult.failure_result(
                message=f"Unsupported task type: {task_type}",
                errors=[f"Task type '{task_type}' is not supported by SEO Analyzer"],
            )
    
    async def _perform_comprehensive_analysis(self, task: SEOTask) -> ExecutionResult:
        """Perform comprehensive SEO analysis."""
        try:
            url = task.parameters.get("url")
            if not url:
                return ExecutionResult.failure_result(
                    message="URL parameter is required for SEO analysis",
                    errors=["Missing 'url' parameter"],
                )
            
            if not self.validate_url(url):
                return ExecutionResult.failure_result(
                    message=f"Invalid URL format: {url}",
                    errors=["URL validation failed"],
                )
            
            self.logger.info(f"Starting comprehensive SEO analysis for: {url}")
            
            # Fetch and parse the page
            page_data = await self._fetch_page_data(url)
            if not page_data:
                return ExecutionResult.failure_result(
                    message=f"Failed to fetch page data for: {url}",
                    errors=["Page fetch failed"],
                )
            
            # Perform various analyses
            content_analysis = await self._extract_content_metrics(page_data, url)
            technical_analysis = await self._extract_technical_metrics(page_data, url)
            performance_metrics = await self._extract_performance_metrics(url)
            
            # Create comprehensive analysis result
            analysis = SEOAnalysis(
                url=url,
                title=content_analysis.get("title"),
                meta_description=content_analysis.get("meta_description"),
                word_count=content_analysis.get("word_count"),
                heading_structure=content_analysis.get("heading_structure", {}),
                keyword_density=content_analysis.get("keyword_density", {}),
                page_load_time=performance_metrics.get("page_load_time"),
                mobile_friendly=technical_analysis.get("mobile_friendly"),
                https_enabled=technical_analysis.get("https_enabled", False),
                internal_links=technical_analysis.get("internal_links", 0),
                external_links=technical_analysis.get("external_links", 0),
                broken_links=technical_analysis.get("broken_links", []),
                images_count=technical_analysis.get("images_count", 0),
                images_without_alt=technical_analysis.get("images_without_alt", 0),
                schema_markup=technical_analysis.get("schema_markup", []),
                seo_score=self._calculate_seo_score(content_analysis, technical_analysis, performance_metrics),
                content_score=self._calculate_content_score(content_analysis),
                technical_score=self._calculate_technical_score(technical_analysis),
            )
            
            return ExecutionResult.success_result(
                message=f"SEO analysis completed for {url}",
                data={
                    "analysis": analysis.model_dump(),
                    "recommendations": self._generate_recommendations(analysis),
                },
            )
            
        except Exception as e:
            self.logger.exception(f"Error during comprehensive SEO analysis: {e}")
            return ExecutionResult.failure_result(
                message=f"SEO analysis failed: {str(e)}",
                errors=[str(e)],
            )
    
    async def _analyze_single_page(self, task: SEOTask) -> ExecutionResult:
        """Analyze a single page for basic SEO metrics."""
        try:
            url = task.parameters.get("url")
            if not url or not self.validate_url(url):
                return ExecutionResult.failure_result(
                    message="Valid URL parameter is required",
                    errors=["Invalid or missing URL"],
                )
            
            page_data = await self._fetch_page_data(url)
            if not page_data:
                return ExecutionResult.failure_result(
                    message="Failed to fetch page data",
                    errors=["Page fetch failed"],
                )
            
            # Extract basic metrics
            soup = BeautifulSoup(page_data["content"], "html.parser")
            
            analysis_data = {
                "url": url,
                "title": self._extract_title(soup),
                "meta_description": self._extract_meta_description(soup),
                "word_count": self._count_words(soup),
                "headings": self._extract_headings(soup),
                "images": self._analyze_images(soup),
                "links": self._analyze_links(soup, url),
                "status_code": page_data.get("status_code"),
                "response_time": page_data.get("response_time"),
            }
            
            return ExecutionResult.success_result(
                message=f"Page analysis completed for {url}",
                data=analysis_data,
            )
            
        except Exception as e:
            self.logger.exception(f"Error during page analysis: {e}")
            return ExecutionResult.failure_result(
                message=f"Page analysis failed: {str(e)}",
                errors=[str(e)],
            )
    
    async def _analyze_content(self, task: SEOTask) -> ExecutionResult:
        """Analyze content-specific SEO metrics."""
        try:
            url = task.parameters.get("url")
            target_keywords = task.parameters.get("target_keywords", [])
            
            if not url or not self.validate_url(url):
                return ExecutionResult.failure_result(
                    message="Valid URL parameter is required",
                    errors=["Invalid or missing URL"],
                )
            
            page_data = await self._fetch_page_data(url)
            if not page_data:
                return ExecutionResult.failure_result(
                    message="Failed to fetch page data",
                    errors=["Page fetch failed"],
                )
            
            soup = BeautifulSoup(page_data["content"], "html.parser")
            
            # Content analysis
            content_metrics = {
                "title_analysis": self._analyze_title_seo(soup, target_keywords),
                "meta_description_analysis": self._analyze_meta_description_seo(soup, target_keywords),
                "content_structure": self._analyze_content_structure(soup),
                "keyword_analysis": self._analyze_keyword_usage(soup, target_keywords),
                "readability": self._analyze_readability(soup),
                "content_quality": self._analyze_content_quality(soup),
            }
            
            return ExecutionResult.success_result(
                message=f"Content analysis completed for {url}",
                data=content_metrics,
            )
            
        except Exception as e:
            self.logger.exception(f"Error during content analysis: {e}")
            return ExecutionResult.failure_result(
                message=f"Content analysis failed: {str(e)}",
                errors=[str(e)],
            )
    
    async def _analyze_technical_seo(self, task: SEOTask) -> ExecutionResult:
        """Analyze technical SEO aspects."""
        try:
            url = task.parameters.get("url")
            
            if not url or not self.validate_url(url):
                return ExecutionResult.failure_result(
                    message="Valid URL parameter is required",
                    errors=["Invalid or missing URL"],
                )
            
            # Technical analysis
            technical_metrics = {
                "https_check": self._check_https(url),
                "robots_txt": await self._check_robots_txt(url),
                "sitemap": await self._check_sitemap(url),
                "canonical_tags": await self._check_canonical_tags(url),
                "meta_robots": await self._check_meta_robots(url),
                "structured_data": await self._check_structured_data(url),
                "mobile_friendly": await self._check_mobile_friendly(url),
            }
            
            return ExecutionResult.success_result(
                message=f"Technical SEO analysis completed for {url}",
                data=technical_metrics,
            )
            
        except Exception as e:
            self.logger.exception(f"Error during technical analysis: {e}")
            return ExecutionResult.failure_result(
                message=f"Technical analysis failed: {str(e)}",
                errors=[str(e)],
            )
    
    async def _analyze_performance(self, task: SEOTask) -> ExecutionResult:
        """Analyze performance metrics."""
        try:
            url = task.parameters.get("url")
            
            if not url or not self.validate_url(url):
                return ExecutionResult.failure_result(
                    message="Valid URL parameter is required",
                    errors=["Invalid or missing URL"],
                )
            
            # Performance analysis (basic implementation)
            start_time = datetime.utcnow()
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response_time = (datetime.utcnow() - start_time).total_seconds()
                    content_length = len(await response.read())
            
            performance_metrics = {
                "response_time": response_time,
                "content_size": content_length,
                "status_code": response.status,
                "performance_score": self._calculate_performance_score(response_time, content_length),
            }
            
            return ExecutionResult.success_result(
                message=f"Performance analysis completed for {url}",
                data=performance_metrics,
            )
            
        except Exception as e:
            self.logger.exception(f"Error during performance analysis: {e}")
            return ExecutionResult.failure_result(
                message=f"Performance analysis failed: {str(e)}",
                errors=[str(e)],
            )
    
    # Helper methods
    
    async def _fetch_page_data(self, url: str) -> Optional[Dict[str, Any]]:
        """Fetch page data including content and metadata."""
        try:
            start_time = datetime.utcnow()
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url,
                    headers={"User-Agent": self.settings.user_agent},
                    timeout=aiohttp.ClientTimeout(total=self.settings.request_timeout),
                ) as response:
                    content = await response.text()
                    response_time = (datetime.utcnow() - start_time).total_seconds()
                    
                    return {
                        "content": content,
                        "status_code": response.status,
                        "headers": dict(response.headers),
                        "response_time": response_time,
                        "url": str(response.url),
                    }
        except Exception as e:
            self.logger.error(f"Failed to fetch page data for {url}: {e}")
            return None
    
    async def _extract_content_metrics(self, page_data: Dict[str, Any], url: str) -> Dict[str, Any]:
        """Extract content-related metrics."""
        soup = BeautifulSoup(page_data["content"], "html.parser")
        
        return {
            "title": self._extract_title(soup),
            "meta_description": self._extract_meta_description(soup),
            "word_count": self._count_words(soup),
            "heading_structure": self._extract_heading_structure(soup),
            "keyword_density": self._calculate_keyword_density(soup),
        }
    
    async def _extract_technical_metrics(self, page_data: Dict[str, Any], url: str) -> Dict[str, Any]:
        """Extract technical SEO metrics."""
        soup = BeautifulSoup(page_data["content"], "html.parser")
        
        return {
            "https_enabled": url.startswith("https://"),
            "mobile_friendly": self._check_viewport_meta(soup),
            "internal_links": len(self._get_internal_links(soup, url)),
            "external_links": len(self._get_external_links(soup, url)),
            "broken_links": [],  # Would need additional checking
            "images_count": len(soup.find_all("img")),
            "images_without_alt": len([img for img in soup.find_all("img") if not img.get("alt")]),
            "schema_markup": self._extract_schema_markup(soup),
        }
    
    async def _extract_performance_metrics(self, url: str) -> Dict[str, Any]:
        """Extract performance metrics."""
        # Basic performance metrics - would integrate with actual performance tools
        return {
            "page_load_time": None,  # Would measure actual load time
            "first_contentful_paint": None,
            "largest_contentful_paint": None,
        }
    
    def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract page title."""
        title_tag = soup.find("title")
        return title_tag.get_text().strip() if title_tag else None
    
    def _extract_meta_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract meta description."""
        meta_desc = soup.find("meta", attrs={"name": "description"})
        return meta_desc.get("content", "").strip() if meta_desc else None
    
    def _count_words(self, soup: BeautifulSoup) -> int:
        """Count words in the main content."""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        words = text.split()
        return len(words)
    
    def _extract_heading_structure(self, soup: BeautifulSoup) -> Dict[str, int]:
        """Extract heading structure."""
        headings = {}
        for i in range(1, 7):
            headings[f"h{i}"] = len(soup.find_all(f"h{i}"))
        return headings
    
    def _calculate_keyword_density(self, soup: BeautifulSoup) -> Dict[str, float]:
        """Calculate keyword density (basic implementation)."""
        # This is a simplified implementation
        text = soup.get_text().lower()
        words = text.split()
        total_words = len(words)
        
        if total_words == 0:
            return {}
        
        # Count word frequency
        word_count = {}
        for word in words:
            word = word.strip(".,!?;:")
            if len(word) > 3:  # Only count words longer than 3 characters
                word_count[word] = word_count.get(word, 0) + 1
        
        # Calculate density for top words
        density = {}
        for word, count in sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:10]:
            density[word] = (count / total_words) * 100
        
        return density
    
    def _calculate_seo_score(self, content: Dict, technical: Dict, performance: Dict) -> float:
        """Calculate overall SEO score."""
        score = 0.0
        
        # Content score (40% weight)
        content_score = self._calculate_content_score(content)
        score += content_score * 0.4
        
        # Technical score (40% weight)
        technical_score = self._calculate_technical_score(technical)
        score += technical_score * 0.4
        
        # Performance score (20% weight)
        performance_score = self._calculate_performance_score(
            performance.get("page_load_time", 3.0),
            performance.get("content_size", 1000000)
        )
        score += performance_score * 0.2
        
        return min(100.0, max(0.0, score))
    
    def _calculate_content_score(self, content: Dict) -> float:
        """Calculate content quality score."""
        score = 0.0
        
        # Title check
        if content.get("title"):
            score += 20
            if 30 <= len(content["title"]) <= 60:
                score += 10
        
        # Meta description check
        if content.get("meta_description"):
            score += 15
            if 120 <= len(content["meta_description"]) <= 160:
                score += 10
        
        # Word count check
        word_count = content.get("word_count", 0)
        if word_count >= 300:
            score += 20
        elif word_count >= 150:
            score += 10
        
        # Heading structure
        headings = content.get("heading_structure", {})
        if headings.get("h1", 0) == 1:
            score += 15
        if headings.get("h2", 0) > 0:
            score += 10
        
        return min(100.0, score)
    
    def _calculate_technical_score(self, technical: Dict) -> float:
        """Calculate technical SEO score."""
        score = 0.0
        
        # HTTPS check
        if technical.get("https_enabled"):
            score += 20
        
        # Mobile friendly check
        if technical.get("mobile_friendly"):
            score += 20
        
        # Images with alt text
        images_count = technical.get("images_count", 0)
        images_without_alt = technical.get("images_without_alt", 0)
        if images_count > 0:
            alt_ratio = (images_count - images_without_alt) / images_count
            score += alt_ratio * 20
        
        # Internal linking
        if technical.get("internal_links", 0) > 0:
            score += 15
        
        # Schema markup
        if technical.get("schema_markup"):
            score += 25
        
        return min(100.0, score)
    
    def _calculate_performance_score(self, response_time: float, content_size: int) -> float:
        """Calculate performance score."""
        score = 100.0
        
        # Response time penalty
        if response_time > 3.0:
            score -= 30
        elif response_time > 2.0:
            score -= 20
        elif response_time > 1.0:
            score -= 10
        
        # Content size penalty
        if content_size > 2000000:  # 2MB
            score -= 20
        elif content_size > 1000000:  # 1MB
            score -= 10
        
        return max(0.0, score)
    
    def _generate_recommendations(self, analysis: SEOAnalysis) -> List[Dict[str, Any]]:
        """Generate SEO recommendations based on analysis."""
        recommendations = []
        
        # Title recommendations
        if not analysis.title:
            recommendations.append({
                "type": "title",
                "priority": "high",
                "message": "Add a title tag to the page",
                "description": "Every page should have a unique, descriptive title tag.",
            })
        elif len(analysis.title) > 60:
            recommendations.append({
                "type": "title",
                "priority": "medium",
                "message": "Title tag is too long",
                "description": "Keep title tags under 60 characters for better display in search results.",
            })
        
        # Meta description recommendations
        if not analysis.meta_description:
            recommendations.append({
                "type": "meta_description",
                "priority": "high",
                "message": "Add a meta description",
                "description": "Meta descriptions help search engines understand your page content.",
            })
        elif len(analysis.meta_description) > 160:
            recommendations.append({
                "type": "meta_description",
                "priority": "medium",
                "message": "Meta description is too long",
                "description": "Keep meta descriptions under 160 characters.",
            })
        
        # Content recommendations
        if analysis.word_count and analysis.word_count < 300:
            recommendations.append({
                "type": "content",
                "priority": "medium",
                "message": "Content is too short",
                "description": "Consider adding more comprehensive content (300+ words).",
            })
        
        # Technical recommendations
        if not analysis.https_enabled:
            recommendations.append({
                "type": "security",
                "priority": "high",
                "message": "Enable HTTPS",
                "description": "HTTPS is a ranking factor and improves user trust.",
            })
        
        if analysis.images_without_alt > 0:
            recommendations.append({
                "type": "accessibility",
                "priority": "medium",
                "message": f"{analysis.images_without_alt} images missing alt text",
                "description": "Add descriptive alt text to all images for accessibility and SEO.",
            })
        
        return recommendations
    
    # Additional helper methods for specific checks
    
    def _check_https(self, url: str) -> bool:
        """Check if URL uses HTTPS."""
        return url.startswith("https://")
    
    async def _check_robots_txt(self, url: str) -> Dict[str, Any]:
        """Check robots.txt file."""
        try:
            domain = self.extract_domain(url)
            robots_url = f"https://{domain}/robots.txt"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(robots_url) as response:
                    if response.status == 200:
                        content = await response.text()
                        return {
                            "exists": True,
                            "accessible": True,
                            "content_length": len(content),
                        }
                    else:
                        return {"exists": False, "accessible": False}
        except Exception:
            return {"exists": False, "accessible": False}
    
    async def _check_sitemap(self, url: str) -> Dict[str, Any]:
        """Check XML sitemap."""
        try:
            domain = self.extract_domain(url)
            sitemap_url = f"https://{domain}/sitemap.xml"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(sitemap_url) as response:
                    if response.status == 200:
                        return {"exists": True, "accessible": True}
                    else:
                        return {"exists": False, "accessible": False}
        except Exception:
            return {"exists": False, "accessible": False}
    
    async def _check_canonical_tags(self, url: str) -> Dict[str, Any]:
        """Check canonical tags."""
        page_data = await self._fetch_page_data(url)
        if not page_data:
            return {"has_canonical": False}
        
        soup = BeautifulSoup(page_data["content"], "html.parser")
        canonical = soup.find("link", rel="canonical")
        
        return {
            "has_canonical": canonical is not None,
            "canonical_url": canonical.get("href") if canonical else None,
        }
    
    async def _check_meta_robots(self, url: str) -> Dict[str, Any]:
        """Check meta robots tags."""
        page_data = await self._fetch_page_data(url)
        if not page_data:
            return {"has_meta_robots": False}
        
        soup = BeautifulSoup(page_data["content"], "html.parser")
        meta_robots = soup.find("meta", attrs={"name": "robots"})
        
        return {
            "has_meta_robots": meta_robots is not None,
            "robots_content": meta_robots.get("content") if meta_robots else None,
        }
    
    async def _check_structured_data(self, url: str) -> Dict[str, Any]:
        """Check for structured data."""
        page_data = await self._fetch_page_data(url)
        if not page_data:
            return {"has_structured_data": False}
        
        soup = BeautifulSoup(page_data["content"], "html.parser")
        
        # Check for JSON-LD
        json_ld = soup.find_all("script", type="application/ld+json")
        
        # Check for microdata
        microdata = soup.find_all(attrs={"itemscope": True})
        
        return {
            "has_structured_data": len(json_ld) > 0 or len(microdata) > 0,
            "json_ld_count": len(json_ld),
            "microdata_count": len(microdata),
        }
    
    async def _check_mobile_friendly(self, url: str) -> Dict[str, Any]:
        """Check mobile-friendly indicators."""
        page_data = await self._fetch_page_data(url)
        if not page_data:
            return {"mobile_friendly": False}
        
        soup = BeautifulSoup(page_data["content"], "html.parser")
        
        # Check viewport meta tag
        viewport = soup.find("meta", attrs={"name": "viewport"})
        has_viewport = viewport is not None
        
        # Check responsive design indicators
        has_media_queries = "@media" in page_data["content"]
        
        return {
            "mobile_friendly": has_viewport and has_media_queries,
            "has_viewport": has_viewport,
            "has_media_queries": has_media_queries,
        }
    
    def _check_viewport_meta(self, soup: BeautifulSoup) -> bool:
        """Check if page has viewport meta tag."""
        viewport = soup.find("meta", attrs={"name": "viewport"})
        return viewport is not None
    
    def _get_internal_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Get internal links from the page."""
        domain = self.extract_domain(base_url)
        internal_links = []
        
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if href.startswith("/") or domain in href:
                internal_links.append(href)
        
        return internal_links
    
    def _get_external_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Get external links from the page."""
        domain = self.extract_domain(base_url)
        external_links = []
        
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if href.startswith("http") and domain not in href:
                external_links.append(href)
        
        return external_links
    
    def _extract_schema_markup(self, soup: BeautifulSoup) -> List[str]:
        """Extract schema markup types."""
        schema_types = []
        
        # JSON-LD schema
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                import json
                data = json.loads(script.string)
                if isinstance(data, dict) and "@type" in data:
                    schema_types.append(data["@type"])
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and "@type" in item:
                            schema_types.append(item["@type"])
            except Exception:
                continue
        
        # Microdata schema
        for element in soup.find_all(attrs={"itemtype": True}):
            itemtype = element.get("itemtype", "")
            if "schema.org" in itemtype:
                schema_type = itemtype.split("/")[-1]
                schema_types.append(schema_type)
        
        return list(set(schema_types))
    
    def _extract_headings(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """Extract all headings from the page."""
        headings = {}
        for i in range(1, 7):
            tag = f"h{i}"
            headings[tag] = [h.get_text().strip() for h in soup.find_all(tag)]
        return headings
    
    def _analyze_images(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze images on the page."""
        images = soup.find_all("img")
        
        return {
            "total_count": len(images),
            "without_alt": len([img for img in images if not img.get("alt")]),
            "without_src": len([img for img in images if not img.get("src")]),
            "with_lazy_loading": len([img for img in images if img.get("loading") == "lazy"]),
        }
    
    def _analyze_links(self, soup: BeautifulSoup, base_url: str) -> Dict[str, Any]:
        """Analyze links on the page."""
        links = soup.find_all("a", href=True)
        domain = self.extract_domain(base_url)
        
        internal_links = []
        external_links = []
        
        for link in links:
            href = link["href"]
            if href.startswith("/") or (domain and domain in href):
                internal_links.append(href)
            elif href.startswith("http"):
                external_links.append(href)
        
        return {
            "total_count": len(links),
            "internal_count": len(internal_links),
            "external_count": len(external_links),
            "internal_links": internal_links[:10],  # First 10 for brevity
            "external_links": external_links[:10],  # First 10 for brevity
        }
    
    def _analyze_title_seo(self, soup: BeautifulSoup, target_keywords: List[str]) -> Dict[str, Any]:
        """Analyze title tag for SEO."""
        title = self._extract_title(soup)
        
        if not title:
            return {"has_title": False, "length": 0, "keyword_present": False}
        
        keyword_present = any(keyword.lower() in title.lower() for keyword in target_keywords)
        
        return {
            "has_title": True,
            "title": title,
            "length": len(title),
            "optimal_length": 30 <= len(title) <= 60,
            "keyword_present": keyword_present,
            "target_keywords": target_keywords,
        }
    
    def _analyze_meta_description_seo(self, soup: BeautifulSoup, target_keywords: List[str]) -> Dict[str, Any]:
        """Analyze meta description for SEO."""
        meta_desc = self._extract_meta_description(soup)
        
        if not meta_desc:
            return {"has_meta_description": False, "length": 0, "keyword_present": False}
        
        keyword_present = any(keyword.lower() in meta_desc.lower() for keyword in target_keywords)
        
        return {
            "has_meta_description": True,
            "meta_description": meta_desc,
            "length": len(meta_desc),
            "optimal_length": 120 <= len(meta_desc) <= 160,
            "keyword_present": keyword_present,
            "target_keywords": target_keywords,
        }
    
    def _analyze_content_structure(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze content structure."""
        headings = self._extract_headings(soup)
        
        return {
            "heading_structure": headings,
            "has_h1": len(headings.get("h1", [])) > 0,
            "h1_count": len(headings.get("h1", [])),
            "has_proper_hierarchy": self._check_heading_hierarchy(headings),
            "paragraphs": len(soup.find_all("p")),
            "lists": len(soup.find_all(["ul", "ol"])),
        }
    
    def _check_heading_hierarchy(self, headings: Dict[str, List[str]]) -> bool:
        """Check if heading hierarchy is proper."""
        # Simple check: H1 should exist and be unique
        h1_count = len(headings.get("h1", []))
        return h1_count == 1
    
    def _analyze_keyword_usage(self, soup: BeautifulSoup, target_keywords: List[str]) -> Dict[str, Any]:
        """Analyze keyword usage throughout the page."""
        if not target_keywords:
            return {"target_keywords": [], "keyword_density": {}, "keyword_placement": {}}
        
        text = soup.get_text().lower()
        title = self._extract_title(soup)
        meta_desc = self._extract_meta_description(soup)
        
        keyword_analysis = {}
        
        for keyword in target_keywords:
            keyword_lower = keyword.lower()
            
            # Count occurrences
            text_count = text.count(keyword_lower)
            
            # Check placement
            in_title = title and keyword_lower in title.lower()
            in_meta_desc = meta_desc and keyword_lower in meta_desc.lower()
            
            # Check in headings
            in_headings = False
            for heading_list in self._extract_headings(soup).values():
                if any(keyword_lower in h.lower() for h in heading_list):
                    in_headings = True
                    break
            
            keyword_analysis[keyword] = {
                "count": text_count,
                "density": (text_count / len(text.split())) * 100 if text else 0,
                "in_title": in_title,
                "in_meta_description": in_meta_desc,
                "in_headings": in_headings,
            }
        
        return {
            "target_keywords": target_keywords,
            "keyword_analysis": keyword_analysis,
        }
    
    def _analyze_readability(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze content readability (basic implementation)."""
        text = soup.get_text()
        
        # Basic readability metrics
        sentences = text.count(".") + text.count("!") + text.count("?")
        words = len(text.split())
        
        if sentences == 0:
            return {"readability_score": 0, "avg_sentence_length": 0}
        
        avg_sentence_length = words / sentences
        
        # Simple readability score (lower is better)
        readability_score = min(100, max(0, 100 - (avg_sentence_length - 15) * 2))
        
        return {
            "readability_score": readability_score,
            "avg_sentence_length": avg_sentence_length,
            "total_sentences": sentences,
            "total_words": words,
        }
    
    def _analyze_content_quality(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze overall content quality."""
        text = soup.get_text()
        words = text.split()
        
        # Basic quality indicators
        word_count = len(words)
        unique_words = len(set(word.lower() for word in words))
        
        quality_score = 0
        
        # Word count scoring
        if word_count >= 1000:
            quality_score += 30
        elif word_count >= 500:
            quality_score += 20
        elif word_count >= 300:
            quality_score += 10
        
        # Vocabulary diversity
        if word_count > 0:
            diversity_ratio = unique_words / word_count
            quality_score += diversity_ratio * 30
        
        # Structure scoring
        paragraphs = len(soup.find_all("p"))
        if paragraphs >= 3:
            quality_score += 20
        
        # Lists and formatting
        lists = len(soup.find_all(["ul", "ol"]))
        if lists > 0:
            quality_score += 10
        
        # Images
        images = len(soup.find_all("img"))
        if images > 0:
            quality_score += 10
        
        return {
            "quality_score": min(100, quality_score),
            "word_count": word_count,
            "unique_words": unique_words,
            "vocabulary_diversity": unique_words / word_count if word_count > 0 else 0,
            "paragraphs": paragraphs,
            "lists": lists,
            "images": images,
        }
