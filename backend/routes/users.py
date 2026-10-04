from flask import Blueprint, jsonify
from database.db import SessionLocal
from models.models import User, Rating, WatchHistory
from mining.preprocessing import build_user_genre_profiles

users_bp = Blueprint("users", __name__)

@users_bp.route("/api/users", methods=["GET"])
def get_users():
    """List users for persona selector in frontend."""
    db = SessionLocal()
    try:
        users = db.query(User).order_by(User.user_id.asc()).limit(150).all()
        return jsonify([u.to_dict() for u in users])
    finally:
        db.close()

@users_bp.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        data = user.to_dict()
        data["ratings_count"] = db.query(Rating).filter(Rating.user_id == user_id).count()
        data["watch_count"] = db.query(WatchHistory).filter(WatchHistory.user_id == user_id).count()
        return jsonify(data)
    finally:
        db.close()

@users_bp.route("/api/users/<int:user_id>/ratings", methods=["GET"])
def get_user_ratings(user_id):
    db = SessionLocal()
    try:
        ratings = db.query(Rating).filter(Rating.user_id == user_id).order_by(Rating.rating_date.desc()).all()
        return jsonify([r.to_dict() for r in ratings])
    finally:
        db.close()

@users_bp.route("/api/users/<int:user_id>/genre-preferences", methods=["GET"])
def get_user_genre_preferences(user_id):
    """
    Returns normalized genre preference percentages for user profile charts.
    """
    db = SessionLocal()
    try:
        profiles = build_user_genre_profiles(db)
        if profiles.empty or user_id not in profiles.index:
            return jsonify([])

        user_row = profiles.loc[user_id]
        chart_data = [
            {"genre": genre, "affinity": round(float(weight) * 100, 1)}
            for genre, weight in user_row.items() if weight > 0
        ]
        chart_data = sorted(chart_data, key=lambda x: x["affinity"], reverse=True)
        return jsonify(chart_data)
    finally:
        db.close()
