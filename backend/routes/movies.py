from flask import Blueprint, request, jsonify
from database.db import SessionLocal
from services.movie_service import MovieService

movies_bp = Blueprint("movies", __name__)

@movies_bp.route("/api/movies", methods=["GET"])
def get_movies():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 20))
    genre = request.args.get("genre", None)
    search = request.args.get("search", None)
    sort_by = request.args.get("sort_by", "rating")

    db = SessionLocal()
    try:
        data = MovieService.get_movies(db, page, per_page, genre, search, sort_by)
        return jsonify(data)
    finally:
        db.close()

@movies_bp.route("/api/movies/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    db = SessionLocal()
    try:
        movie = MovieService.get_movie_by_id(db, movie_id)
        if not movie:
            return jsonify({"error": "Movie not found"}), 404
        return jsonify(movie)
    finally:
        db.close()

@movies_bp.route("/api/movies/search", methods=["GET"])
def search_movies():
    q = request.args.get("q", "")
    db = SessionLocal()
    try:
        data = MovieService.get_movies(db, page=1, per_page=15, search=q)
        return jsonify(data["movies"])
    finally:
        db.close()

@movies_bp.route("/api/genres", methods=["GET"])
def get_genres():
    db = SessionLocal()
    try:
        genres = MovieService.get_genres(db)
        return jsonify(genres)
    finally:
        db.close()
