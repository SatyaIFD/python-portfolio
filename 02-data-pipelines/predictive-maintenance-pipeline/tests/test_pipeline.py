import unittest
import pandas as pd
from app.core.data_processor import DataProcessor
from app.core.model import MaintenanceModel

class TestPredictiveMaintenancePipeline(unittest.TestCase):
    def setUp(self):
        self.processor = DataProcessor(window_size=3)
        self.model_manager = MaintenanceModel()

    def test_data_generation_and_features(self):
        # Generate smaller data context frame
        df = self.processor.generate_synthetic_data(n_samples=50)
        self.assertEqual(len(df), 50)
        self.assertIn("temperature", df.columns)
        self.assertIn("vibration", df.columns)

        # Verify rolling transformations execute and insert without dropping indices
        transformed_df = self.processor.extract_features(df)
        self.assertIn("temperature_roll_mean", transformed_df.columns)
        self.assertIn("vibration_gradient", transformed_df.columns)
        self.assertEqual(len(transformed_df), 50)

    def test_model_training_cycle(self):
        df = self.processor.generate_synthetic_data(n_samples=100)
        transformed_df = self.processor.extract_features(df)
        
        metrics = self.model_manager.train(transformed_df)
        self.assertIn("accuracy", metrics["report"])
        self.assertIn("confusion_matrix", metrics)

if __name__ == "__main__":
    unittest.main()
