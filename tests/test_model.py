import os
import unittest
import pandas as pd
import numpy as np
import joblib

# Add parent dir to path so tests can run from root
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import Config
import train_model

class TestModelPipeline(unittest.TestCase):
    
    def setUp(self):
        """Configure test environments."""
        # Use config locations
        self.processed_path = Config.PROCESSED_DATA_PATH
        self.model_path = Config.MODEL_PATH
        self.scaler_path = Config.SCALER_PATH

    def test_synthetic_data_generation(self):
        """Verifies synthetic dataset is created and features are properly structured."""
        # Run generator
        train_model.generate_synthetic_dataset()
        
        # Verify file exists
        self.assertTrue(os.path.exists(self.processed_path), "Processed dataset file should be generated.")
        
        # Read and check structure
        df = pd.read_csv(self.processed_path)
        self.assertFalse(df.empty, "Processed dataset should not be empty.")
        
        required_cols = ['country', 'year', 'life_expectancy', 'expected_years_schooling', 'mean_years_schooling', 'gni_per_capita', 'hdi']
        for col in required_cols:
            self.assertIn(col, df.columns, f"Column '{col}' must be present in dataset.")
            
        # Check bounds
        self.assertTrue((df['hdi'] >= 0.0).all() and (df['hdi'] <= 1.0).all(), "HDI values must be between 0.0 and 1.0.")
        self.assertTrue((df['life_expectancy'] >= 20.0).all(), "Life expectancy must be >= 20.")
        self.assertTrue((df['gni_per_capita'] >= 100.0).all(), "GNI per Capita must be >= 100.")

    def test_model_training_outputs(self):
        """Verifies that model training runs and serializes correct pickle binaries."""
        # Ensure processed dataset exists
        if not os.path.exists(self.processed_path):
            train_model.generate_synthetic_dataset()
            
        df = pd.read_csv(self.processed_path)
        
        # Train and save
        r2 = train_model.train_and_save_model(df)
        
        # Verify files are saved
        self.assertTrue(os.path.exists(self.model_path), "Model binary hdi_model.pkl should be created.")
        self.assertTrue(os.path.exists(self.scaler_path), "Scaler binary scaler.pkl should be created.")
        
        # Load and verify model prediction outputs
        model = joblib.load(self.model_path)
        scaler = joblib.load(self.scaler_path)
        
        # Test mock feature mapping
        # features order: life_expectancy, expected_years_schooling, mean_years_schooling, gni_per_capita
        mock_features = np.array([[78.0, 16.0, 12.0, 45000.0]])
        mock_scaled = scaler.transform(mock_features)
        pred_hdi = model.predict(mock_scaled)[0]
        
        self.assertIsInstance(float(pred_hdi), float, "Model prediction output should be float.")
        self.assertTrue(0.0 <= pred_hdi <= 1.0, f"Predicted HDI {pred_hdi} should be within logical limits (0.0 to 1.0).")

if __name__ == '__main__':
    unittest.main()
