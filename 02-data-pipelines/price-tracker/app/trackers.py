import requests
from datetime import datetime

class PriceFetcher:
    """
    A class to fetch live market exchange data and simulate
    competitor product pricing based on currency fluctuations.
    """

    def __init__(self):
        """
        Initialize the PriceFetcher with a public exchange-rate API.
        """
        
        # API endpoint providing live USD exchange rates
        self.api_url = "https://open.er-api.com/v6/latest/USD"

    def get_competitor_data(self):
        """
        Fetch live exchange-rate data and transform it into
        simulated product pricing information.

        Returns:
            list:
                - A list of product dictionaries with dynamically
                  calculated prices and timestamps.
                - An empty list if the API request fails.
        """

        try:
            # Display status message before fetching data
            print("[INFO] Fetching real-time market indices...")

            # Send GET request to exchange-rate API
            response = requests.get(self.api_url, timeout=10)

            # Raise exception if HTTP request fails
            response.raise_for_status()

            # Convert API response to Python dictionary
            raw_data = response.json()

            # Extract currency exchange rates
            rates = raw_data.get("rates", {})

            # Generate current timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # -----------------------------------------
            # Simulated competitor product pricing
            # -----------------------------------------
            # Product prices are dynamically adjusted
            # using exchange-rate fluctuations.

            tracked_products = [

                # Product 1: Price adjusted using EUR rate
                {
                    "id": "SKU-9921",
                    "title": "Enterprise Cloud Server Unit X1",
                    "category": "Electronics",

                    # Convert and adjust price based on EUR exchange rate
                    "price": round(
                        1200.50 * (1 / rates.get("EUR", 0.92)),
                        2
                    ),

                    "timestamp": timestamp
                },

                # Product 2: Price adjusted using GBP rate
                {
                    "id": "SKU-4412",
                    "title": "Crypto Mining Rig Element v4",
                    "category": "Electronics",

                    # Convert and adjust price based on GBP exchange rate
                    "price": round(
                        850.00 * (1 / rates.get("GBP", 0.78)),
                        2
                    ),

                    "timestamp": timestamp
                },

                # Product 3: Price adjusted using JPY rate
                {
                    "id": "SKU-1084",
                    "title": "Premium Imported Leather Component",
                    "category": "Raw Materials",

                    # Adjust price proportionally using JPY exchange rate
                    "price": round(
                        340.25 * (rates.get("JPY", 155.0) / 150.0),
                        2
                    ),

                    "timestamp": timestamp
                }
            ]

            # Return processed product pricing data
            return tracked_products

        except requests.exceptions.RequestException as e:

            # Handle API/network-related errors
            print(f"[ERROR] Failed to extract from public endpoint: {e}")

            # Return empty list if request fails
            return []