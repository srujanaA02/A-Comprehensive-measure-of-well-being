import os
import unittest
import json

# Add parent dir to path so tests can run from root
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Ensure dataset and models are present for app.py initialization
from config import Config
import train_model
Config.init_app()
if not os.path.exists(Config.PROCESSED_DATA_PATH):
    train_model.generate_synthetic_dataset()
if not os.path.exists(Config.MODEL_PATH) or not os.path.exists(Config.SCALER_PATH):
    df = pd = train_model.pd.read_csv(Config.PROCESSED_DATA_PATH)
    train_model.train_and_save_model(df)

from app import app

class TestFlaskBackend(unittest.TestCase):
    
    def setUp(self):
        """Initialize test client."""
        self.app = app.test_client()
        self.app.testing = True
        # Set up authenticated session by default
        with self.app.session_transaction() as sess:
            sess['logged_in'] = True

    def test_dashboard_route(self):
        """Verifies dashboard responds successfully."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Human Development Index Predictor', response.data)
        self.assertIn(b'Total Countries Tracked', response.data)

    def test_about_route(self):
        """Verifies about page loads successfully."""
        response = self.app.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'HDI Computation Methodology', response.data)

    def test_invalid_404_handler(self):
        """Verifies custom 404 is served for invalid paths."""
        response = self.app.get('/some-non-existent-route')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Page Not Found', response.data)

    def test_api_countries_endpoint(self):
        """Verifies API responds with list of countries."""
        response = self.app.get('/api/countries')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('countries', data)
        self.assertIsInstance(data['countries'], list)

    def test_api_stats_endpoint(self):
        """Verifies API responds with statistics dictionary."""
        response = self.app.get('/api/stats')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('total_countries', data)
        self.assertIn('avg_hdi', data)

    def test_prediction_successful(self):
        """Verifies prediction executes correctly with valid arguments."""
        form_data = {
            'country': 'Germany',
            'life_expectancy': '81.3',
            'expected_years_schooling': '17.0',
            'mean_years_schooling': '14.1',
            'gni_per_capita': '54000'
        }
        response = self.app.post('/predict', data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Estimated Human Development Index', response.data)
        self.assertIn(b'Germany', response.data)

    def test_prediction_invalid_fields(self):
        """Verifies prediction fails (400) if bounds are violated."""
        # 1. Invalid life expectancy (too high)
        form_data = {
            'country': 'Custom Country',
            'life_expectancy': '150.0', # Out of bounds (20-100)
            'expected_years_schooling': '12.0',
            'mean_years_schooling': '8.0',
            'gni_per_capita': '25000'
        }
        response = self.app.post('/predict', data=form_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Validation Error', response.data)
        
        # 2. Non-numeric inputs
        form_data_text = {
            'country': 'Custom Country',
            'life_expectancy': 'string_val',
            'expected_years_schooling': '12.0',
            'mean_years_schooling': '8.0',
            'gni_per_capita': '25000'
        }
        response = self.app.post('/predict', data=form_data_text)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Values must be numeric', response.data)

if __name__ == '__main__':
    unittest.main()
