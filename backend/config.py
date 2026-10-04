import os
from pathlib import Path
from dotenv import load_dotenv

# Base paths
BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
DATA_DIR = ROOT_DIR / "data"

# Load environment variables from .env if present
load_dotenv(BASE_DIR / ".env")

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "moviemine-secret-data-mining-key-2026")
    
    # MySQL connection string format:
    # mysql+pymysql://<username>:<password>@<host>:<port>/<database_name>
    MYSQL_USER = os.environ.get("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
    MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
    MYSQL_PORT = os.environ.get("MYSQL_PORT", "3306")
    MYSQL_DB = os.environ.get("MYSQL_DB", "moviemine")
    
    # Priority:
    # 1. DATABASE_URL environment variable if set
    # 2. MySQL connection string if reachable
    # 3. Fallback SQLite database for instant zero-config testing & demonstration
    DEFAULT_MYSQL_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    DATABASE_URL = os.environ.get("DATABASE_URL", DEFAULT_MYSQL_URL)
    
    FORCE_SQLITE = os.environ.get("FORCE_SQLITE", "false").lower() in ("true", "1", "yes")
    SQLITE_URL = f"sqlite:///{BASE_DIR / 'moviemine.db'}"

    # Default Data Mining Hyperparameters
    DEFAULT_K_CLUSTERS = 4
    DEFAULT_MIN_SUPPORT = 0.08
    DEFAULT_MIN_CONFIDENCE = 0.40
    DEFAULT_MIN_LIFT = 1.0

    # Hybrid Recommendation weights (Academic formulation)
    # Hybrid Score = 0.5 * Collaborative + 0.3 * Content + 0.2 * Popularity
    HYBRID_WEIGHT_COLLAB = 0.50
    HYBRID_WEIGHT_CONTENT = 0.30
    HYBRID_WEIGHT_POPULARITY = 0.20
