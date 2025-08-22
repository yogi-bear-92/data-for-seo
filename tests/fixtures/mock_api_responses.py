"""Mock API responses for Data for SEO API testing."""

import json
from datetime import datetime
from typing import Any, Dict, List
from uuid import uuid4


def generate_mock_serp_response(
    keyword: str = "test keyword",
    location: str = "United States",
    results_count: int = 10
) -> Dict[str, Any]:
    """Generate mock SERP response from Data for SEO API."""
    items = []
    
    for i in range(results_count):
        items.append({
            "type": "organic",
            "rank_group": i + 1,
            "rank_absolute": i + 1,
            "position": "left",
            "xpath": f"/html[1]/body[1]/div[6]/div[1]/div[9]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[{i+1}]",
            "domain": f"example{i+1}.com",
            "title": f"Test Result {i+1} - {keyword.title()} Guide",
            "url": f"https://example{i+1}.com/page-{i+1}",
            "cache_url": f"https://webcache.googleusercontent.com/search?q=cache:example{i+1}.com",
            "breadcrumb": f"example{i+1}.com › guide › {keyword.replace(' ', '-')}",
            "website_name": f"Example {i+1} Website",
            "description": f"Comprehensive guide about {keyword} with detailed information and best practices. Learn everything you need to know about {keyword} optimization.",
            "amp_version": False,
            "rating": {
                "rating_type": "Max5",
                "value": 4.5 + (i * 0.1) % 0.5,
                "votes_count": 150 - (i * 10),
                "rating_max": 5
            } if i < 3 else None,
            "highlighted": keyword.split(),
            "links": [
                {
                    "type": "sitelink",
                    "title": f"Advanced {keyword.title()}",
                    "description": f"Learn advanced {keyword} techniques",
                    "url": f"https://example{i+1}.com/advanced-{keyword.replace(' ', '-')}",
                },
                {
                    "type": "sitelink", 
                    "title": f"{keyword.title()} Tools",
                    "description": f"Best tools for {keyword}",
                    "url": f"https://example{i+1}.com/tools",
                }
            ] if i < 5 else [],
            "faq": [
                {
                    "type": "faq_box",
                    "title": f"What is {keyword}?",
                    "description": f"{keyword.title()} is a comprehensive approach to optimizing your website for search engines."
                }
            ] if i == 0 else None,
        })
    
    return {
        "status_code": 20000,
        "status_message": "Ok.",
        "time": "0.1234",
        "cost": 0.01 * results_count,
        "tasks_count": 1,
        "tasks_error": 0,
        "tasks": [
            {
                "id": str(uuid4()),
                "status_code": 20000,
                "status_message": "Ok.",
                "time": "0.1234",
                "cost": 0.01 * results_count,
                "result_count": 1,
                "path": ["v3", "serp", "google", "organic", "live", "advanced"],
                "data": {
                    "api": "serp",
                    "function": "live_advanced",
                    "keyword": keyword,
                    "location_code": 2840,  # United States
                    "language_code": "en",
                    "device": "desktop",
                    "os": "windows",
                },
                "result": [
                    {
                        "keyword": keyword,
                        "type": "organic",
                        "se_domain": "google.com",
                        "location_code": 2840,
                        "language_code": "en",
                        "check_url": f"https://www.google.com/search?q={keyword.replace(' ', '+')}",
                        "datetime": datetime.utcnow().isoformat() + " +00:00",
                        "spell": None,
                        "refinement_chips": None,
                        "item_types": ["organic", "paid"],
                        "se_results_count": 1234567 + (len(keyword) * 10000),
                        "items_count": results_count,
                        "items": items,
                    }
                ],
            }
        ],
    }


def generate_mock_keyword_data_response(keywords: List[str]) -> Dict[str, Any]:
    """Generate mock keyword data response."""
    tasks = []
    
    for keyword in keywords:
        keyword_data = {
            "keyword": keyword,
            "location_code": 2840,
            "language_code": "en",
            "search_partners": False,
            "competition": round(0.3 + (len(keyword) % 10) * 0.07, 2),
            "competition_level": "MEDIUM" if len(keyword) % 3 == 0 else "HIGH" if len(keyword) % 2 == 0 else "LOW",
            "cpc": round(1.25 + (len(keyword) * 0.15), 2),
            "search_volume": 1000 + (len(keyword) * 150) + (hash(keyword) % 5000),
            "low_top_of_page_bid": round(0.8 + (len(keyword) * 0.1), 2),
            "high_top_of_page_bid": round(2.5 + (len(keyword) * 0.2), 2),
            "categories": [
                10166,  # Business & Industrial
                10167,  # Computers & Electronics
            ],
            "monthly_searches": [
                {"year": 2024, "month": 1, "search_volume": 1200 + (hash(keyword) % 300)},
                {"year": 2023, "month": 12, "search_volume": 1100 + (hash(keyword) % 300)},
                {"year": 2023, "month": 11, "search_volume": 1050 + (hash(keyword) % 300)},
            ],
        }
        
        tasks.append({
            "id": str(uuid4()),
            "status_code": 20000,
            "status_message": "Ok.",
            "time": "0.0567",
            "cost": 0.002,
            "result_count": 1,
            "path": ["v3", "keywords_data", "google_ads", "search_volume", "live"],
            "data": {
                "api": "keywords_data",
                "function": "search_volume",
                "keywords": [keyword],
                "location_code": 2840,
                "language_code": "en",
            },
            "result": [keyword_data],
        })
    
    return {
        "status_code": 20000,
        "status_message": "Ok.",
        "time": "0.1234",
        "cost": 0.002 * len(keywords),
        "tasks_count": len(keywords),
        "tasks_error": 0,
        "tasks": tasks,
    }


def generate_mock_competitor_analysis_response(domain: str) -> Dict[str, Any]:
    """Generate mock competitor analysis response."""
    competitors = [
        f"competitor1-{domain.replace('.', '-')}.com",
        f"competitor2-{domain.replace('.', '-')}.com", 
        f"competitor3-{domain.replace('.', '-')}.com",
    ]
    
    return {
        "status_code": 20000,
        "status_message": "Ok.",
        "time": "0.2341",
        "cost": 0.05,
        "tasks_count": 1,
        "tasks_error": 0,
        "tasks": [
            {
                "id": str(uuid4()),
                "status_code": 20000,
                "status_message": "Ok.",
                "time": "0.2341",
                "cost": 0.05,
                "result_count": 1,
                "path": ["v3", "dataforseo_labs", "google", "competitors_domain", "live"],
                "data": {
                    "api": "dataforseo_labs",
                    "function": "competitors_domain",
                    "target": domain,
                    "location_code": 2840,
                    "language_code": "en",
                },
                "result": [
                    {
                        "target": domain,
                        "location_code": 2840,
                        "language_code": "en",
                        "total_count": len(competitors),
                        "items_count": len(competitors),
                        "items": [
                            {
                                "se_type": "google",
                                "domain": comp,
                                "avg_position": 15.5 + (i * 2.3),
                                "sum_position": 1250 + (i * 150),
                                "intersections": 45 - (i * 5),
                                "full_domain_metrics": {
                                    "organic_keywords": 2500 + (i * 200),
                                    "organic_traffic": 15000 + (i * 1500),
                                    "organic_cost": 12500 + (i * 1000),
                                    "paid_keywords": 150 + (i * 25),
                                    "paid_traffic": 800 + (i * 100),
                                    "paid_cost": 2500 + (i * 300),
                                }
                            }
                            for i, comp in enumerate(competitors)
                        ],
                    }
                ],
            }
        ],
    }


def generate_mock_backlinks_response(domain: str) -> Dict[str, Any]:
    """Generate mock backlinks response."""
    backlinks = []
    
    for i in range(20):
        backlinks.append({
            "type": "backlink",
            "domain_from": f"referrer{i+1}.com",
            "url_from": f"https://referrer{i+1}.com/article-{i+1}",
            "url_to": f"https://{domain}/page-{i+1}",
            "tld_from": "com",
            "is_new": i < 3,
            "is_lost": False,
            "rank": 85 - (i * 2),
            "page_from_rank": 78 - (i * 1.5),
            "domain_from_rank": 82 - (i * 1.8),
            "page_from_external_links": 150 - (i * 5),
            "domain_from_external_links": 2500 - (i * 100),
            "page_from_internal_links": 45 + (i * 2),
            "domain_from_internal_links": 8500 + (i * 50),
            "page_from_size": 25000 + (i * 1000),
            "anchor": f"anchor text {i+1}",
            "image_url": f"https://referrer{i+1}.com/image-{i+1}.jpg" if i % 3 == 0 else None,
            "link_attribute": "followed" if i % 4 != 0 else "nofollow",
            "page_from_title": f"Article {i+1} About SEO and Digital Marketing",
            "first_seen": "2024-01-01",
            "prev_seen": "2024-01-15",
            "last_seen": "2024-01-16",
        })
    
    return {
        "status_code": 20000,
        "status_message": "Ok.",
        "time": "0.3456",
        "cost": 0.1,
        "tasks_count": 1,
        "tasks_error": 0,
        "tasks": [
            {
                "id": str(uuid4()),
                "status_code": 20000,
                "status_message": "Ok.",
                "time": "0.3456",
                "cost": 0.1,
                "result_count": 1,
                "path": ["v3", "backlinks", "backlinks", "live"],
                "data": {
                    "api": "backlinks",
                    "function": "backlinks",
                    "target": domain,
                    "limit": 100,
                },
                "result": [
                    {
                        "target": domain,
                        "total_count": len(backlinks),
                        "items_count": len(backlinks),
                        "items": backlinks,
                    }
                ],
            }
        ],
    }


def generate_mock_domain_analytics_response(domain: str) -> Dict[str, Any]:
    """Generate mock domain analytics response."""
    return {
        "status_code": 20000,
        "status_message": "Ok.",
        "time": "0.1567",
        "cost": 0.025,
        "tasks_count": 1,
        "tasks_error": 0,
        "tasks": [
            {
                "id": str(uuid4()),
                "status_code": 20000,
                "status_message": "Ok.",
                "time": "0.1567",
                "cost": 0.025,
                "result_count": 1,
                "path": ["v3", "domain_analytics", "google", "organic", "pages", "live"],
                "data": {
                    "api": "domain_analytics",
                    "function": "organic_pages",
                    "target": domain,
                    "location_code": 2840,
                    "language_code": "en",
                },
                "result": [
                    {
                        "target": domain,
                        "location_code": 2840,
                        "language_code": "en",
                        "total_count": 150,
                        "items_count": 50,
                        "metrics": {
                            "organic_keywords": 3500,
                            "organic_traffic": 25000,
                            "organic_cost": 18500,
                            "organic_count": 150,
                        },
                        "items": [
                            {
                                "page": f"https://{domain}/page-{i+1}",
                                "keywords": 25 - i,
                                "traffic": 1500 - (i * 50),
                                "cost": 1200 - (i * 40),
                                "count": 45 - i,
                            }
                            for i in range(50)
                        ],
                    }
                ],
            }
        ],
    }


def generate_mock_technical_audit_response(domain: str) -> Dict[str, Any]:
    """Generate mock technical audit response."""
    issues = [
        {
            "type": "missing_meta_description",
            "severity": "warning",
            "affected_urls": [
                f"https://{domain}/page-without-meta",
                f"https://{domain}/another-page-without-meta",
            ],
            "description": "Pages missing meta description tags",
            "recommendation": "Add unique meta descriptions to all pages",
        },
        {
            "type": "duplicate_title_tags",
            "severity": "error",
            "affected_urls": [
                f"https://{domain}/duplicate-title-1",
                f"https://{domain}/duplicate-title-2",
            ],
            "description": "Multiple pages with identical title tags",
            "recommendation": "Create unique title tags for each page",
        },
        {
            "type": "broken_internal_links",
            "severity": "error",
            "affected_urls": [
                f"https://{domain}/broken-link-page",
            ],
            "description": "Internal links returning 404 errors",
            "recommendation": "Fix or remove broken internal links",
        },
        {
            "type": "missing_alt_text",
            "severity": "warning",
            "affected_urls": [
                f"https://{domain}/images-without-alt",
            ],
            "description": "Images missing alt text attributes",
            "recommendation": "Add descriptive alt text to all images",
        },
        {
            "type": "slow_page_speed",
            "severity": "critical",
            "affected_urls": [
                f"https://{domain}/slow-page",
            ],
            "description": "Pages with slow loading times",
            "recommendation": "Optimize images and reduce server response time",
        },
    ]
    
    return {
        "status_code": 20000,
        "status_message": "Ok.",
        "time": "2.1234",
        "cost": 0.5,
        "tasks_count": 1,
        "tasks_error": 0,
        "tasks": [
            {
                "id": str(uuid4()),
                "status_code": 20000,
                "status_message": "Ok.",
                "time": "2.1234",
                "cost": 0.5,
                "result_count": 1,
                "path": ["v3", "on_page", "summary", "live"],
                "data": {
                    "api": "on_page",
                    "function": "summary",
                    "target": domain,
                },
                "result": [
                    {
                        "crawl_progress": "finished",
                        "crawl_status": {
                            "max_crawl_pages": 100,
                            "pages_in_queue": 0,
                            "pages_crawled": 95,
                        },
                        "total_issues": len(issues),
                        "issues_by_severity": {
                            "critical": 1,
                            "error": 2,
                            "warning": 2,
                            "notice": 0,
                        },
                        "issues": issues,
                        "pages_summary": {
                            "total_pages": 95,
                            "unique_pages": 92,
                            "duplicate_pages": 3,
                            "pages_with_issues": 15,
                            "pages_without_issues": 80,
                        },
                        "performance_metrics": {
                            "average_loading_time": 2.3,
                            "average_page_size": 1250000,
                            "pages_over_3s": 8,
                            "pages_over_5s": 2,
                        },
                    }
                ],
            }
        ],
    }


# Error response templates
def generate_error_response(
    status_code: int = 40000,
    status_message: str = "Bad Request",
    error_message: str = "Invalid parameters"
) -> Dict[str, Any]:
    """Generate mock error response."""
    return {
        "status_code": status_code,
        "status_message": status_message,
        "time": "0.0123",
        "cost": 0,
        "tasks_count": 0,
        "tasks_error": 1,
        "tasks": [
            {
                "id": str(uuid4()),
                "status_code": status_code,
                "status_message": status_message,
                "time": "0.0123",
                "cost": 0,
                "result_count": 0,
                "path": [],
                "data": {},
                "result": None,
                "error": {
                    "error_code": status_code,
                    "error_message": error_message,
                }
            }
        ],
    }


# Rate limit response
RATE_LIMIT_RESPONSE = generate_error_response(
    status_code=40103,
    status_message="Rate Limit Exceeded",
    error_message="API rate limit exceeded. Please wait before making more requests."
)

# Authentication error response
AUTH_ERROR_RESPONSE = generate_error_response(
    status_code=40101,
    status_message="Authentication Failed",
    error_message="Invalid API credentials provided."
)

# All mock responses for easy access
MOCK_API_RESPONSES = {
    "serp_success": generate_mock_serp_response(),
    "keyword_data_success": generate_mock_keyword_data_response(["test keyword", "seo analysis"]),
    "competitor_analysis_success": generate_mock_competitor_analysis_response("example.com"),
    "backlinks_success": generate_mock_backlinks_response("example.com"),
    "domain_analytics_success": generate_mock_domain_analytics_response("example.com"),
    "technical_audit_success": generate_mock_technical_audit_response("example.com"),
    "rate_limit_error": RATE_LIMIT_RESPONSE,
    "auth_error": AUTH_ERROR_RESPONSE,
}