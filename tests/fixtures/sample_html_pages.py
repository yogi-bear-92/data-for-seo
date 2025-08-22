"""Sample HTML pages for testing SEO analysis."""

# Basic HTML page for testing
BASIC_HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Basic Test Page</title>
    <meta name="description" content="This is a basic test page for SEO analysis.">
</head>
<body>
    <h1>Welcome to the Basic Test Page</h1>
    <p>This is a simple paragraph with basic content.</p>
</body>
</html>
"""

# Comprehensive HTML page with good SEO practices
GOOD_SEO_HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Comprehensive test page demonstrating good SEO practices with proper meta tags, structured content, and semantic markup.">
    <meta name="robots" content="index, follow">
    <meta name="author" content="SEO Test Suite">
    <title>Comprehensive SEO Test Page - Best Practices Example</title>
    <link rel="canonical" href="https://example.com/good-seo-page">
    <link rel="alternate" hreflang="en" href="https://example.com/good-seo-page">
    <link rel="alternate" hreflang="es" href="https://example.com/es/good-seo-page">
    
    <!-- Open Graph tags -->
    <meta property="og:title" content="Comprehensive SEO Test Page">
    <meta property="og:description" content="Test page with excellent SEO practices">
    <meta property="og:image" content="https://example.com/og-image.jpg">
    <meta property="og:url" content="https://example.com/good-seo-page">
    <meta property="og:type" content="website">
    
    <!-- Twitter Card tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Comprehensive SEO Test Page">
    <meta name="twitter:description" content="Test page with excellent SEO practices">
    <meta name="twitter:image" content="https://example.com/twitter-image.jpg">
    
    <!-- Structured Data -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "Comprehensive SEO Test Page",
        "description": "Test page demonstrating good SEO practices",
        "url": "https://example.com/good-seo-page",
        "author": {
            "@type": "Organization",
            "name": "SEO Test Suite"
        },
        "mainEntity": {
            "@type": "Article",
            "headline": "SEO Best Practices Guide",
            "author": {
                "@type": "Organization",
                "name": "SEO Test Suite"
            },
            "datePublished": "2024-01-01",
            "dateModified": "2024-01-15"
        }
    }
    </script>
    
    <style>
        /* Responsive design CSS */
        @media (max-width: 768px) {
            .container { padding: 10px; }
        }
    </style>
</head>
<body>
    <header>
        <nav>
            <ul>
                <li><a href="/">Home</a></li>
                <li><a href="/about">About</a></li>
                <li><a href="/services">Services</a></li>
                <li><a href="/contact">Contact</a></li>
            </ul>
        </nav>
    </header>
    
    <main>
        <article>
            <h1>SEO Best Practices: A Comprehensive Guide</h1>
            
            <p>This comprehensive guide covers all essential SEO best practices that every website should implement. SEO optimization is crucial for improving search engine rankings and driving organic traffic to your website.</p>
            
            <h2>On-Page SEO Fundamentals</h2>
            <p>On-page SEO involves optimizing individual web pages to rank higher and earn more relevant traffic. This includes optimizing both the content and HTML source code of a page, unlike off-page SEO which refers to links and other external signals.</p>
            
            <h3>Title Tag Optimization</h3>
            <p>Title tags are one of the most important on-page SEO elements. They should be descriptive, unique, and contain your target keywords while staying under 60 characters for optimal display in search results.</p>
            
            <h3>Meta Description Best Practices</h3>
            <p>Meta descriptions provide a brief summary of your page content. While they don't directly impact rankings, they significantly affect click-through rates from search results.</p>
            
            <h2>Technical SEO Considerations</h2>
            <p>Technical SEO focuses on optimizing the infrastructure of your website to help search engines crawl and index your content more effectively.</p>
            
            <h3>Site Speed and Performance</h3>
            <p>Page loading speed is a crucial ranking factor. Optimize images, minify CSS and JavaScript, and use content delivery networks (CDNs) to improve performance.</p>
            
            <ul>
                <li>Optimize images with proper compression and alt text</li>
                <li>Implement lazy loading for images and videos</li>
                <li>Use browser caching to reduce server load</li>
                <li>Minify CSS, JavaScript, and HTML files</li>
            </ul>
            
            <h2>Content Quality and Relevance</h2>
            <p>High-quality, relevant content is the foundation of good SEO. Create comprehensive, valuable content that addresses user intent and provides genuine value to your audience.</p>
            
            <blockquote>
                "Content is king, but context is God. The best SEO strategies focus on creating content that serves user intent while maintaining technical excellence."
            </blockquote>
            
            <h3>Keyword Research and Optimization</h3>
            <p>Effective keyword research involves understanding your audience's search behavior and creating content that matches their queries. Use tools like Google Keyword Planner, SEMrush, or Ahrefs for comprehensive keyword analysis.</p>
            
            <ol>
                <li>Identify primary and secondary keywords</li>
                <li>Analyze competitor keyword strategies</li>
                <li>Create content clusters around topic themes</li>
                <li>Monitor keyword performance and adjust strategy</li>
            </ol>
            
            <h2>Link Building and Authority</h2>
            <p>Both internal and external links play crucial roles in SEO. Internal links help distribute page authority throughout your site, while quality external links signal authority and relevance to search engines.</p>
            
            <p>For more information, visit our <a href="/advanced-seo-guide">Advanced SEO Guide</a> or check out these authoritative resources:</p>
            <ul>
                <li><a href="https://moz.com/beginners-guide-to-seo" target="_blank" rel="noopener">Moz SEO Guide</a></li>
                <li><a href="https://developers.google.com/search/docs" target="_blank" rel="noopener">Google Search Documentation</a></li>
                <li><a href="https://searchengineland.com" target="_blank" rel="noopener">Search Engine Land</a></li>
            </ul>
        </article>
        
        <aside>
            <h2>Related Articles</h2>
            <ul>
                <li><a href="/technical-seo-checklist">Technical SEO Checklist</a></li>
                <li><a href="/content-optimization-guide">Content Optimization Guide</a></li>
                <li><a href="/local-seo-strategies">Local SEO Strategies</a></li>
            </ul>
        </aside>
    </main>
    
    <footer>
        <p>&copy; 2024 SEO Test Suite. All rights reserved.</p>
        <p>
            <img src="/seo-badge.png" alt="SEO optimized website badge" width="100" height="50">
            <img src="/accessibility-badge.png" alt="WCAG accessibility compliant badge" width="100" height="50">
        </p>
    </footer>
</body>
</html>
"""

# Poor SEO HTML page with common issues
POOR_SEO_HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>page</title>
</head>
<body>
    <h1>header</h1>
    <h3>subheader without h2</h3>
    <p>short content</p>
    <img src="image1.jpg">
    <img src="image2.jpg" alt="">
    <a href="https://spam-site.com">click here</a>
    <script>alert('popup');</script>
</body>
</html>
"""

# HTML page with technical issues
TECHNICAL_ISSUES_HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Test Page with Technical Issues - This title is way too long and exceeds the recommended 60 character limit for optimal search engine display</title>
    <meta name="description" content="This meta description is far too long and exceeds the recommended 160 character limit for optimal search engine results page display which can negatively impact click-through rates from search results.">
    <meta name="robots" content="noindex, nofollow">
</head>
<body>
    <h1>Main Heading</h1>
    <h1>Another H1 - This is problematic</h1>
    <h3>H3 without H2 - Poor hierarchy</h3>
    
    <p>This page has various technical SEO issues that need to be identified and fixed.</p>
    
    <img src="/missing-image.jpg">
    <img src="/another-image.jpg" alt="">
    <img src="data:image/gif;base64,invalid" alt="Invalid image source">
    
    <a href="/broken-link">Broken internal link</a>
    <a href="http://non-secure-external-site.com">Non-HTTPS external link</a>
    <a href="">Empty href attribute</a>
    
    <div itemscope itemtype="https://schema.org/InvalidType">
        <span itemprop="invalidProperty">Invalid schema markup</span>
    </div>
    
    <script type="application/ld+json">
    {
        "invalid": "json
        "missing": "closing_brace"
    </script>
    
    <!-- Missing structured data closing -->
    
    <iframe src="javascript:alert('xss')"></iframe>
    
    <form action="http://insecure-form-handler.com" method="post">
        <input type="text" name="data">
        <input type="submit" value="Submit">
    </form>
</body>
</html>
"""

# Mobile-friendly HTML page
MOBILE_FRIENDLY_HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mobile-Friendly Test Page</title>
    <meta name="description" content="Test page optimized for mobile devices with responsive design.">
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 0; 
            padding: 20px; 
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        @media screen and (max-width: 768px) {
            body { padding: 10px; }
            h1 { font-size: 24px; }
            .nav-menu { 
                flex-direction: column; 
                gap: 10px;
            }
        }
        
        @media screen and (max-width: 480px) {
            h1 { font-size: 20px; }
            p { font-size: 14px; }
        }
        
        .touch-target {
            min-height: 44px;
            min-width: 44px;
            padding: 10px;
            margin: 5px;
        }
        
        img {
            max-width: 100%;
            height: auto;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Mobile-Optimized Content</h1>
            <nav class="nav-menu">
                <a href="/" class="touch-target">Home</a>
                <a href="/about" class="touch-target">About</a>
                <a href="/contact" class="touch-target">Contact</a>
            </nav>
        </header>
        
        <main>
            <p>This page is optimized for mobile devices with proper viewport settings, responsive design, and touch-friendly interface elements.</p>
            
            <img src="/responsive-image.jpg" alt="Responsive image that scales properly" loading="lazy">
            
            <button class="touch-target">Touch-friendly button</button>
        </main>
    </div>
</body>
</html>
"""

# E-commerce product page
ECOMMERCE_PRODUCT_HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Premium SEO Tool - Advanced Website Analysis Software | SEO Suite</title>
    <meta name="description" content="Get the premium SEO tool for comprehensive website analysis. Features keyword tracking, technical audits, and competitor analysis. Try free for 14 days.">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://example.com/products/premium-seo-tool">
    
    <!-- Open Graph for social sharing -->
    <meta property="og:title" content="Premium SEO Tool - Advanced Website Analysis">
    <meta property="og:description" content="Comprehensive SEO analysis tool with keyword tracking and technical audits">
    <meta property="og:image" content="https://example.com/images/seo-tool-preview.jpg">
    <meta property="og:type" content="product">
    <meta property="product:price:amount" content="99.99">
    <meta property="product:price:currency" content="USD">
    
    <!-- Product structured data -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": "Premium SEO Tool",
        "description": "Advanced website analysis software for comprehensive SEO optimization",
        "brand": {
            "@type": "Brand",
            "name": "SEO Suite"
        },
        "sku": "SEO-TOOL-PREMIUM",
        "offers": {
            "@type": "Offer",
            "price": "99.99",
            "priceCurrency": "USD",
            "availability": "https://schema.org/InStock",
            "seller": {
                "@type": "Organization",
                "name": "SEO Suite"
            }
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.8",
            "reviewCount": "127"
        },
        "review": [
            {
                "@type": "Review",
                "author": {
                    "@type": "Person",
                    "name": "John Smith"
                },
                "reviewRating": {
                    "@type": "Rating",
                    "ratingValue": "5"
                },
                "reviewBody": "Excellent SEO tool with comprehensive features."
            }
        ]
    }
    </script>
</head>
<body>
    <header>
        <nav>
            <a href="/">Home</a>
            <a href="/products">Products</a>
            <a href="/pricing">Pricing</a>
            <a href="/support">Support</a>
        </nav>
    </header>
    
    <main>
        <div class="product-container">
            <h1>Premium SEO Tool - Advanced Website Analysis Software</h1>
            
            <div class="product-images">
                <img src="/seo-tool-main.jpg" alt="Premium SEO Tool dashboard showing keyword analysis and technical audit results" width="600" height="400">
                <img src="/seo-tool-features.jpg" alt="SEO tool features including rank tracking and competitor analysis" width="300" height="200">
            </div>
            
            <div class="product-details">
                <h2>Product Features</h2>
                <ul>
                    <li>Comprehensive keyword rank tracking</li>
                    <li>Technical SEO audit automation</li>
                    <li>Competitor analysis and monitoring</li>
                    <li>Backlink profile analysis</li>
                    <li>Content optimization suggestions</li>
                    <li>Local SEO tracking</li>
                </ul>
                
                <h2>Pricing</h2>
                <div class="pricing">
                    <span class="price">$99.99/month</span>
                    <span class="original-price">$149.99</span>
                    <span class="discount">33% off</span>
                </div>
                
                <h2>Customer Reviews</h2>
                <div class="reviews">
                    <div class="review">
                        <h3>Excellent tool for SEO professionals</h3>
                        <p>"This SEO tool has transformed our optimization workflow. The technical audit features are particularly impressive."</p>
                        <p><strong>Rating:</strong> ⭐⭐⭐⭐⭐ (5/5)</p>
                        <p><em>- Sarah Johnson, Digital Marketing Manager</em></p>
                    </div>
                </div>
                
                <div class="product-specs">
                    <h2>Technical Specifications</h2>
                    <table>
                        <tr>
                            <td>Supported websites</td>
                            <td>Unlimited</td>
                        </tr>
                        <tr>
                            <td>Keyword tracking</td>
                            <td>Up to 10,000 keywords</td>
                        </tr>
                        <tr>
                            <td>API access</td>
                            <td>Full REST API</td>
                        </tr>
                        <tr>
                            <td>Data retention</td>
                            <td>2 years</td>
                        </tr>
                    </table>
                </div>
            </div>
        </div>
        
        <section class="related-products">
            <h2>Related Products</h2>
            <div class="product-grid">
                <a href="/products/basic-seo-tool">Basic SEO Tool</a>
                <a href="/products/enterprise-seo-suite">Enterprise SEO Suite</a>
                <a href="/products/local-seo-tracker">Local SEO Tracker</a>
            </div>
        </section>
    </main>
    
    <footer>
        <p>&copy; 2024 SEO Suite. All rights reserved.</p>
        <div class="footer-links">
            <a href="/privacy">Privacy Policy</a>
            <a href="/terms">Terms of Service</a>
            <a href="/contact">Contact Support</a>
        </div>
    </footer>
</body>
</html>
"""

# Blog post HTML page
BLOG_POST_HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>10 Essential SEO Tips for 2024 - Complete Guide | SEO Blog</title>
    <meta name="description" content="Discover the 10 most important SEO tips for 2024. Learn proven strategies to improve your search rankings and drive more organic traffic to your website.">
    <meta name="robots" content="index, follow">
    <meta name="author" content="Jane Doe">
    <link rel="canonical" href="https://example.com/blog/essential-seo-tips-2024">
    
    <!-- Article structured data -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "10 Essential SEO Tips for 2024 - Complete Guide",
        "description": "Comprehensive guide covering the most important SEO strategies for 2024",
        "author": {
            "@type": "Person",
            "name": "Jane Doe",
            "url": "https://example.com/authors/jane-doe"
        },
        "publisher": {
            "@type": "Organization",
            "name": "SEO Blog",
            "logo": {
                "@type": "ImageObject",
                "url": "https://example.com/logo.png"
            }
        },
        "datePublished": "2024-01-15T10:00:00Z",
        "dateModified": "2024-01-16T14:30:00Z",
        "image": "https://example.com/images/seo-tips-2024.jpg",
        "articleSection": "SEO Strategy",
        "wordCount": 1500,
        "keywords": ["SEO tips", "search optimization", "2024 SEO", "organic traffic"]
    }
    </script>
</head>
<body>
    <header>
        <nav>
            <a href="/">Home</a>
            <a href="/blog">Blog</a>
            <a href="/guides">Guides</a>
            <a href="/tools">Tools</a>
        </nav>
    </header>
    
    <main>
        <article>
            <header class="article-header">
                <h1>10 Essential SEO Tips for 2024: A Complete Guide</h1>
                <div class="article-meta">
                    <p>By <a href="/authors/jane-doe">Jane Doe</a> | Published on January 15, 2024 | Updated January 16, 2024</p>
                    <p>Reading time: 8 minutes | Category: <a href="/blog/category/seo-strategy">SEO Strategy</a></p>
                </div>
                <img src="/seo-tips-2024-featured.jpg" alt="Illustration showing SEO optimization strategies and search engine ranking factors for 2024" width="800" height="400">
            </header>
            
            <div class="article-content">
                <p class="lead">Search engine optimization continues to evolve rapidly, and staying ahead of the curve is crucial for maintaining and improving your website's visibility. In this comprehensive guide, we'll explore the 10 most essential SEO tips that will help you dominate search results in 2024.</p>
                
                <h2>1. Focus on User Experience and Core Web Vitals</h2>
                <p>Google's emphasis on user experience has never been stronger. Core Web Vitals, including Largest Contentful Paint (LCP), First Input Delay (FID), and Cumulative Layout Shift (CLS), are critical ranking factors that directly impact your search performance.</p>
                
                <h3>Key Metrics to Monitor</h3>
                <ul>
                    <li><strong>LCP:</strong> Should occur within 2.5 seconds</li>
                    <li><strong>FID:</strong> Should be less than 100 milliseconds</li>
                    <li><strong>CLS:</strong> Should be less than 0.1</li>
                </ul>
                
                <h2>2. Optimize for Mobile-First Indexing</h2>
                <p>With mobile-first indexing now the default for all websites, ensuring your site is fully optimized for mobile devices is non-negotiable. This goes beyond responsive design to include mobile page speed, touch-friendly navigation, and mobile-specific user experience considerations.</p>
                
                <h2>3. Create Comprehensive, Topic-Focused Content</h2>
                <p>Gone are the days of keyword stuffing and thin content. Search engines now favor comprehensive, authoritative content that covers topics in depth. Focus on creating content clusters around main topics, with pillar pages linking to related subtopic pages.</p>
                
                <blockquote>
                    "The best SEO strategy is to create genuinely helpful content that answers users' questions comprehensively and accurately."
                </blockquote>
                
                <h2>4. Implement Advanced Schema Markup</h2>
                <p>Structured data helps search engines understand your content better and can lead to rich snippets in search results. Implement relevant schema types such as Article, FAQ, HowTo, and Review schemas to enhance your search presence.</p>
                
                <h2>5. Optimize for Voice Search and Featured Snippets</h2>
                <p>Voice search optimization involves targeting conversational, long-tail keywords and creating content that answers specific questions. Structure your content to be snippet-friendly by using clear headings, bullet points, and concise answers.</p>
                
                <h3>Voice Search Optimization Tips</h3>
                <ol>
                    <li>Target question-based keywords</li>
                    <li>Use conversational language</li>
                    <li>Optimize for local search queries</li>
                    <li>Create FAQ sections</li>
                </ol>
                
                <h2>6. Build High-Quality Backlinks</h2>
                <p>Quality backlinks remain one of the strongest ranking factors. Focus on earning links from authoritative, relevant websites through guest posting, digital PR, broken link building, and creating linkable assets like original research or comprehensive guides.</p>
                
                <h2>7. Optimize for E-A-T (Expertise, Authoritativeness, Trustworthiness)</h2>
                <p>Google's E-A-T guidelines are particularly important for YMYL (Your Money or Your Life) content. Establish author credibility, cite authoritative sources, maintain accurate information, and regularly update your content to demonstrate expertise and trustworthiness.</p>
                
                <h2>8. Leverage Video Content for SEO</h2>
                <p>Video content can significantly boost engagement and provide additional optimization opportunities. Create video content for important topics, optimize video titles and descriptions, add transcripts, and implement VideoObject schema markup.</p>
                
                <h2>9. Monitor and Improve Page Speed</h2>
                <p>Page speed remains a critical ranking factor and user experience element. Use tools like Google PageSpeed Insights, GTmetrix, and Core Web Vitals reports to identify and fix performance issues.</p>
                
                <h3>Common Page Speed Optimization Techniques</h3>
                <ul>
                    <li>Optimize and compress images</li>
                    <li>Minify CSS, JavaScript, and HTML</li>
                    <li>Enable browser caching</li>
                    <li>Use a Content Delivery Network (CDN)</li>
                    <li>Eliminate render-blocking resources</li>
                </ul>
                
                <h2>10. Focus on Local SEO</h2>
                <p>For businesses with physical locations or local service areas, local SEO is essential. Optimize your Google My Business profile, maintain consistent NAP (Name, Address, Phone) information across all platforms, and encourage customer reviews.</p>
                
                <h2>Conclusion</h2>
                <p>Implementing these 10 essential SEO tips will provide a solid foundation for improving your search engine rankings in 2024. Remember that SEO is a long-term strategy, and consistent effort and monitoring are key to success.</p>
                
                <p>For more advanced SEO strategies, check out our <a href="/guides/advanced-seo-techniques">Advanced SEO Techniques Guide</a> or explore our <a href="/tools/seo-analyzer">free SEO analysis tool</a>.</p>
            </div>
            
            <footer class="article-footer">
                <div class="author-bio">
                    <img src="/authors/jane-doe-avatar.jpg" alt="Jane Doe, SEO Expert and Content Strategist" width="80" height="80">
                    <div>
                        <h3>About the Author</h3>
                        <p><strong>Jane Doe</strong> is a certified SEO expert with over 8 years of experience in digital marketing. She specializes in technical SEO and content strategy for enterprise websites.</p>
                        <p>Follow Jane on <a href="https://twitter.com/janedoe" rel="noopener">Twitter</a> | <a href="https://linkedin.com/in/janedoe" rel="noopener">LinkedIn</a></p>
                    </div>
                </div>
                
                <div class="related-articles">
                    <h3>Related Articles</h3>
                    <ul>
                        <li><a href="/blog/technical-seo-checklist-2024">Complete Technical SEO Checklist for 2024</a></li>
                        <li><a href="/blog/content-optimization-guide">Advanced Content Optimization Strategies</a></li>
                        <li><a href="/blog/local-seo-best-practices">Local SEO Best Practices for Small Businesses</a></li>
                    </ul>
                </div>
            </footer>
        </article>
    </main>
    
    <aside class="sidebar">
        <div class="newsletter-signup">
            <h3>Get Weekly SEO Tips</h3>
            <p>Subscribe to our newsletter for the latest SEO strategies and industry updates.</p>
            <form>
                <input type="email" placeholder="Enter your email" required>
                <button type="submit">Subscribe</button>
            </form>
        </div>
        
        <div class="popular-posts">
            <h3>Popular Posts</h3>
            <ul>
                <li><a href="/blog/seo-audit-checklist">Complete SEO Audit Checklist</a></li>
                <li><a href="/blog/keyword-research-guide">Keyword Research Guide</a></li>
                <li><a href="/blog/link-building-strategies">Link Building Strategies</a></li>
            </ul>
        </div>
    </aside>
    
    <footer>
        <div class="footer-content">
            <p>&copy; 2024 SEO Blog. All rights reserved.</p>
            <nav class="footer-nav">
                <a href="/privacy">Privacy Policy</a>
                <a href="/terms">Terms of Service</a>
                <a href="/contact">Contact</a>
                <a href="/sitemap">Sitemap</a>
            </nav>
        </div>
    </footer>
</body>
</html>
"""

# All sample pages for easy access
SAMPLE_HTML_PAGES = {
    "basic": BASIC_HTML_PAGE,
    "good_seo": GOOD_SEO_HTML_PAGE,
    "poor_seo": POOR_SEO_HTML_PAGE,
    "technical_issues": TECHNICAL_ISSUES_HTML_PAGE,
    "mobile_friendly": MOBILE_FRIENDLY_HTML_PAGE,
    "ecommerce_product": ECOMMERCE_PRODUCT_HTML_PAGE,
    "blog_post": BLOG_POST_HTML_PAGE,
}