import os

import pytest

from app.core.engine import SearchEngine


# ===================================================================
# Pytest Fixtures
# ===================================================================

@pytest.fixture
def temp_text_dir(tmp_path):
    """
    Create a temporary directory containing sample documents.

    This fixture simulates a small local document collection
    that can be indexed during testing.

    Files created:
    - python_tips.txt
    - cooking_recipe.md

    Args:
        tmp_path:
            Built-in pytest temporary directory fixture

    Returns:
        Path to the temporary document directory as a string
    """

    # Create temporary directory
    d = tmp_path / "documents"
    d.mkdir()

    # ---------------------------------------------------------------
    # Sample technical document
    # ---------------------------------------------------------------
    f1 = d / "python_tips.txt"
    f1.write_text(
        "Python is an amazing dynamic programming language "
        "for FastAPI development."
    )

    # ---------------------------------------------------------------
    # Sample cooking document
    # ---------------------------------------------------------------
    f2 = d / "cooking_recipe.md"
    f2.write_text(
        "How to bake the perfect sourdough bread "
        "using local flour."
    )

    return str(d)


# ===================================================================
# Test Cases
# ===================================================================

def test_indexing_and_searching(temp_text_dir):
    """
    Test the complete indexing and search workflow.

    Test Flow:
    1. Create search engine instance
    2. Index temporary documents
    3. Verify indexing count
    4. Execute search query
    5. Validate returned results

    Expected Outcome:
    - Both files should be indexed
    - The FastAPI-related document should rank highest
    - Search score should be positive
    """

    # Initialize search engine
    engine = SearchEngine()

    # ---------------------------------------------------------------
    # Index the temporary document directory
    # ---------------------------------------------------------------
    indexed_count = engine.index_directory(temp_text_dir)

    # Ensure both documents were indexed successfully
    assert indexed_count == 2

    # ---------------------------------------------------------------
    # Perform relevance search
    # ---------------------------------------------------------------
    results = engine.search(
        "FastAPI language",
        top_n=1
    )

    # Ensure exactly one result is returned
    assert len(results) == 1

    # Verify the most relevant document is returned
    assert results[0]["title"] == "python_tips.txt"

    # Ensure BM25 relevance score is positive
    assert results[0]["score"] > 0.0