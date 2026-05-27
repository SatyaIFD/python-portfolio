import numpy as np
import pandas as pd
from app.utils.logger import setup_logger

logger = setup_logger("pipeline.data_processor")

class DataProcessor:
    def __init__(self, window_size: int = 5):
        self.window_size = window_size
        logger.info(f"DataProcessor initialized with rolling window size: {window_size}")

    def generate_synthetic_data(self, n_samples: int = 1000) -> pd.DataFrame:
        """Generates a realistic industrial sensor timeline dataset."""
        logger.info(f"Generating {n_samples} structural sensor samples...")
        np.random.seed(42)
        
        timestamps = pd.date_range(start="2026-01-01", periods=n_samples, freq="min")
        
        # Base normal operation signals
        temperature = 65.0 + np.random.normal(0, 2.0, n_samples)
        vibration = 1.2 + np.random.normal(0, 0.15, n_samples)
        
        # Inject periodic degradation/anomalies (e.g., bearings wearing out)
        anomaly_indices = np.random.choice(range(self.window_size, n_samples), size=int(n_samples * 0.08), replace=False)
        
        for idx in anomaly_indices:
            temperature[idx:] += np.random.uniform(5.0, 15.0)  # Thermal spike
            vibration[idx:] += np.random.uniform(0.5, 1.5)     # Structural oscillation
            
        df = pd.DataFrame({
            "timestamp": timestamps,
            "temperature": temperature,
            "vibration": vibration
        })
        
        # Ground truth flag: If either feature crosses a dangerous threshold
        df["failure_target"] = ((df["temperature"] > 75.0) & (df["vibration"] > 1.8)).astype(int)
        return df

    def extract_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extracts rolling statistical window calculations from raw telemetry."""
        logger.info("Extracting rolling-window features...")
        df = df.sort_values("timestamp").copy()
        
        # Numeric operational parameters
        features = ["temperature", "vibration"]
        
        for feat in features:
            df[f"{feat}_roll_mean"] = df[feat].rolling(window=self.window_size, min_periods=1).mean()
            df[f"{feat}_roll_std"] = df[feat].rolling(window=self.window_size, min_periods=1).std().fillna(0)
            df[f"{feat}_gradient"] = np.gradient(df[feat].values)
            
        return df
