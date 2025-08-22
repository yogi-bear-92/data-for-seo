# SEO Analysis Patterns and Methodologies

## Overview

This guide provides comprehensive SEO analysis patterns, scoring algorithms, and methodologies used in the SEO automation framework. It covers technical SEO, content analysis, performance metrics, and recommendation generation.

## SEO Analysis Framework

### Multi-Dimensional Analysis Approach

SEO analysis is performed across four key dimensions:

1. **Technical SEO** (40% weight) - Infrastructure and crawlability
2. **Content Quality** (30% weight) - Content relevance and optimization
3. **Performance** (20% weight) - Page speed and user experience
4. **Authority** (10% weight) - Backlinks and domain authority

### Scoring Algorithm

```python
def calculate_overall_seo_score(
    technical_score: float,
    content_score: float,
    performance_score: float,
    authority_score: float
) -> float:
    """Calculate weighted overall SEO score (0-100)."""
    return (
        technical_score * 0.40 +
        content_score * 0.30 +
        performance_score * 0.20 +
        authority_score * 0.10
    )
```

## Technical SEO Analysis

### Core Technical Factors

#### 1. HTTPS Implementation
```python
def analyze_https(url: str) -> dict:
    """Analyze HTTPS implementation."""
    return {
        "has_https": url.startswith("https://"),
        "score_impact": 15,  # 15 points out of 100
        "priority": "high" if not url.startswith("https://") else "low",
        "recommendation": "Enable HTTPS for security and SEO benefits" if not url.startswith("https://") else None
    }
```

#### 2. Mobile-Friendly Analysis
```python
def analyze_mobile_friendly(soup: BeautifulSoup) -> dict:
    """Analyze mobile-friendly indicators."""
    viewport_meta = soup.find("meta", attrs={"name": "viewport"})
    has_viewport = viewport_meta is not None
    
    # Check for responsive design indicators
    has_media_queries = "@media" in str(soup)
    
    mobile_score = 0
    if has_viewport:
        mobile_score += 10
    if has_media_queries:
        mobile_score += 10
    
    return {
        "has_viewport": has_viewport,
        "has_media_queries": has_media_queries,
        "mobile_score": mobile_score,
        "score_impact": 20,  # 20 points out of 100
        "recommendations": generate_mobile_recommendations(has_viewport, has_media_queries)
    }

def generate_mobile_recommendations(has_viewport: bool, has_media_queries: bool) -> list:
    recommendations = []
    if not has_viewport:
        recommendations.append({
            "type": "mobile",
            "priority": "high",
            "message": "Add viewport meta tag",
            "description": "Add <meta name='viewport' content='width=device-width, initial-scale=1'> to improve mobile experience"
        })
    if not has_media_queries:
        recommendations.append({
            "type": "mobile",
            "priority": "medium",
            "message": "Implement responsive design",
            "description": "Use CSS media queries to create responsive layouts for different screen sizes"
        })
    return recommendations
```

#### 3. Page Speed Analysis
```python
def analyze_page_speed(response_time: float, content_size: int) -> dict:
    """Analyze page speed metrics."""
    speed_score = 100
    
    # Response time penalties
    if response_time > 3.0:
        speed_score -= 40
    elif response_time > 2.0:
        speed_score -= 25
    elif response_time > 1.0:
        speed_score -= 15
    elif response_time > 0.5:
        speed_score -= 5
    
    # Content size penalties
    if content_size > 2_000_000:  # 2MB
        speed_score -= 20
    elif content_size > 1_000_000:  # 1MB
        speed_score -= 10
    elif content_size > 500_000:  # 500KB
        speed_score -= 5
    
    return {
        "response_time": response_time,
        "content_size": content_size,
        "speed_score": max(0, speed_score),
        "score_impact": 25,  # 25 points out of 100
        "performance_grade": get_performance_grade(speed_score),
        "recommendations": generate_speed_recommendations(response_time, content_size)
    }

def get_performance_grade(score: float) -> str:
    """Get performance grade based on score."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"
```

#### 4. Crawlability Analysis
```python
async def analyze_crawlability(url: str) -> dict:
    """Analyze website crawlability."""
    domain = extract_domain(url)
    
    # Check robots.txt
    robots_status = await check_robots_txt(domain)
    
    # Check XML sitemap
    sitemap_status = await check_xml_sitemap(domain)
    
    # Check meta robots
    meta_robots = await check_meta_robots(url)
    
    crawlability_score = 0
    
    if robots_status["exists"] and robots_status["accessible"]:
        crawlability_score += 10
    
    if sitemap_status["exists"] and sitemap_status["accessible"]:
        crawlability_score += 15
    
    if not meta_robots.get("blocks_indexing", False):
        crawlability_score += 10
    
    return {
        "robots_txt": robots_status,
        "xml_sitemap": sitemap_status,
        "meta_robots": meta_robots,
        "crawlability_score": crawlability_score,
        "score_impact": 15,  # 15 points out of 100
        "recommendations": generate_crawlability_recommendations(robots_status, sitemap_status, meta_robots)
    }
```

#### 5. Structured Data Analysis
```python
def analyze_structured_data(soup: BeautifulSoup) -> dict:
    """Analyze structured data implementation."""
    schema_types = []
    
    # JSON-LD schema
    json_ld_scripts = soup.find_all("script", type="application/ld+json")
    for script in json_ld_scripts:
        try:
            import json
            data = json.loads(script.string)
            if isinstance(data, dict) and "@type" in data:
                schema_types.append(data["@type"])
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and "@type" in item:
                        schema_types.append(item["@type"])
        except (json.JSONDecodeError, AttributeError):
            continue
    
    # Microdata schema
    microdata_elements = soup.find_all(attrs={"itemtype": True})
    for element in microdata_elements:
        itemtype = element.get("itemtype", "")
        if "schema.org" in itemtype:
            schema_type = itemtype.split("/")[-1]
            schema_types.append(schema_type)
    
    structured_data_score = min(25, len(set(schema_types)) * 5)  # 5 points per unique schema type, max 25
    
    return {
        "schema_types": list(set(schema_types)),
        "json_ld_count": len(json_ld_scripts),
        "microdata_count": len(microdata_elements),
        "structured_data_score": structured_data_score,
        "score_impact": 25,  # 25 points out of 100
        "recommendations": generate_structured_data_recommendations(schema_types)
    }
```

## Content Analysis Patterns

### 1. Title Tag Optimization
```python
def analyze_title_tag(soup: BeautifulSoup, target_keywords: list = None) -> dict:
    """Analyze title tag optimization."""
    title_element = soup.find("title")
    
    if not title_element:
        return {
            "has_title": False,
            "title_score": 0,
            "score_impact": 20,
            "recommendations": [{
                "type": "title",
                "priority": "critical",
                "message": "Missing title tag",
                "description": "Add a unique, descriptive title tag to every page"
            }]
        }
    
    title = title_element.get_text().strip()
    title_length = len(title)
    
    # Title scoring
    title_score = 0
    
    # Length scoring
    if 30 <= title_length <= 60:
        title_score += 15  # Optimal length
    elif 20 <= title_length <= 70:
        title_score += 10  # Acceptable length
    elif title_length > 0:
        title_score += 5   # Has title but poor length
    
    # Keyword presence scoring
    if target_keywords:
        keyword_present = any(keyword.lower() in title.lower() for keyword in target_keywords)
        if keyword_present:
            title_score += 5
    
    return {
        "has_title": True,
        "title": title,
        "title_length": title_length,
        "title_score": title_score,
        "score_impact": 20,
        "keyword_present": keyword_present if target_keywords else None,
        "recommendations": generate_title_recommendations(title, title_length, target_keywords)
    }

def generate_title_recommendations(title: str, length: int, keywords: list = None) -> list:
    recommendations = []
    
    if length < 30:
        recommendations.append({
            "type": "title",
            "priority": "medium",
            "message": "Title too short",
            "description": f"Current title is {length} characters. Aim for 30-60 characters for better visibility."
        })
    elif length > 60:
        recommendations.append({
            "type": "title",
            "priority": "medium",
            "message": "Title too long",
            "description": f"Current title is {length} characters. Keep under 60 characters to avoid truncation."
        })
    
    if keywords and not any(kw.lower() in title.lower() for kw in keywords):
        recommendations.append({
            "type": "title",
            "priority": "high",
            "message": "Include target keywords",
            "description": f"Consider including target keywords: {', '.join(keywords[:3])}"
        })
    
    return recommendations
```

### 2. Meta Description Analysis
```python
def analyze_meta_description(soup: BeautifulSoup, target_keywords: list = None) -> dict:
    """Analyze meta description optimization."""
    meta_desc_element = soup.find("meta", attrs={"name": "description"})
    
    if not meta_desc_element:
        return {
            "has_meta_description": False,
            "meta_description_score": 0,
            "score_impact": 15,
            "recommendations": [{
                "type": "meta_description",
                "priority": "high",
                "message": "Missing meta description",
                "description": "Add a compelling meta description to improve click-through rates"
            }]
        }
    
    meta_desc = meta_desc_element.get("content", "").strip()
    desc_length = len(meta_desc)
    
    # Meta description scoring
    desc_score = 0
    
    # Length scoring
    if 120 <= desc_length <= 160:
        desc_score += 10  # Optimal length
    elif 100 <= desc_length <= 170:
        desc_score += 7   # Acceptable length
    elif desc_length > 0:
        desc_score += 3   # Has description but poor length
    
    # Keyword presence scoring
    keyword_present = False
    if target_keywords:
        keyword_present = any(keyword.lower() in meta_desc.lower() for keyword in target_keywords)
        if keyword_present:
            desc_score += 5
    
    return {
        "has_meta_description": True,
        "meta_description": meta_desc,
        "description_length": desc_length,
        "meta_description_score": desc_score,
        "score_impact": 15,
        "keyword_present": keyword_present,
        "recommendations": generate_meta_description_recommendations(meta_desc, desc_length, target_keywords)
    }
```

### 3. Content Quality Analysis
```python
def analyze_content_quality(soup: BeautifulSoup) -> dict:
    """Analyze overall content quality."""
    # Extract main content (remove nav, footer, sidebar)
    content_text = extract_main_content(soup)
    
    words = content_text.split()
    word_count = len(words)
    
    # Calculate readability metrics
    sentences = count_sentences(content_text)
    avg_sentence_length = word_count / max(sentences, 1)
    
    # Calculate vocabulary diversity
    unique_words = len(set(word.lower().strip(".,!?;:") for word in words))
    vocabulary_diversity = unique_words / max(word_count, 1)
    
    # Content structure analysis
    headings = analyze_heading_structure(soup)
    paragraphs = len(soup.find_all("p"))
    lists = len(soup.find_all(["ul", "ol"]))
    images = len(soup.find_all("img"))
    
    # Content quality scoring
    quality_score = 0
    
    # Word count scoring
    if word_count >= 1000:
        quality_score += 25
    elif word_count >= 500:
        quality_score += 15
    elif word_count >= 300:
        quality_score += 10
    elif word_count >= 150:
        quality_score += 5
    
    # Readability scoring
    if 15 <= avg_sentence_length <= 25:
        quality_score += 10  # Good readability
    elif 10 <= avg_sentence_length <= 30:
        quality_score += 5   # Acceptable readability
    
    # Vocabulary diversity scoring
    if vocabulary_diversity >= 0.6:
        quality_score += 10
    elif vocabulary_diversity >= 0.4:
        quality_score += 5
    
    # Structure scoring
    if headings["h1_count"] == 1:
        quality_score += 10  # Proper H1 usage
    
    if headings["total_headings"] >= 3:
        quality_score += 5   # Good heading structure
    
    if paragraphs >= 3:
        quality_score += 5   # Adequate paragraph structure
    
    if lists > 0:
        quality_score += 5   # Use of lists for better readability
    
    if images > 0:
        quality_score += 5   # Visual content
    
    return {
        "word_count": word_count,
        "sentence_count": sentences,
        "avg_sentence_length": round(avg_sentence_length, 1),
        "vocabulary_diversity": round(vocabulary_diversity, 2),
        "heading_structure": headings,
        "paragraph_count": paragraphs,
        "list_count": lists,
        "image_count": images,
        "content_quality_score": min(100, quality_score),
        "score_impact": 30,
        "recommendations": generate_content_quality_recommendations(
            word_count, avg_sentence_length, vocabulary_diversity, headings
        )
    }

def extract_main_content(soup: BeautifulSoup) -> str:
    """Extract main content text, excluding navigation and other non-content elements."""
    # Remove script and style elements
    for element in soup(["script", "style", "nav", "header", "footer", "aside"]):
        element.decompose()
    
    # Try to find main content area
    main_content = soup.find("main") or soup.find("article") or soup.find("div", class_="content")
    
    if main_content:
        return main_content.get_text(separator=" ", strip=True)
    else:
        return soup.get_text(separator=" ", strip=True)

def count_sentences(text: str) -> int:
    """Count sentences in text."""
    import re
    sentences = re.split(r'[.!?]+', text)
    return len([s for s in sentences if s.strip()])

def analyze_heading_structure(soup: BeautifulSoup) -> dict:
    """Analyze heading structure."""
    headings = {}
    total_headings = 0
    
    for i in range(1, 7):
        tag = f"h{i}"
        count = len(soup.find_all(tag))
        headings[f"{tag}_count"] = count
        total_headings += count
    
    headings["total_headings"] = total_headings
    headings["has_proper_h1"] = headings["h1_count"] == 1
    headings["has_hierarchy"] = (
        headings["h1_count"] > 0 and 
        headings["h2_count"] > 0 and
        headings["h1_count"] <= headings["h2_count"]
    )
    
    return headings
```

### 4. Keyword Density Analysis
```python
def analyze_keyword_density(soup: BeautifulSoup, target_keywords: list) -> dict:
    """Analyze keyword density and distribution."""
    content_text = extract_main_content(soup).lower()
    words = content_text.split()
    total_words = len(words)
    
    if total_words == 0:
        return {"error": "No content found"}
    
    keyword_analysis = {}
    
    for keyword in target_keywords:
        keyword_lower = keyword.lower()
        
        # Count exact matches
        exact_matches = content_text.count(keyword_lower)
        
        # Count word-boundary matches (more accurate)
        import re
        word_matches = len(re.findall(r'\b' + re.escape(keyword_lower) + r'\b', content_text))
        
        # Calculate density
        density = (word_matches / total_words) * 100
        
        # Analyze keyword placement
        title = soup.find("title")
        meta_desc = soup.find("meta", attrs={"name": "description"})
        h1_tags = soup.find_all("h1")
        
        in_title = title and keyword_lower in title.get_text().lower()
        in_meta_desc = meta_desc and keyword_lower in meta_desc.get("content", "").lower()
        in_h1 = any(keyword_lower in h1.get_text().lower() for h1 in h1_tags)
        
        # Keyword scoring
        keyword_score = 0
        
        # Density scoring (optimal: 1-3%)
        if 1.0 <= density <= 3.0:
            keyword_score += 10
        elif 0.5 <= density <= 5.0:
            keyword_score += 5
        elif density > 0:
            keyword_score += 2
        
        # Placement scoring
        if in_title:
            keyword_score += 5
        if in_meta_desc:
            keyword_score += 3
        if in_h1:
            keyword_score += 4
        
        keyword_analysis[keyword] = {
            "exact_matches": exact_matches,
            "word_matches": word_matches,
            "density": round(density, 2),
            "in_title": in_title,
            "in_meta_description": in_meta_desc,
            "in_h1": in_h1,
            "keyword_score": keyword_score,
            "recommendations": generate_keyword_recommendations(keyword, density, in_title, in_meta_desc, in_h1)
        }
    
    return {
        "total_words": total_words,
        "keyword_analysis": keyword_analysis,
        "overall_keyword_score": sum(kw["keyword_score"] for kw in keyword_analysis.values()),
        "score_impact": 20
    }

def generate_keyword_recommendations(keyword: str, density: float, in_title: bool, in_meta_desc: bool, in_h1: bool) -> list:
    recommendations = []
    
    if density == 0:
        recommendations.append({
            "type": "keyword",
            "priority": "high",
            "message": f"Keyword '{keyword}' not found",
            "description": f"Include the target keyword '{keyword}' naturally in your content"
        })
    elif density < 0.5:
        recommendations.append({
            "type": "keyword",
            "priority": "medium",
            "message": f"Low keyword density for '{keyword}'",
            "description": f"Current density: {density}%. Consider increasing to 1-3% for better optimization"
        })
    elif density > 5.0:
        recommendations.append({
            "type": "keyword",
            "priority": "medium",
            "message": f"High keyword density for '{keyword}'",
            "description": f"Current density: {density}%. Reduce to avoid keyword stuffing (aim for 1-3%)"
        })
    
    if not in_title:
        recommendations.append({
            "type": "keyword",
            "priority": "high",
            "message": f"Include '{keyword}' in title tag",
            "description": "Adding the target keyword to the title tag improves relevance"
        })
    
    if not in_meta_desc:
        recommendations.append({
            "type": "keyword",
            "priority": "medium",
            "message": f"Include '{keyword}' in meta description",
            "description": "Including keywords in meta descriptions can improve click-through rates"
        })
    
    if not in_h1:
        recommendations.append({
            "type": "keyword",
            "priority": "medium",
            "message": f"Include '{keyword}' in H1 tag",
            "description": "H1 tags help search engines understand page topic and relevance"
        })
    
    return recommendations
```

## Link Analysis Patterns

### Internal Link Analysis
```python
def analyze_internal_links(soup: BeautifulSoup, base_url: str) -> dict:
    """Analyze internal linking structure."""
    domain = extract_domain(base_url)
    all_links = soup.find_all("a", href=True)
    
    internal_links = []
    external_links = []
    
    for link in all_links:
        href = link.get("href", "")
        
        # Skip empty links, anchors, and javascript
        if not href or href.startswith("#") or href.startswith("javascript:"):
            continue
        
        # Resolve relative URLs
        if href.startswith("/"):
            full_url = f"https://{domain}{href}"
            internal_links.append({
                "url": full_url,
                "anchor_text": link.get_text().strip(),
                "title": link.get("title", "")
            })
        elif domain in href:
            internal_links.append({
                "url": href,
                "anchor_text": link.get_text().strip(),
                "title": link.get("title", "")
            })
        elif href.startswith("http"):
            external_links.append({
                "url": href,
                "anchor_text": link.get_text().strip(),
                "title": link.get("title", ""),
                "domain": extract_domain(href)
            })
    
    # Analyze anchor text diversity
    anchor_texts = [link["anchor_text"] for link in internal_links if link["anchor_text"]]
    unique_anchors = len(set(anchor_texts))
    total_anchors = len(anchor_texts)
    
    # Internal linking scoring
    internal_score = 0
    
    if len(internal_links) >= 3:
        internal_score += 10  # Good internal linking
    elif len(internal_links) >= 1:
        internal_score += 5   # Some internal linking
    
    if unique_anchors / max(total_anchors, 1) >= 0.7:
        internal_score += 5   # Good anchor text diversity
    
    return {
        "internal_links": internal_links[:10],  # Limit for response size
        "external_links": external_links[:10],
        "internal_count": len(internal_links),
        "external_count": len(external_links),
        "anchor_text_diversity": round(unique_anchors / max(total_anchors, 1), 2),
        "internal_linking_score": internal_score,
        "score_impact": 10,
        "recommendations": generate_link_recommendations(len(internal_links), len(external_links))
    }
```

## Image Optimization Analysis

```python
def analyze_image_optimization(soup: BeautifulSoup) -> dict:
    """Analyze image optimization."""
    images = soup.find_all("img")
    
    total_images = len(images)
    images_with_alt = 0
    images_with_title = 0
    images_with_lazy_loading = 0
    large_images = 0
    
    image_analysis = []
    
    for img in images:
        src = img.get("src", "")
        alt = img.get("alt", "")
        title = img.get("title", "")
        loading = img.get("loading", "")
        
        has_alt = bool(alt.strip())
        has_title = bool(title.strip())
        has_lazy_loading = loading == "lazy"
        
        if has_alt:
            images_with_alt += 1
        if has_title:
            images_with_title += 1
        if has_lazy_loading:
            images_with_lazy_loading += 1
        
        # Estimate if image might be large (basic heuristic)
        if any(keyword in src.lower() for keyword in ["banner", "hero", "large", "full"]):
            large_images += 1
        
        image_analysis.append({
            "src": src,
            "alt": alt,
            "title": title,
            "has_alt": has_alt,
            "has_title": has_title,
            "has_lazy_loading": has_lazy_loading
        })
    
    # Image optimization scoring
    image_score = 0
    
    if total_images > 0:
        alt_ratio = images_with_alt / total_images
        if alt_ratio >= 0.9:
            image_score += 15  # Excellent alt text coverage
        elif alt_ratio >= 0.7:
            image_score += 10  # Good alt text coverage
        elif alt_ratio >= 0.5:
            image_score += 5   # Fair alt text coverage
        
        # Lazy loading bonus
        if images_with_lazy_loading > 0:
            image_score += 5
    
    return {
        "total_images": total_images,
        "images_with_alt": images_with_alt,
        "images_without_alt": total_images - images_with_alt,
        "alt_text_coverage": round(images_with_alt / max(total_images, 1), 2),
        "images_with_lazy_loading": images_with_lazy_loading,
        "image_optimization_score": image_score,
        "score_impact": 10,
        "recommendations": generate_image_recommendations(total_images, images_with_alt, images_with_lazy_loading)
    }
```

## Recommendation Engine

### Priority-Based Recommendations
```python
class SEORecommendationEngine:
    """Generate prioritized SEO recommendations."""
    
    PRIORITY_WEIGHTS = {
        "critical": 100,
        "high": 75,
        "medium": 50,
        "low": 25
    }
    
    def __init__(self):
        self.recommendations = []
    
    def add_recommendation(self, recommendation: dict):
        """Add a recommendation with automatic priority scoring."""
        priority = recommendation.get("priority", "medium")
        recommendation["priority_score"] = self.PRIORITY_WEIGHTS.get(priority, 50)
        self.recommendations.append(recommendation)
    
    def get_prioritized_recommendations(self, limit: int = 10) -> list:
        """Get recommendations sorted by priority and impact."""
        sorted_recommendations = sorted(
            self.recommendations,
            key=lambda x: (x["priority_score"], x.get("impact_score", 50)),
            reverse=True
        )
        return sorted_recommendations[:limit]
    
    def generate_action_plan(self) -> dict:
        """Generate a structured action plan."""
        recommendations = self.get_prioritized_recommendations()
        
        action_plan = {
            "immediate_actions": [],  # Critical and high priority
            "short_term_goals": [],   # Medium priority
            "long_term_improvements": [],  # Low priority
            "estimated_impact": self.calculate_total_impact()
        }
        
        for rec in recommendations:
            priority = rec.get("priority", "medium")
            if priority in ["critical", "high"]:
                action_plan["immediate_actions"].append(rec)
            elif priority == "medium":
                action_plan["short_term_goals"].append(rec)
            else:
                action_plan["long_term_improvements"].append(rec)
        
        return action_plan
    
    def calculate_total_impact(self) -> dict:
        """Calculate estimated total impact of all recommendations."""
        total_score_improvement = sum(
            rec.get("score_improvement", 5) for rec in self.recommendations
        )
        
        return {
            "potential_score_increase": min(total_score_improvement, 50),  # Cap at 50 points
            "implementation_effort": self.estimate_effort(),
            "timeline": self.estimate_timeline()
        }
    
    def estimate_effort(self) -> str:
        """Estimate implementation effort."""
        critical_count = sum(1 for rec in self.recommendations if rec.get("priority") == "critical")
        high_count = sum(1 for rec in self.recommendations if rec.get("priority") == "high")
        
        if critical_count > 5 or high_count > 10:
            return "high"
        elif critical_count > 2 or high_count > 5:
            return "medium"
        else:
            return "low"
    
    def estimate_timeline(self) -> str:
        """Estimate implementation timeline."""
        effort = self.estimate_effort()
        
        if effort == "high":
            return "2-4 weeks"
        elif effort == "medium":
            return "1-2 weeks"
        else:
            return "2-5 days"
```

This comprehensive SEO analysis framework provides the foundation for automated, accurate, and actionable SEO audits with proper scoring algorithms and recommendation generation.
