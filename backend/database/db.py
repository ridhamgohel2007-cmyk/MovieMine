import sys
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from config import Config

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("MovieMine.DB")

Base = declarative_base()

def get_active_engine():
    """
    Attempts to connect to MySQL if configured.
    Falls back gracefully to SQLite if MySQL is not available or if FORCE_SQLITE is set.
    """
    if Config.FORCE_SQLITE:
        logger.info(f"Using SQLite database: {Config.SQLITE_URL}")
        return create_engine(Config.SQLITE_URL, echo=False, connect_args={"check_same_thread": False})

    # Test MySQL connection
    try:
        engine = create_engine(Config.DATABASE_URL, echo=False, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info(f"Successfully connected to MySQL database: {Config.DATABASE_URL.split('@')[-1]}")
        return engine
    except Exception as e:
        logger.warning(f"MySQL connection failed ({e}). Falling back to SQLite for zero-downtime execution.")
        logger.info(f"Fallback SQLite URL: {Config.SQLITE_URL}")
        return create_engine(Config.SQLITE_URL, echo=False, connect_args={"check_same_thread": False})

engine = get_active_engine()
session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal = scoped_session(session_factory)

def get_db():
    """Dependency helper for route handlers / services."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Create all relational tables defined in models."""
    from models.models import (
        User, Movie, Genre, MovieGenre, Rating,
        WatchHistory, Recommendation, Cluster,
        UserCluster, AssociationRuleModel
    )
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables verified / created successfully.")
