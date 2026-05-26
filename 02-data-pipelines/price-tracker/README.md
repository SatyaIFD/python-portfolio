# Automated Competitor Price Tracker & Analyzer

## Technical Overview
An automated Extract-Transform-Load (ETL) analytics engine built to track pricing adjustments across changing product configurations. The app streams data points via live financial open API responses, calculates price normalization transformations across dataframes using Pandas, and auto-builds an interactive Plotly timeline profile dashboard.

## Architecture Design
- **`app/trackers.py`**: Interacts with remote endpoint targets to fetch data arrays.
- **`app/processor.py`**: Performs structural transformations, type sanitization, and saves to file storage.
- **`app/visualizer.py`**: Compiles structural records into visual metric outputs.

## Run Execution Flow
To launch the tool without package route failures, execute with your `PYTHONPATH` global variable pinned to the root project tree structure:

```bash
# Install package dependencies
uv pip install -r requirements.txt

# Run orchestration workflow 
PYTHONPATH=. uv run main.py