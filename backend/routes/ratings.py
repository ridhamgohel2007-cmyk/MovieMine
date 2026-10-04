from flask import Blueprint, request, jsonify
from database.db import SessionLocal
from services.movie_service import MovieService

ratings_bp = Blueprint("ratings", __name__)

@ratings_bp.route("/api/ratings", methods=["POST"])
def add_rating():
    data = request.get_json() or {}
    user_id = data.get("user_id")
    movie_id = data.get("movie_id")
    rating_val = data.get("rating")

    if not user_id or not movie_id or rating_val is None:
        return jsonify({"error": "user_id, movie_id, and rating are required."}), 400

    try:
        rating_val = float(rating_val)
        if not (0.5 <= rating_val <= 5.0):
            return jsonify({"error": "Rating must be between 0.5 and 5.0."}), 400
    except ValueError:
        return jsonify({"error": "Invalid rating value."}), 400

    db = SessionLocal()
    try:
        success, msg = MovieService.add_or_update_rating(db, int(user_id), int(movie_id), rating_val)
        if not success:
            return jsonify({"error": msg}), 404
        return jsonify({"success": True, "message": msg})
    finally:
        db.close()

@ratings_bp.route("/api/watch-history", methods=["POST"])
def add_watch_history():
    data = request.get_json() or {}
    user_id = data.get("user_id")
    movie_id = data.get("movie_id")

    if not user_id or not movie_id:
        return jsonify({"error": "user_id and movie_id are required."}), 400

    db = SessionLocal()
    try:
        success, msg = MovieService.add_to_watch_history(db, int(user_id), int(movie_id))
        if not success:
            return jsonify({"error": msg}), 404
        return jsonify({"success": True, "message": msg})
    finally:
        db.close()
