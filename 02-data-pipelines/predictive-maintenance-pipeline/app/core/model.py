import os
import joblib
from typing import Tuple, Dict, Any
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from app.utils.logger import setup_logger

# The rest of your model.py code remains exactly the same...

logger = setup_logger("pipeline.model")

class MaintenanceModel:
    def __init__(self, n_estimators: int = 100, max_depth: int = 7):
        self.model = RandomForestClassifier(
            n_estimators=n_estimators, 
            max_depth=max_depth, 
            random_state=42,
            class_weight="balanced"
        )
        self.feature_cols = [
            "temperature", "vibration", 
            "temperature_roll_mean", "temperature_roll_std", "temperature_gradient",
            "vibration_roll_mean", "vibration_roll_std", "vibration_gradient"
        ]
        logger.info("RandomForest Safety Classifier initialized successfully.")

    def train(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Splits, trains, and comprehensively evaluates the classifier performance."""
        X = df[self.feature_cols]
        y = df["failure_target"]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        logger.info(f"Training shapes: X_train={X_train.shape}, Class distribution={np.bincount(y_train)}")
        self.model.fit(X_train, y_train)
        
        # Run predictions for evaluation
        predictions = self.model.predict(X_test)
        
        metrics = {
            "report": classification_report(y_test, predictions, output_dict=True),
            "confusion_matrix": confusion_matrix(y_test, predictions).tolist()
        }
        
        # Log out human-readable evaluations
        logger.info("=== MODEL PERFORMANCE EVALUATION ===")
        print(classification_report(y_test, predictions))
        
        return metrics

    def predict(self, df: pd.DataFrame) -> np.ndarray:
        """Infuses live inference generation on engineered inputs."""
        return self.model.predict(df[self.feature_cols])

    def save_artifacts(self, directory: str = "artifacts") -> str:
        """Serializes the pipeline architecture into cold storage files."""
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, "predictive_model.joblib")
        joblib.dump(self.model, filepath)
        logger.info(f"Model checkpoint successfully written to {filepath}")
        return filepath

    def load_artifacts(self, filepath: str):
        """Restores model execution configurations directly from storage."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"No existing binary found at {filepath}")
        self.model = joblib.load(filepath)
        logger.info(f"Model successfully loaded back from context: {filepath}")
