from flask import Blueprint, request, jsonify
from database.db import SessionLocal
from services.mining_service import MiningService
from mining.classification import MoviePreferenceClassifier
from config import Config

mining_bp = Blueprint("mining", __name__)

@mining_bp.route("/api/mining/statistics", methods=["GET"])
def get_mining_statistics():
    db = SessionLocal()
    try:
        stats = MiningService.get_statistics(db)
        return jsonify(stats)
    finally:
        db.close()

@mining_bp.route("/api/mining/cluster-users", methods=["POST"])
def cluster_users():
    data = request.get_json() or {}
    k = int(data.get("k", Config.DEFAULT_K_CLUSTERS))
    if k < 2 or k > 10:
        return jsonify({"error": "Number of clusters k must be between 2 and 10."}), 400

    db = SessionLocal()
    try:
        result = MiningService.run_clustering(db, k=k)
        return jsonify(result)
    finally:
        db.close()

@mining_bp.route("/api/mining/clusters", methods=["GET"])
def get_clusters():
    db = SessionLocal()
    try:
        clusters = MiningService.get_clusters(db)
        return jsonify(clusters)
    finally:
        db.close()

@mining_bp.route("/api/mining/association-rules", methods=["POST"])
def mine_association_rules():
    data = request.get_json() or {}
    min_support = float(data.get("min_support", Config.DEFAULT_MIN_SUPPORT))
    min_confidence = float(data.get("min_confidence", Config.DEFAULT_MIN_CONFIDENCE))
    min_lift = float(data.get("min_lift", Config.DEFAULT_MIN_LIFT))

    db = SessionLocal()
    try:
        result = MiningService.run_association_rules(
            db,
            min_support=min_support,
            min_confidence=min_confidence,
            min_lift=min_lift
        )
        return jsonify(result)
    finally:
        db.close()

@mining_bp.route("/api/mining/association-rules", methods=["GET"])
def get_association_rules():
    db = SessionLocal()
    try:
        rules = MiningService.get_association_rules(db)
        return jsonify(rules)
    finally:
        db.close()

@mining_bp.route("/api/mining/classify-preference", methods=["POST"])
def classify_preference():
    data = request.get_json() or {}
    user_id = data.get("user_id")
    movie_id = data.get("movie_id")

    if not user_id or not movie_id:
        return jsonify({"error": "user_id and movie_id are required."}), 400

    db = SessionLocal()
    try:
        classifier = MoviePreferenceClassifier(db)
        result = classifier.predict_user_movie_preference(int(user_id), int(movie_id))
        return jsonify(result)
    finally:
        db.close()

@mining_bp.route("/api/mining/pipeline/run-all", methods=["POST"])
def run_all_pipeline():
    """
    Executes full pipeline for faculty demonstration.
    """
    db = SessionLocal()
    try:
        results = MiningService.train_all_models(db)
        return jsonify(results)
    finally:
        db.close()
