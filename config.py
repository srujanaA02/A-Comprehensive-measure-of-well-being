
import os


class Config:
    """Base configuration settings for the Flask Application."""

    # Security
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # PostgreSQL database configuration
    DATABASE_URL = os.environ.get("DATABASE_URL")

    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://", "postgresql://", 1
        )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300
    }

    # Flask settings
    DEBUG = os.environ.get(
        "FLASK_DEBUG", "False"
    ).lower() in ("true", "1", "t")

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # Path configuration
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "dataset")
    MODEL_DIR = os.path.join(BASE_DIR, "models")
    STATIC_DIR = os.path.join(BASE_DIR, "static")
    PLOTS_DIR = os.path.join(STATIC_DIR, "plots")

    # Dataset files
    RAW_DATA_URL = (
        "https://hdr.undp.org/sites/default/files/2021-22_HDR/"
        "HDR21-22_Composite_indices_complete_time_series.csv"
    )
    RAW_DATA_PATH = os.path.join(DATA_DIR, "hdi_raw.csv")
    PROCESSED_DATA_PATH = os.path.join(
        DATA_DIR, "hdi_processed.csv"
    )

    # ML model files
    MODEL_PATH = os.path.join(MODEL_DIR, "hdi_model.pkl")
    SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")

    @classmethod
    def init_app(cls):
        """Ensure required directories exist."""
        for directory in [
            cls.DATA_DIR,
            cls.MODEL_DIR,
            cls.PLOTS_DIR
        ]:
            os.makedirs(directory, exist_ok=True)
