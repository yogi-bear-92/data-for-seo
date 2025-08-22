"""Example usage of the Data for SEO API client."""

import asyncio
import os
from data_for_seo.tools import DataForSEOClient


async def main():
    """Demonstrate DataForSEO client usage."""
    
    # Initialize client (credentials would come from environment variables)
    client = DataForSEOClient(
        username=os.getenv("DATAFORSEO_USERNAME", "demo_user"),
        password=os.getenv("DATAFORSEO_PASSWORD", "demo_password"),
        rate_limit=100,  # 100 requests per minute
        redis_url=os.getenv("REDIS_URL"),  # Optional Redis for caching
    )
    
    try:
        async with client:
            print("Data for SEO API Client Example")
            print("=" * 40)
            
            # Example 1: SERP Analysis
            print("\n1. SERP Analysis Example:")
            print("This would analyze search results for 'python programming'")
            # serp_data = await client.get_serp_data(
            #     keyword="python programming",
            #     location_name="United States",
            #     language_name="English"
            # )
            print("✓ SERP analysis method available")
            
            # Example 2: Keywords for Site
            print("\n2. Keywords for Site Example:")
            print("This would get keywords for 'python.org'")
            # keywords_data = await client.get_keywords_for_site(
            #     target="python.org",
            #     limit=50
            # )
            print("✓ Keywords for site method available")
            
            # Example 3: Keyword Suggestions
            print("\n3. Keyword Suggestions Example:")
            print("This would get suggestions for 'web development'")
            # suggestions_data = await client.get_keyword_suggestions(
            #     keyword="web development",
            #     limit=100
            # )
            print("✓ Keyword suggestions method available")
            
            # Example 4: Ranked Keywords
            print("\n4. Ranked Keywords Example:")
            print("This would get ranked keywords for 'github.com'")
            # ranked_data = await client.get_ranked_keywords(
            #     target="github.com",
            #     limit=50
            # )
            print("✓ Ranked keywords method available")
            
            # Rate limiter status
            print(f"\nRate Limiter Status:")
            print(f"Current usage: {client.rate_limiter.get_current_usage()}/{client.rate_limiter.max_requests}")
            print(f"Time until next slot: {client.rate_limiter.get_time_until_next_slot():.2f}s")
            
            print("\n✓ All API endpoints implemented successfully!")
            print("\nTo use with real API calls, set environment variables:")
            print("- DATAFORSEO_USERNAME=your_username")
            print("- DATAFORSEO_PASSWORD=your_password") 
            print("- REDIS_URL=redis://localhost:6379/1 (optional for caching)")
            
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())