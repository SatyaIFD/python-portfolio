import pandas as pd
import numpy as np


class DataProcessor:
    """
    Utility class for loading, validating, and cleaning structured data
    from CSV or JSON files using pandas.
    """

    def __init__(self, file_path):
        # Load dataset immediately when object is created
        self.df = self.load_data(file_path)

    def load_data(self, path):
        """
        Load data from a CSV or JSON file into a pandas DataFrame.

        Args:
            path (str): File path to the dataset

        Returns:
            pd.DataFrame: Loaded dataset
        """
        if path.endswith('.csv'):
            return pd.read_csv(path)

        # Default to JSON if not CSV
        return pd.read_json(path)

    def validate_column(self, col_name, rule_type):
        """
        Validate a column based on a given rule and return indices
        of rows that FAIL validation.

        Args:
            col_name (str): Column to validate
            rule_type (str): Type of validation rule ("Email", "No Nulls")

        Returns:
            pd.Index: Indices of invalid rows
        """

        # Email format validation using regex
        if rule_type == "Email":
            regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'

            # Identify valid email entries
            mask = self.df[col_name].str.contains(regex, na=False)

            # Return rows that do NOT match the pattern
            return self.df[~mask].index

        # Check for missing/null values
        elif rule_type == "No Nulls":
            return self.df[self.df[col_name].isna()].index

        # If rule type is unsupported, return empty result
        return pd.Index([])

    def clean_and_export(self, path, drop_indices):
        """
        Remove invalid rows and export cleaned dataset to a CSV file.

        Args:
            path (str): Output file path
            drop_indices (list or pd.Index): Row indices to remove

        Returns:
            None
        """

        # Drop invalid rows from dataframe
        cleaned_df = self.df.drop(drop_indices)

        # Save cleaned dataset
        cleaned_df.to_csv(path, index=False)