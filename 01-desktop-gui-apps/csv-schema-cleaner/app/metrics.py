import pandas as pd
import numpy as np
import re

class DataProcessor:
    """
    Advanced engine for multi-rule validation and data cleaning.
    """

    def __init__(self, file_path):
        self.df = self.load_data(file_path)
        # Tracks anomalies: { "ColumnName": [list_of_invalid_indices] }
        self.anomaly_map = {}

    def load_data(self, path):
        """Loads CSV or JSON with basic error handling."""
        try:
            if path.endswith('.csv'):
                return pd.read_csv(path)
            elif path.endswith('.json'):
                return pd.read_json(path)
            else:
                raise ValueError("Unsupported file format. Please use CSV or JSON.")
        except Exception as e:
            print(f"Error loading file: {e}")
            return pd.DataFrame()

    def validate_all(self, rules_config):
        """
        Validates multiple columns at once.
        Args:
            rules_config (dict): e.g., {"Email_Col": "Email", "Age_Col": "No Nulls"}
        """
        self.anomaly_map = {} # Reset current anomalies
        for col, rule in rules_config.items():
            invalid_indices = self.validate_column(col, rule)
            if not invalid_indices.empty:
                self.anomaly_map[col] = invalid_indices.tolist()
        return self.anomaly_map

    def validate_column(self, col_name, rule_type):
        """
        Validation logic for specific data types.
        """
        if col_name not in self.df.columns:
            return pd.Index([])

        if rule_type == "Email":
            regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            # Convert to string to avoid errors with mixed types/NaNs
            mask = self.df[col_name].astype(str).str.contains(regex, na=False)
            return self.df[~mask].index

        elif rule_type == "No Nulls":
            return self.df[self.df[col_name].isna() | (self.df[col_name].astype(str).str.strip() == "")].index

        elif rule_type == "Numeric":
            # Identify rows that cannot be converted to a number
            is_numeric = pd.to_numeric(self.df[col_name], errors='coerce').notnull()
            return self.df[~is_numeric].index

        return pd.Index([])

    def get_health_report(self):
        """Returns a summary of errors found."""
        report = {col: len(idxs) for col, idxs in self.anomaly_map.items()}
        total_rows = len(self.df)
        dirty_rows = len(set([i for sublist in self.anomaly_map.values() for i in sublist]))
        
        return {
            "detail": report,
            "total_anomalies": dirty_rows,
            "clean_percentage": round(((total_rows - dirty_rows) / total_rows) * 100, 2) if total_rows > 0 else 0
        }

    def clean_and_export(self, output_path):
        """
        Drops all unique invalid rows tracked in anomaly_map and exports.
        """
        if not self.anomaly_map:
            # If no validation was run, just export the current df
            self.df.to_csv(output_path, index=False)
            return

        # Get unique indices from all failed rules
        all_bad_indices = set()
        for idx_list in self.anomaly_map.values():
            all_bad_indices.update(idx_list)

        cleaned_df = self.df.drop(index=list(all_bad_indices))
        cleaned_df.to_csv(output_path, index=False)
        return len(all_bad_indices) # Return count of dropped rows