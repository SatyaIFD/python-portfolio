from app.trackers import PriceFetcher
from app.processor import DataProcessor
from app.visualizer import generate_report

def run_pipeline():
    """
    Execute the complete automated data pipeline workflow.

    Pipeline Stages:
        1. Extract live competitor pricing data
        2. Transform and store historical records
        3. Generate interactive visualization reports

    Returns:
        None
    """

    # -----------------------------------------
    # Display pipeline startup banner
    # -----------------------------------------
    print("\n==============================================")
    print("      LAUNCHING AUTOMATED DATA PIPELINE       ")
    print("==============================================\n")

    # -----------------------------------------
    # Step 1: Extract Data
    # -----------------------------------------

    # Create instance of PriceFetcher
    fetcher = PriceFetcher()

    # Fetch competitor product pricing data
    raw_data = fetcher.get_competitor_data()

    # Abort execution if no data is retrieved
    if not raw_data:
        print("[CRITICAL] Extraction engine failed. Aborting pipeline process.")
        return

    # -----------------------------------------
    # Step 2: Transform and Load Data
    # -----------------------------------------

    # Create instance of DataProcessor
    processor = DataProcessor()

    # Process, clean, and store the fetched data
    # Also returns updated historical dataset
    history_df = processor.process_and_save(raw_data)

    # -----------------------------------------
    # Step 3: Generate Visualization Report
    # -----------------------------------------

    # Create interactive price trend report
    generate_report(history_df)

    # -----------------------------------------
    # Display pipeline completion banner
    # -----------------------------------------
    print("\n==============================================")
    print("         PIPELINE RUN COMPLETED CLEANLY       ")
    print("==============================================\n")


# Run the pipeline only when this script
# is executed directly (not imported)
if __name__ == "__main__":
    run_pipeline()