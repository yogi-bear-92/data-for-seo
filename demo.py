#!/usr/bin/env python3
"""
Example script demonstrating SEO Collector and Processor agents working together.

This script shows:
1. Creating SEO tasks for keyword research and analysis
2. Using the collector agent to simulate data collection
3. Using the processor agent to analyze the collected data
4. Generating insights and recommendations

Note: This example uses mock data since it requires Data for SEO API credentials.
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from unittest.mock import AsyncMock, patch

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_for_seo.agents.seo_collector import SEOCollectorAgent
from data_for_seo.agents.seo_processor import SEOProcessorAgent
from data_for_seo.models.base import SEOTask


async def demo_keyword_research():
    """Demonstrate keyword research workflow."""
    print("🔍 SEO Agent Demo: Keyword Research and Analysis")
    print("=" * 60)
    
    # Initialize agents
    collector = SEOCollectorAgent()
    processor = SEOProcessorAgent()
    
    print(f"✓ Initialized {collector.name} (supports: {collector.get_supported_task_types()})")
    print(f"✓ Initialized {processor.name} (supports: {processor.get_supported_task_types()})")
    print()
    
    # Create a keyword research task
    keyword_task = SEOTask(
        name="Keyword Research Demo",
        description="Research keywords for SEO tools",
        task_type="keyword_research",
        parameters={
            "keywords": ["seo tools", "keyword research", "rank tracking", "seo analysis"],
            "include_metrics": True,
            "include_ideas": True,
            "location": "United States",
            "language": "en"
        },
        tags=["demo", "keyword_research"]
    )
    
    print(f"📋 Created task: {keyword_task.name}")
    print(f"   Keywords: {keyword_task.parameters['keywords']}")
    print()
    
    # Simulate keyword research (normally would call Data for SEO API)
    print("📊 Simulating keyword research data collection...")
    
    # Mock the API response for demo
    mock_keyword_data = {
        "keywords": keyword_task.parameters["keywords"],
        "location": "United States",
        "language": "en",
        "keyword_data": [
            {
                "keyword": "seo tools",
                "search_volume": 12000,
                "competition": 0.7,
                "cpc": 4.50,
                "keyword_difficulty": "medium"
            },
            {
                "keyword": "keyword research",
                "search_volume": 8500,
                "competition": 0.6,
                "cpc": 3.20,
                "keyword_difficulty": "easy"
            },
            {
                "keyword": "rank tracking",
                "search_volume": 3200,
                "competition": 0.4,
                "cpc": 2.80,
                "keyword_difficulty": "easy"
            },
            {
                "keyword": "seo analysis",
                "search_volume": 6800,
                "competition": 0.5,
                "cpc": 3.90,
                "keyword_difficulty": "medium"
            }
        ],
        "keyword_ideas": [
            {"keyword": "free seo tools", "search_volume": 4500},
            {"keyword": "best keyword research tool", "search_volume": 2100},
            {"keyword": "seo rank checker", "search_volume": 1800},
            {"keyword": "website seo analysis", "search_volume": 3600}
        ],
        "collected_at": datetime.utcnow().isoformat(),
    }
    
    print(f"✓ Collected data for {len(mock_keyword_data['keyword_data'])} keywords")
    print(f"✓ Found {len(mock_keyword_data['keyword_ideas'])} related keyword ideas")
    print()
    
    # Create data analysis task for processor
    analysis_task = SEOTask(
        name="Keyword Data Analysis",
        description="Analyze collected keyword research data",
        task_type="data_analysis",
        parameters={
            "data_source": mock_keyword_data,
            "analysis_type": "comprehensive",
            "store_results": False  # Don't store in vector store for demo
        },
        tags=["demo", "analysis"]
    )
    
    print("🧠 Analyzing keyword data with processor agent...")
    
    # Mock vector store for demo
    with patch.object(processor, '_get_vector_store') as mock_vector_store:
        mock_vector_store.return_value = AsyncMock()
        
        # Execute analysis
        analysis_result = await processor._execute_task_impl(analysis_task)
        
        if analysis_result.success:
            print("✓ Analysis completed successfully!")
            
            # Display analysis results
            data = analysis_result.data
            keyword_analysis = data.get("keyword_analysis", {})
            
            print("\n📈 Analysis Results:")
            print("-" * 40)
            
            # Show keyword metrics
            if keyword_analysis.get("metrics"):
                metrics = keyword_analysis["metrics"]
                print(f"Average Search Volume: {metrics['search_volume']['average']:.0f}")
                print(f"Average CPC: ${metrics['cpc']['average']:.2f}")
                print(f"Average Competition: {metrics['competition']['average']:.2f}")
            
            # Show top opportunities
            opportunities = keyword_analysis.get("top_opportunities", [])
            if opportunities:
                print(f"\n🎯 Top Keyword Opportunities:")
                for i, opp in enumerate(opportunities[:3], 1):
                    keyword = opp.get("keyword", "")
                    score = opp.get("potential_score", 0)
                    volume = opp.get("search_volume", 0)
                    print(f"  {i}. {keyword} (Score: {score:.1f}, Volume: {volume:,})")
            
            # Show insights
            insights = data.get("insights", [])
            if insights:
                print(f"\n💡 Key Insights:")
                for insight in insights:
                    print(f"  • {insight}")
            
            # Show performance metrics
            performance = data.get("performance_metrics", {})
            if performance:
                overall_score = performance.get("overall_score", 0)
                print(f"\n📊 Overall SEO Performance Score: {overall_score:.1f}/100")
            
        else:
            print(f"✗ Analysis failed: {analysis_result.message}")
    
    print()


async def demo_recommendation_generation():
    """Demonstrate recommendation generation."""
    print("💡 Generating SEO Recommendations")
    print("=" * 40)
    
    processor = SEOProcessorAgent()
    
    # Sample analysis data for recommendations
    sample_analysis = {
        "keyword_analysis": {
            "total_keywords": 4,
            "top_opportunities": [
                {
                    "keyword": "keyword research",
                    "potential_score": 85.2,
                    "search_volume": 8500,
                    "competition": 0.6
                },
                {
                    "keyword": "seo analysis", 
                    "potential_score": 78.8,
                    "search_volume": 6800,
                    "competition": 0.5
                }
            ]
        },
        "performance_metrics": {
            "overall_score": 65.5,
            "keyword_performance": 72.0
        }
    }
    
    # Create recommendation task
    rec_task = SEOTask(
        name="Generate SEO Recommendations",
        description="Generate actionable SEO recommendations",
        task_type="recommendation_generation",
        parameters={
            "analysis_data": sample_analysis,
            "recommendation_types": ["keyword", "content", "technical"],
            "priority_level": "high"
        },
        tags=["demo", "recommendations"]
    )
    
    print("🎯 Generating recommendations...")
    
    rec_result = await processor._execute_task_impl(rec_task)
    
    if rec_result.success:
        print("✓ Recommendations generated successfully!")
        
        data = rec_result.data
        
        # Show keyword recommendations
        keyword_recs = data.get("keyword_recommendations", [])
        if keyword_recs:
            print(f"\n🔍 Keyword Recommendations:")
            for i, rec in enumerate(keyword_recs[:2], 1):
                print(f"  {i}. {rec.get('title', '')}")
                print(f"     Priority: {rec.get('priority', 'medium').upper()}")
                print(f"     Impact: {rec.get('impact', 'medium').upper()}")
                
        # Show content recommendations  
        content_recs = data.get("content_recommendations", [])
        if content_recs:
            print(f"\n✍️  Content Recommendations:")
            for i, rec in enumerate(content_recs[:2], 1):
                print(f"  {i}. {rec.get('title', '')}")
                print(f"     Priority: {rec.get('priority', 'medium').upper()}")
        
        # Show quick wins
        quick_wins = data.get("quick_wins", [])
        if quick_wins:
            print(f"\n⚡ Quick Wins ({len(quick_wins)} items):")
            for win in quick_wins[:3]:
                print(f"  • {win.get('title', '')}")
        
    else:
        print(f"✗ Recommendation generation failed: {rec_result.message}")
    
    print()


async def demo_agent_health_check():
    """Demonstrate agent health checks and metrics."""
    print("🏥 Agent Health Check and Metrics")
    print("=" * 40)
    
    collector = SEOCollectorAgent()
    processor = SEOProcessorAgent()
    
    # Get health checks
    collector_health = await collector.health_check()
    processor_health = await processor.health_check()
    
    print("Collector Agent Status:")
    print(f"  Status: {collector_health.get('status', 'unknown')}")
    print(f"  Supported Tasks: {len(collector_health.get('supported_tasks', []))}")
    print(f"  Cache Size: {collector_health.get('cache_size', 0)}")
    
    print("\nProcessor Agent Status:")
    print(f"  Status: {processor_health.get('status', 'unknown')}")
    print(f"  Supported Tasks: {len(processor_health.get('supported_tasks', []))}")
    
    # Get metrics
    collector_metrics = await collector.get_metrics()
    processor_metrics = await processor.get_metrics()
    
    print(f"\nCollector Metrics:")
    print(f"  Tasks Executed: {collector_metrics.get('tasks_executed', 0)}")
    print(f"  Success Rate: {collector_metrics.get('success_rate', 0):.1%}")
    
    print(f"\nProcessor Metrics:")
    print(f"  Tasks Processed: {processor_metrics.get('processing_stats', {}).get('tasks_processed', 0)}")
    print(f"  Patterns Identified: {processor_metrics.get('processing_stats', {}).get('patterns_identified', 0)}")
    print(f"  Recommendations Generated: {processor_metrics.get('processing_stats', {}).get('recommendations_generated', 0)}")
    
    print()


async def main():
    """Run the complete demo."""
    print("🚀 Data for SEO Agent Framework Demo")
    print("=" * 60)
    print("This demo showcases the SEO Collector and Processor agents")
    print("working together to analyze keywords and generate recommendations.")
    print()
    
    try:
        # Run demos
        await demo_keyword_research()
        await demo_recommendation_generation() 
        await demo_agent_health_check()
        
        print("✅ Demo completed successfully!")
        print("\nNext steps:")
        print("1. Configure Data for SEO API credentials")
        print("2. Set up Redis for agent communication")
        print("3. Initialize ChromaDB for knowledge storage")
        print("4. Run real SEO audits with the AgentCoordinator")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Run the demo
    asyncio.run(main())