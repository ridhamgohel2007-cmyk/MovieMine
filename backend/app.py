import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from database.db import init_db
from routes import (
    movies_bp,
    users_bp,
    ratings_bp,
    recommendations_bp,
    mining_bp
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
)
logger = logging.getLogger("MovieMine.App")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for all frontend origins
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Initialize Database Schema
    try:
        init_db()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing database schema: {e}")

    # Register Blueprints
    app.register_blueprint(movies_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(ratings_bp)
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(mining_bp)

    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "healthy",
            "project": "MovieMine – Data Mining Based Movie Recommendation System",
            "version": "1.0.0"
        })

    # Error Handlers
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(e):
        logger.error(f"Internal server error: {e}")
        return jsonify({"error": "Internal server error occurred in Data Mining engine"}), 500

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting MovieMine Data Mining Server on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
