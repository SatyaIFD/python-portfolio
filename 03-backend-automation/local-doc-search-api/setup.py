from setuptools import setup, find_packages


# ===================================================================
# Package Configuration
# ===================================================================
#
# This setup.py file defines how the project is packaged,
# distributed, and installed using setuptools.
#
# Main Responsibilities:
# - Define package metadata
# - Specify Python version compatibility
# - List required dependencies
# - Discover project packages automatically
#
# Install locally:
#     pip install .
#
# Install in editable/development mode:
#     pip install -e .
#
# Build distribution package:
#     python setup.py sdist bdist_wheel
#
# ===================================================================


setup(
    # ---------------------------------------------------------------
    # Package Name
    # ---------------------------------------------------------------
    #
    # The installable package name shown in pip.
    #
    name="local-doc-search-api",

    # ---------------------------------------------------------------
    # Package Version
    # ---------------------------------------------------------------
    #
    # Semantic versioning format:
    # MAJOR.MINOR.PATCH
    #
    version="1.0.0",

    # ---------------------------------------------------------------
    # Author Information
    # ---------------------------------------------------------------
    author="Your Name",

    # ---------------------------------------------------------------
    # Project Description
    # ---------------------------------------------------------------
    #
    # Short summary displayed on package repositories.
    #
    description=(
        "A locally hosted FastAPI service that builds "
        "a keyword-based BM25 search index for local files."
    ),

    # ---------------------------------------------------------------
    # Automatically Discover Packages
    # ---------------------------------------------------------------
    #
    # Searches the project directory for Python packages
    # containing __init__.py files.
    #
    packages=find_packages(),

    # ---------------------------------------------------------------
    # Minimum Supported Python Version
    # ---------------------------------------------------------------
    #
    # Prevents installation on unsupported Python versions.
    #
    python_requires=">=3.9",

    # ---------------------------------------------------------------
    # Project Dependencies
    # ---------------------------------------------------------------
    #
    # These packages are automatically installed when
    # the project is installed via pip.
    #
    install_requires=[

        # FastAPI web framework
        "fastapi==0.110.0",

        # ASGI server for running FastAPI apps
        "uvicorn==0.28.0",

        # Data validation and serialization
        "pydantic==2.6.4",

        # PDF text extraction
        "PyPDF2==3.0.1",

        # Microsoft Word (.docx) parsing
        "python-docx==1.1.0",

        # BM25 ranking algorithm implementation
        "rank_bm25==0.2.2",

        # NLP tokenization utilities
        "nltk==3.8.1",
    ],
)