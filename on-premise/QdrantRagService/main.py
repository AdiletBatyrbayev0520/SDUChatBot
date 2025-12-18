from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import os
import numpy as np
from typing import List, Optional
import logging
import uuid


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="RAG Service", description="Retrieval-Augmented Generation Service")


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    threshold: float = 0.7

class SearchResult(BaseModel):
    text: str
    score: float
    metadata: Optional[dict] = None

class SearchResponse(BaseModel):
    results: List[SearchResult]
    total_found: int

class Document(BaseModel):
    text: str
    metadata: Optional[dict] = None


qdrant_client = None
embedding_model = None
COLLECTION_NAME = "documents"

@app.on_event("startup")
async def startup_event():
    global qdrant_client, embedding_model
    
    try:
        
        qdrant_host = os.getenv("QDRANT_HOST", "localhost")
        qdrant_port = int(os.getenv("QDRANT_PORT", "6333"))
        
        qdrant_client = QdrantClient(host=qdrant_host, port=qdrant_port)
        logger.info(f"Connected to Qdrant at {qdrant_host}:{qdrant_port}")
        
        
        model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        embedding_model = SentenceTransformer(model_name)
        logger.info(f"Loaded embedding model: {model_name}")
        
        
        await create_collection_if_not_exists()
        
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise

async def create_collection_if_not_exists():
    try:
        collections = qdrant_client.get_collections()
        collection_names = [col.name for col in collections.collections]
        
        if COLLECTION_NAME not in collection_names:
            
            sample_embedding = embedding_model.encode(["test"])
            vector_size = len(sample_embedding[0])
            
            qdrant_client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )
            logger.info(f"Created collection '{COLLECTION_NAME}' with vector size {vector_size}")
        else:
            logger.info(f"Collection '{COLLECTION_NAME}' already exists")
            
    except Exception as e:
        logger.error(f"Error creating collection: {e}")
        raise

@app.get("/")
async def root():
    return {"message": "RAG Service is running", "status": "ok"}

@app.get("/health")
async def health_check():
    try:
        
        collections = qdrant_client.get_collections()
        return {
            "status": "healthy",
            "qdrant_connected": True,
            "embedding_model_loaded": embedding_model is not None,
            "collections_count": len(collections.collections)
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    try:
        
        query_embedding = embedding_model.encode([request.query])[0]
        
        
        search_results = qdrant_client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_embedding.tolist(),
            limit=request.top_k,
            score_threshold=request.threshold
        )
        
        
        results = []
        for hit in search_results:
            results.append(SearchResult(
                text=hit.payload.get("text", ""),
                score=hit.score,
                metadata=hit.payload.get("metadata", {})
            ))
        
        return SearchResponse(
            results=results,
            total_found=len(results)
        )
        
    except Exception as e:
        logger.error(f"Error during search: {e}")
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@app.post("/add_document")
async def add_document(document: Document):
    try:
        
        embedding = embedding_model.encode([document.text])[0]
        
        
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding.tolist(),
            payload={
                "text": document.text,
                "metadata": document.metadata or {}
            }
        )
        
        
        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=[point]
        )
        
        return {"message": "Document added successfully", "id": point.id}
        
    except Exception as e:
        logger.error(f"Error adding document: {e}")
        raise HTTPException(status_code=500, detail=f"Error adding document: {str(e)}")

@app.post("/add_documents")
async def add_documents(documents: List[Document]):
    try:
        points = []
        texts = [doc.text for doc in documents]
        
        
        embeddings = embedding_model.encode(texts)
        
        for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding.tolist(),
                payload={
                    "text": doc.text,
                    "metadata": doc.metadata or {}
                }
            )
            points.append(point)
        
        
        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
        
        return {
            "message": f"Successfully added {len(documents)} documents",
            "added_count": len(documents)
        }
        
    except Exception as e:
        logger.error(f"Error adding documents: {e}")
        raise HTTPException(status_code=500, detail=f"Error adding documents: {str(e)}")

@app.get("/collection/info")
async def get_collection_info():
    try:
        collection_info = qdrant_client.get_collection(COLLECTION_NAME)
        return {
            "collection_name": COLLECTION_NAME,
            "points_count": collection_info.points_count,
            "vector_size": collection_info.config.params.vectors.size,
            "distance_metric": collection_info.config.params.vectors.distance
        }
        
    except Exception as e:
        logger.error(f"Error getting collection info: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting collection info: {str(e)}")

@app.delete("/collection/clear")
async def clear_collection():
    try:
        qdrant_client.delete_collection(COLLECTION_NAME)
        await create_collection_if_not_exists()
        
        return {"message": "Collection cleared successfully"}
        
    except Exception as e:
        logger.error(f"Error clearing collection: {e}")
        raise HTTPException(status_code=500, detail=f"Error clearing collection: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)