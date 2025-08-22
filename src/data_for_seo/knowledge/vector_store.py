"""ChromaDB vector store integration for SEO knowledge management."""

import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import chromadb
from chromadb.api.models.Collection import Collection
from sentence_transformers import SentenceTransformer

from ..config import get_settings
from ..models.base import KnowledgeEntry

logger = logging.getLogger(__name__)


class SEOVectorStore:
    """Vector store for SEO knowledge using ChromaDB."""
    
    def __init__(
        self,
        collection_name: Optional[str] = None,
        embedding_model: Optional[str] = None,
        persist_directory: Optional[str] = None,
    ):
        """Initialize the SEO vector store.
        
        Args:
            collection_name: Name of the ChromaDB collection
            embedding_model: Name of the sentence transformer model
            persist_directory: Directory for ChromaDB persistence
        """
        self.settings = get_settings()
        self.collection_name = collection_name or self.settings.chroma_collection_name
        self.embedding_model_name = embedding_model or self.settings.embedding_model
        self.persist_directory = persist_directory or self.settings.chroma_persist_directory
        
        # Initialize embedding model
        self.embedding_model: Optional[SentenceTransformer] = None
        self.client: Optional[chromadb.PersistentClient] = None
        self.collection: Optional[Collection] = None
        
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    async def initialize(self) -> None:
        """Initialize ChromaDB client and collection."""
        try:
            # Initialize ChromaDB client
            self.client = chromadb.PersistentClient(path=self.persist_directory)
            self.logger.info(f"Initialized ChromaDB client with persist directory: {self.persist_directory}")
            
            # Initialize embedding model
            self.embedding_model = SentenceTransformer(self.embedding_model_name)
            self.logger.info(f"Initialized embedding model: {self.embedding_model_name}")
            
            # Get or create collection
            try:
                self.collection = self.client.get_collection(name=self.collection_name)
                self.logger.info(f"Retrieved existing collection: {self.collection_name}")
            except Exception:
                # Collection doesn't exist, create it
                self.collection = self.client.create_collection(
                    name=self.collection_name,
                    metadata={"description": "SEO knowledge and patterns"}
                )
                self.logger.info(f"Created new collection: {self.collection_name}")
                
        except Exception as e:
            self.logger.error(f"Failed to initialize vector store: {e}")
            raise
    
    def _generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        if not self.embedding_model:
            raise RuntimeError("Embedding model not initialized")
        
        # Generate embedding
        embedding = self.embedding_model.encode(text, convert_to_tensor=False)
        return embedding.tolist()
    
    async def store_knowledge(
        self,
        content: str,
        source_type: str,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        entry_id: Optional[str] = None,
    ) -> str:
        """Store knowledge entry in the vector store.
        
        Args:
            content: Knowledge content
            source_type: Type of knowledge source
            metadata: Additional metadata
            tags: Knowledge tags
            entry_id: Optional entry ID (generated if not provided)
            
        Returns:
            Entry ID
        """
        if not self.collection:
            await self.initialize()
        
        # Generate entry ID if not provided
        if not entry_id:
            entry_id = str(uuid.uuid4())
        
        # Prepare metadata
        entry_metadata = {
            "source_type": source_type,
            "tags": tags or [],
            "created_at": datetime.utcnow().isoformat(),
            **(metadata or {}),
        }
        
        # Generate embedding
        try:
            embedding = self._generate_embedding(content)
        except Exception as e:
            self.logger.error(f"Failed to generate embedding: {e}")
            raise
        
        # Store in ChromaDB
        try:
            self.collection.add(
                ids=[entry_id],
                documents=[content],
                metadatas=[entry_metadata],
                embeddings=[embedding],
            )
            
            self.logger.debug(f"Stored knowledge entry: {entry_id}")
            return entry_id
            
        except Exception as e:
            self.logger.error(f"Failed to store knowledge entry: {e}")
            raise
    
    async def store_seo_analysis(
        self,
        url: str,
        analysis_data: Dict[str, Any],
        analysis_type: str = "seo_analysis",
    ) -> str:
        """Store SEO analysis results.
        
        Args:
            url: Analyzed URL
            analysis_data: Analysis results
            analysis_type: Type of analysis
            
        Returns:
            Entry ID
        """
        # Create searchable content from analysis data
        content_parts = [
            f"URL: {url}",
            f"Analysis Type: {analysis_type}",
        ]
        
        # Extract key information for searchable content
        if "seo_score" in analysis_data:
            content_parts.append(f"SEO Score: {analysis_data['seo_score']}")
        
        if "title" in analysis_data:
            content_parts.append(f"Title: {analysis_data['title']}")
        
        if "meta_description" in analysis_data:
            content_parts.append(f"Meta Description: {analysis_data['meta_description']}")
        
        if "heading_structure" in analysis_data:
            headings = analysis_data["heading_structure"]
            content_parts.append(f"Headings: {', '.join(f'{k}:{v}' for k, v in headings.items())}")
        
        if "keyword_density" in analysis_data:
            keywords = analysis_data["keyword_density"]
            top_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:5]
            content_parts.append(f"Top Keywords: {', '.join(f'{k}({v:.1f}%)' for k, v in top_keywords)}")
        
        content = "\n".join(content_parts)
        
        # Prepare metadata
        metadata = {
            "url": url,
            "analysis_type": analysis_type,
            "seo_score": analysis_data.get("seo_score"),
            "analyzed_at": analysis_data.get("analyzed_at", datetime.utcnow().isoformat()),
        }
        
        # Store with SEO analysis tags
        tags = ["seo_analysis", analysis_type, "url_analysis"]
        
        return await self.store_knowledge(
            content=content,
            source_type="seo_analysis",
            metadata=metadata,
            tags=tags,
        )
    
    async def store_keyword_data(
        self,
        keyword: str,
        keyword_data: Dict[str, Any],
    ) -> str:
        """Store keyword research data.
        
        Args:
            keyword: Target keyword
            keyword_data: Keyword analysis data
            
        Returns:
            Entry ID
        """
        # Create searchable content
        content_parts = [
            f"Keyword: {keyword}",
        ]
        
        if "search_volume" in keyword_data:
            content_parts.append(f"Search Volume: {keyword_data['search_volume']}")
        
        if "keyword_difficulty" in keyword_data:
            content_parts.append(f"Difficulty: {keyword_data['keyword_difficulty']}")
        
        if "cpc" in keyword_data:
            content_parts.append(f"CPC: ${keyword_data['cpc']}")
        
        if "competition" in keyword_data:
            content_parts.append(f"Competition: {keyword_data['competition']}")
        
        if "related_keywords" in keyword_data:
            related = keyword_data["related_keywords"][:5]  # Top 5 related
            content_parts.append(f"Related Keywords: {', '.join(related)}")
        
        content = "\n".join(content_parts)
        
        # Prepare metadata
        metadata = {
            "keyword": keyword,
            "search_volume": keyword_data.get("search_volume"),
            "keyword_difficulty": keyword_data.get("keyword_difficulty"),
            "cpc": keyword_data.get("cpc"),
            "competition": keyword_data.get("competition"),
            "collected_at": keyword_data.get("last_updated", datetime.utcnow().isoformat()),
        }
        
        # Store with keyword tags
        tags = ["keyword_research", "search_data", keyword.replace(" ", "_")]
        
        return await self.store_knowledge(
            content=content,
            source_type="keyword_data",
            metadata=metadata,
            tags=tags,
        )
    
    async def store_competitor_analysis(
        self,
        target_url: str,
        competitor_data: Dict[str, Any],
    ) -> str:
        """Store competitor analysis data.
        
        Args:
            target_url: Target URL being analyzed
            competitor_data: Competitor analysis results
            
        Returns:
            Entry ID
        """
        # Create searchable content
        content_parts = [
            f"Target URL: {target_url}",
            "Competitor Analysis",
        ]
        
        if "competitor_keywords" in competitor_data:
            keyword_count = len(competitor_data["competitor_keywords"])
            content_parts.append(f"Competitor Keywords Found: {keyword_count}")
            
            # Add top competitor keywords
            if keyword_count > 0:
                top_keywords = competitor_data["competitor_keywords"][:10]
                content_parts.append(f"Top Competitor Keywords: {', '.join(kw.get('keyword', '') for kw in top_keywords)}")
        
        if "domain_analytics" in competitor_data:
            analytics = competitor_data["domain_analytics"]
            content_parts.append(f"Domains Analyzed: {len(analytics)}")
        
        content = "\n".join(content_parts)
        
        # Prepare metadata
        metadata = {
            "target_url": target_url,
            "competitor_count": len(competitor_data.get("competitor_urls", [])),
            "keywords_found": len(competitor_data.get("competitor_keywords", [])),
            "collected_at": competitor_data.get("collected_at", datetime.utcnow().isoformat()),
        }
        
        # Store with competitor analysis tags
        tags = ["competitor_analysis", "competitive_intel", "market_research"]
        
        return await self.store_knowledge(
            content=content,
            source_type="competitor_analysis",
            metadata=metadata,
            tags=tags,
        )
    
    async def query_knowledge(
        self,
        query: str,
        n_results: int = 10,
        where: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
    ) -> List[KnowledgeEntry]:
        """Query knowledge entries by similarity.
        
        Args:
            query: Search query
            n_results: Number of results to return
            where: Metadata filter conditions
            tags: Filter by tags
            
        Returns:
            List of knowledge entries with similarity scores
        """
        if not self.collection:
            await self.initialize()
        
        # Generate query embedding
        try:
            query_embedding = self._generate_embedding(query)
        except Exception as e:
            self.logger.error(f"Failed to generate query embedding: {e}")
            raise
        
        # Prepare where clause
        where_clause = where or {}
        if tags:
            # ChromaDB metadata filtering for tags
            where_clause["tags"] = {"$in": tags}
        
        # Query ChromaDB
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where_clause if where_clause else None,
                include=["documents", "metadatas", "distances"],
            )
            
            # Convert to KnowledgeEntry objects
            entries = []
            if results["ids"] and results["ids"][0]:
                for i, entry_id in enumerate(results["ids"][0]):
                    document = results["documents"][0][i] if results["documents"] else None
                    metadata = results["metadatas"][0][i] if results["metadatas"] else {}
                    distance = results["distances"][0][i] if results["distances"] else None
                    
                    # Convert distance to similarity score (1 - distance for cosine similarity)
                    similarity_score = 1.0 - distance if distance is not None else None
                    
                    entry = KnowledgeEntry(
                        id=entry_id,
                        content=document or "",
                        source_type=metadata.get("source_type", "unknown"),
                        metadata=metadata,
                        tags=metadata.get("tags", []),
                        similarity_score=similarity_score,
                    )
                    entries.append(entry)
            
            self.logger.debug(f"Query returned {len(entries)} results")
            return entries
            
        except Exception as e:
            self.logger.error(f"Failed to query knowledge: {e}")
            raise
    
    async def get_similar_urls(
        self,
        url: str,
        n_results: int = 5,
    ) -> List[KnowledgeEntry]:
        """Get knowledge entries for similar URLs.
        
        Args:
            url: Target URL
            n_results: Number of results to return
            
        Returns:
            List of similar URL analyses
        """
        return await self.query_knowledge(
            query=f"URL analysis: {url}",
            n_results=n_results,
            tags=["seo_analysis", "url_analysis"],
        )
    
    async def get_keyword_insights(
        self,
        keyword: str,
        n_results: int = 10,
    ) -> List[KnowledgeEntry]:
        """Get keyword-related insights.
        
        Args:
            keyword: Target keyword
            n_results: Number of results to return
            
        Returns:
            List of keyword-related knowledge entries
        """
        return await self.query_knowledge(
            query=f"Keyword research: {keyword}",
            n_results=n_results,
            tags=["keyword_research", "search_data"],
        )
    
    async def get_competitor_insights(
        self,
        domain: str,
        n_results: int = 5,
    ) -> List[KnowledgeEntry]:
        """Get competitor analysis insights.
        
        Args:
            domain: Target domain
            n_results: Number of results to return
            
        Returns:
            List of competitor analysis entries
        """
        return await self.query_knowledge(
            query=f"Competitor analysis: {domain}",
            n_results=n_results,
            tags=["competitor_analysis", "competitive_intel"],
        )
    
    async def delete_knowledge(self, entry_id: str) -> bool:
        """Delete a knowledge entry.
        
        Args:
            entry_id: ID of entry to delete
            
        Returns:
            True if deleted successfully
        """
        if not self.collection:
            await self.initialize()
        
        try:
            self.collection.delete(ids=[entry_id])
            self.logger.debug(f"Deleted knowledge entry: {entry_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete knowledge entry {entry_id}: {e}")
            return False
    
    async def update_knowledge(
        self,
        entry_id: str,
        content: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Update a knowledge entry.
        
        Args:
            entry_id: ID of entry to update
            content: New content (optional)
            metadata: New metadata (optional)
            
        Returns:
            True if updated successfully
        """
        if not self.collection:
            await self.initialize()
        
        if not content and not metadata:
            return True  # Nothing to update
        
        try:
            # Get existing entry
            existing = self.collection.get(ids=[entry_id], include=["documents", "metadatas"])
            
            if not existing["ids"] or entry_id not in existing["ids"]:
                self.logger.warning(f"Knowledge entry not found: {entry_id}")
                return False
            
            # Prepare update data
            update_data = {}
            
            if content:
                # Generate new embedding for updated content
                embedding = self._generate_embedding(content)
                update_data["documents"] = [content]
                update_data["embeddings"] = [embedding]
            
            if metadata:
                # Update metadata with timestamp
                updated_metadata = existing["metadatas"][0].copy() if existing["metadatas"] else {}
                updated_metadata.update(metadata)
                updated_metadata["updated_at"] = datetime.utcnow().isoformat()
                update_data["metadatas"] = [updated_metadata]
            
            # Update in ChromaDB
            self.collection.update(ids=[entry_id], **update_data)
            
            self.logger.debug(f"Updated knowledge entry: {entry_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update knowledge entry {entry_id}: {e}")
            return False
    
    async def get_collection_stats(self) -> Dict[str, Any]:
        """Get collection statistics.
        
        Returns:
            Collection statistics
        """
        if not self.collection:
            await self.initialize()
        
        try:
            count = self.collection.count()
            
            # Get sample of metadata to analyze
            sample = self.collection.get(limit=100, include=["metadatas"])
            
            # Analyze source types and tags
            source_types = {}
            all_tags = {}
            
            if sample["metadatas"]:
                for metadata in sample["metadatas"]:
                    source_type = metadata.get("source_type", "unknown")
                    source_types[source_type] = source_types.get(source_type, 0) + 1
                    
                    tags = metadata.get("tags", [])
                    for tag in tags:
                        all_tags[tag] = all_tags.get(tag, 0) + 1
            
            return {
                "total_entries": count,
                "collection_name": self.collection_name,
                "source_types": source_types,
                "top_tags": dict(sorted(all_tags.items(), key=lambda x: x[1], reverse=True)[:10]),
                "embedding_model": self.embedding_model_name,
                "embedding_dimension": self.settings.embedding_dimension,
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get collection stats: {e}")
            return {"error": str(e)}
    
    async def close(self) -> None:
        """Close the vector store connection."""
        # ChromaDB client doesn't need explicit closing in current version
        self.client = None
        self.collection = None
        self.logger.info("Closed vector store connection")


# Convenience function for creating vector store instances
async def create_seo_vector_store(
    collection_name: Optional[str] = None,
    embedding_model: Optional[str] = None,
    persist_directory: Optional[str] = None,
) -> SEOVectorStore:
    """Create and initialize SEO vector store.
    
    Args:
        collection_name: Name of the ChromaDB collection
        embedding_model: Name of the sentence transformer model
        persist_directory: Directory for ChromaDB persistence
        
    Returns:
        Initialized SEOVectorStore instance
    """
    store = SEOVectorStore(
        collection_name=collection_name,
        embedding_model=embedding_model,
        persist_directory=persist_directory,
    )
    await store.initialize()
    return store