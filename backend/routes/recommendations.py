from flask import Blueprint, request, jsonify
from database.db import SessionLocal
from services.mining_service import MiningService
from mining.content_based import ContentBasedRecommender
from mining.collaborative import CollaborativeFilteringRecommender

recommendations_bp = Blueprint("recommendations", __name__)

@recommendations_bp.route("/api/recommendations/<int:user_id>", methods=["GET"])
def get_recommendations_for_user(user_id):
    top_n = int(request.args.get("top_n", 8))
    db = SessionLocal()
    try:
        recs = MiningService.get_hybrid_recommendations(db, user_id, top_n=top_n)
        return jsonify(recs)
    finally:
        db.close()

@recommendations_bp.route("/api/recommendations/content-based", methods=["POST"])
def get_content_based_recommendations():
    data = request.get_json() or {}
    movie_id = data.get("movie_id")
    user_id = data.get("user_id")
    top_n = int(data.get("top_n", 6))

    db = SessionLocal()
    try:
        recommender = ContentBasedRecommender(db)
        if movie_id:
            results = recommender.get_similar_movies(int(movie_id), top_n=top_n)
        elif user_id:
            results = recommender.get_recommendations_for_user(int(user_id), top_n=top_n)
        else:
            return jsonify({"error": "Either movie_id or user_id is required."}), 400

        return jsonify(results)
    finally:
        db.close()

@recommendations_bp.route("/api/recommendations/collaborative", methods=["POST"])
def get_collaborative_recommendations():
    data = request.get_json() or {}
    user_id = data.get("user_id")
    top_n = int(data.get("top_n", 6))

    if not user_id:
        return jsonify({"error": "user_id is required."}), 400

    db = SessionLocal()
    try:
        recommender = CollaborativeFilteringRecommender(db)
        results = recommender.recommend_for_user(int(user_id), top_n=top_n)
        return jsonify(results)
    finally:
        db.close()
