import pandas as pd
import os
import random
from datetime import datetime, timedelta

class DataProcessor:
    """
    A class to process, validate, and store competitor
    pricing data while maintaining historical records.
    """

    def __init__(self, storage_path="data/price_history.csv"):
        """
        Initialize the DataProcessor with a storage location.

        Args:
            storage_path (str): Path to the CSV file used for
                                storing historical price data.
        """

        self.storage_path = storage_path

        # Create storage directory if it does not exist
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)

    def _generate_mock_history(self, current_data):
        """
        Generate simulated historical pricing data when
        the database is created for the first time.

        Args:
            current_data (list): List of current product records.

        Returns:
            list: Simulated historical pricing records.
        """

        print("[INFO] Initializing new historical baseline database...")

        historical_records = []

        # Current reference time
        base_time = datetime.now()

        # Generate historical entries for each product
        for item in current_data:

            # Create 5 days of historical data
            for days_back in range(5, 0, -1):

                # Calculate past timestamp
                past_time = base_time - timedelta(days=days_back)

                # Generate random price variation
                # between -4% and +6%
                variance_factor = 1 + random.uniform(-0.04, 0.06)

                # Store generated historical record
                historical_records.append({
                    "timestamp": past_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "id": item["id"],
                    "title": item["title"],

                    # Adjust historical price using variance
                    "price": round(
                        item["price"] * variance_factor,
                        2
                    ),

                    "category": item["category"]
                })

        return historical_records

    def process_and_save(self, new_data):
        """
        Validate, normalize, and store incoming pricing data.
        Also initializes historical baseline data if storage
        does not already exist.

        Args:
            new_data (list): Incoming competitor pricing data.

        Returns:
            DataFrame: Updated historical dataset.
        """

        # Convert incoming data into pandas DataFrame
        df_new = pd.DataFrame(new_data)

        # Convert price column to numeric format
        # Invalid values become NaN
        df_new['price'] = pd.to_numeric(
            df_new['price'],
            errors='coerce'
        )

        # Keep only required columns
        df_new = df_new[
            ['timestamp', 'id', 'title', 'price', 'category']
        ]

        # -----------------------------------------
        # Initialize storage if file doesn't exist
        # -----------------------------------------
        if not os.path.isfile(self.storage_path):

            # Generate simulated historical dataset
            mock_history = self._generate_mock_history(new_data)

            # Convert mock data into DataFrame
            df_history = pd.DataFrame(mock_history)

            # Combine historical and current data
            df_final = pd.concat(
                [df_history, df_new],
                ignore_index=True
            )

            # Save complete dataset to CSV
            df_final.to_csv(self.storage_path, index=False)

        else:
            # Append only new records to existing file
            df_new.to_csv(
                self.storage_path,
                mode='a',
                header=False,
                index=False
            )

        # Load and return the updated dataset
        return pd.read_csv(self.storage_path)