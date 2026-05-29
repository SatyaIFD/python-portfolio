import os
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from app import search_engine


# -------------------------------------------------------------------
# Initialize FastAPI application
# -------------------------------------------------------------------
app = FastAPI(
    title="Local Document Search API",
    description=(
        "A lightweight document search API using BM25 ranking "
        "to index and search local PDFs, DOCX, Markdown, and text files."
    ),
    version="1.0.0"
)


# ===================================================================
# Pydantic Request / Response Schemas
# ===================================================================

class IndexRequest(BaseModel):
    """
    Request body schema for indexing a directory.
    """

    directory_path: str = Field(
        ...,
        description="Absolute path of the local directory to index",
        example="/Users/username/Documents/Notes"
    )


class IndexResponse(BaseModel):
    """
    Response returned after indexing completes.
    """

    status: str
    message: str
    documents_indexed: int


class SearchResult(BaseModel):
    """
    Represents a single ranked search result.
    """

    title: str
    path: str
    snippet: str
    score: float


class SearchResponse(BaseModel):
    """
    Response schema for search queries.
    """

    query: str
    results_count: int
    results: List[SearchResult]


# ===================================================================
# API Endpoints
# ===================================================================

@app.post(
    "/api/v1/index",
    response_model=IndexResponse,
    tags=["Indexing"]
)
async def index_directory(payload: IndexRequest):
    """
    Scan and index all supported files inside a local directory.

    Supported formats:
    - TXT
    - Markdown
    - PDF
    - DOCX

    Steps:
    1. Validate directory path
    2. Extract document content
    3. Build BM25 index
    4. Store searchable metadata
    """

    # ---------------------------------------------------------------
    # Validate provided directory path
    # ---------------------------------------------------------------
    if not os.path.isdir(payload.directory_path):
        raise HTTPException(
            status_code=400,
            detail="Provided path is not a valid directory."
        )

    try:
        # Build the BM25 search index
        count = search_engine.index_directory(
            payload.directory_path
        )

        return IndexResponse(
            status="success",
            message=(
                f"Successfully indexed files inside "
                f"{payload.directory_path}"
            ),
            documents_indexed=count
        )

    except Exception as e:
        # Handle unexpected indexing errors
        raise HTTPException(
            status_code=500,
            detail=f"Failed to index directory: {str(e)}"
        )


@app.get(
    "/api/v1/search",
    response_model=SearchResponse,
    tags=["Search"]
)
async def search_documents(
    q: str = Query(
        ...,
        description="Search keyword or phrase"
    ),

    top_n: Optional[int] = Query(
        5,
        description="Maximum number of ranked results to return",
        ge=1,
        le=50
    )
):
    """
    Perform BM25-based ranked keyword search.

    Query Parameters:
    - q:
        Search phrase entered by the user

    - top_n:
        Maximum number of results returned
    """

    try:
        # Execute search against indexed documents
        results = search_engine.search(
            query=q,
            top_n=top_n
        )

        return SearchResponse(
            query=q,
            results_count=len(results),
            results=results
        )

    except Exception as e:
        # Handle runtime search failures
        raise HTTPException(
            status_code=500,
            detail=f"Search execution failed: {str(e)}"
        )


@app.get(
    "/api/v1/health",
    tags=["System"]
)
async def health_check():
    """
    Health-check endpoint.

    Useful for:
    - Monitoring
    - Deployment checks
    - Kubernetes readiness/liveness probes
    """

    return {
        "status": "healthy",

        # Total indexed files currently loaded in memory
        "total_indexed_files": len(search_engine.documents)
    }