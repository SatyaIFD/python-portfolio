import os
import re
from typing import List, Dict, Any

from PyPDF2 import PdfReader
from docx import Document
from rank_bm25 import BM25Okapi
import nltk


# -------------------------------------------------------------------
# Ensure the NLTK tokenizer resources are available.
# If not already installed, download them silently.
# -------------------------------------------------------------------
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)


class SearchEngine:
    """
    A lightweight local document search engine using BM25 ranking.

    Supported file types:
    - .txt
    - .md
    - .pdf
    - .docx

    Features:
    - Recursively indexes documents from a directory
    - Extracts and tokenizes text
    - Builds a BM25 search index
    - Returns ranked search results with relevance scores
    """

    def __init__(self):
        """
        Initialize the search engine.

        Attributes:
            index:
                BM25 index object used for ranking documents.

            documents:
                Stores metadata and snippets for indexed documents.
        """
        self.index: BM25Okapi = None
        self.documents: List[Dict[str, Any]] = []

    def _clean_and_tokenize(self, text: str) -> List[str]:
        """
        Convert text into searchable tokens.

        Steps:
        1. Convert text to lowercase
        2. Extract alphanumeric words using regex

        Args:
            text: Raw input text

        Returns:
            List of cleaned tokens
        """
        text = text.lower()

        # Extract words while ignoring punctuation
        tokens = re.findall(r'\b\w+\b', text)

        return tokens

    def _extract_text(self, file_path: str) -> str:
        """
        Extract text content from a supported file type.

        Supported formats:
        - TXT / Markdown
        - PDF
        - DOCX

        Args:
            file_path: Absolute or relative path to the file

        Returns:
            Extracted text as a string.
            Returns empty string if extraction fails.
        """
        ext = os.path.splitext(file_path)[1].lower()
        text = ""

        try:
            # ---------------------------------------------------------
            # Plain text and Markdown files
            # ---------------------------------------------------------
            if ext in ['.txt', '.md']:
                with open(
                    file_path,
                    'r',
                    encoding='utf-8',
                    errors='ignore'
                ) as f:
                    text = f.read()

            # ---------------------------------------------------------
            # PDF documents
            # ---------------------------------------------------------
            elif ext == '.pdf':
                reader = PdfReader(file_path)

                # Combine text from all pages
                text = "".join(
                    [page.extract_text() or "" for page in reader.pages]
                )

            # ---------------------------------------------------------
            # Microsoft Word documents
            # ---------------------------------------------------------
            elif ext == '.docx':
                doc = Document(file_path)

                # Join all paragraph text with newlines
                text = "\n".join(
                    [para.text for para in doc.paragraphs]
                )

        except Exception as e:
            # In production, replace print with proper logging
            print(f"Error reading {file_path}: {e}")

        return text

    def index_directory(self, directory_path: str) -> int:
        """
        Scan a directory recursively and build the BM25 index.

        Process:
        1. Traverse all files
        2. Extract text from supported documents
        3. Tokenize content
        4. Build BM25 search index

        Args:
            directory_path:
                Path to the directory containing documents

        Returns:
            Number of successfully indexed documents

        Raises:
            ValueError:
                If the directory does not exist
        """

        # Validate directory existence
        if not os.path.exists(directory_path):
            raise ValueError(
                f"Directory path '{directory_path}' does not exist."
            )

        # Temporary storage for indexed documents
        new_documents = []

        # Tokenized text corpus used by BM25
        tokenized_corpus = []

        # Supported file extensions
        supported_exts = {'.txt', '.md', '.pdf', '.docx'}

        # -------------------------------------------------------------
        # Walk through all files recursively
        # -------------------------------------------------------------
        for root, _, files in os.walk(directory_path):

            for file in files:
                ext = os.path.splitext(file)[1].lower()

                # Skip unsupported file types
                if ext not in supported_exts:
                    continue

                # Generate absolute file path
                full_path = os.path.abspath(
                    os.path.join(root, file)
                )

                # Extract file content
                content = self._extract_text(full_path)

                # Skip empty documents
                if not content.strip():
                    continue

                # Store document metadata
                new_documents.append({
                    "title": file,
                    "path": full_path,

                    # Store short preview snippet
                    "content_snippet":
                        content[:200] + "..."
                        if len(content) > 200
                        else content
                })

                # Tokenize document for BM25 indexing
                tokenized_corpus.append(
                    self._clean_and_tokenize(content)
                )

        # -------------------------------------------------------------
        # Build BM25 index if documents were found
        # -------------------------------------------------------------
        if new_documents:
            self.documents = new_documents
            self.index = BM25Okapi(tokenized_corpus)

            return len(self.documents)

        return 0

    def search(
        self,
        query: str,
        top_n: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search indexed documents using BM25 ranking.

        Args:
            query:
                User search query

            top_n:
                Maximum number of results to return

        Returns:
            List of ranked search results containing:
            - title
            - file path
            - content snippet
            - BM25 relevance score
        """

        # Ensure index exists before searching
        if not self.index or not self.documents:
            return []

        # Tokenize search query
        query_tokens = self._clean_and_tokenize(query)

        # Compute BM25 relevance scores
        scores = self.index.get_scores(query_tokens)

        results = []

        # -------------------------------------------------------------
        # Pair each document with its relevance score
        # -------------------------------------------------------------
        for doc, score in zip(self.documents, scores):

            # Ignore completely irrelevant documents
            if score > 0:
                results.append({
                    "title": doc["title"],
                    "path": doc["path"],
                    "snippet": doc["content_snippet"],

                    # Round score for cleaner output
                    "score": round(float(score), 4)
                })

        # -------------------------------------------------------------
        # Sort results by descending relevance score
        # -------------------------------------------------------------
        results = sorted(
            results,
            key=lambda x: x["score"],
            reverse=True
        )

        # Return only top N matches
        return results[:top_n]