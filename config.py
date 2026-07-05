import os

class Config:
    """Base configuration settings for the Flask Application."""
    # Flask application settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'hdi-predictor-secret-key-1829038290')
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    
    # Path configuration
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'dataset')
    MODEL_DIR = os.path.join(BASE_DIR, 'models')
    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    PLOTS_DIR = os.path.join(STATIC_DIR, 'plots')
    
    # Raw and processed dataset files
    RAW_DATA_URL = "https://hdr.undp.org/sites/default/files/2021-22_HDR/HDR21-22_Composite_indices_complete_time_series.csv"
    RAW_DATA_PATH = os.path.join(DATA_DIR, 'hdi_raw.csv')
    PROCESSED_DATA_PATH = os.path.join(DATA_DIR, 'hdi_processed.csv')
    
    # Model serialization files
    MODEL_PATH = os.path.join(MODEL_DIR, 'hdi_model.pkl')
    SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.pkl')

    @classmethod
    def init_app(cls):
        """Ensure directories exist."""
        for directory in [cls.DATA_DIR, cls.MODEL_DIR, cls.PLOTS_DIR]:
            os.makedirs(directory, exist_ok=True)
