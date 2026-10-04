import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, func
from models.models import Movie, Genre, Rating, WatchHistory, User

class MovieService:
    @staticmethod
    def get_movies(db: Session, page: int = 1, per_page: int = 20, genre: str = None, search: str = None, sort_by: str = "rating"):
        """
        Retrieves paginated movies with optional genre filter, title search, and sorting.
        """
        query = db.query(Movie)

        if genre and genre != "All":
            query = query.join(Movie.genres).filter(Genre.genre_name == genre)

        if search:
            search_term = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Movie.title.ilike(search_term),
                    Movie.description.ilike(search_term)
                )
            )

        if sort_by == "rating":
            query = query.order_by(desc(Movie.imdb_rating))
        elif sort_by == "year":
            query = query.order_by(desc(Movie.release_year))
        elif sort_by == "title":
            query = query.order_by(Movie.title.asc())
        else:
            query = query.order_by(Movie.movie_id.asc())

        total = query.count()
        offset = (page - 1) * per_page
        movies = query.offset(offset).limit(per_page).all()

        return {
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page,
            "movies": [m.to_dict() for m in movies]
        }

    @staticmethod
    def get_movie_by_id(db: Session, movie_id: int):
        """
        Fetches full details of a movie including ratings count and average.
        """
        movie = db.query(Movie).filter(Movie.movie_id == movie_id).first()
        if not movie:
            return None

        # Aggregate user ratings
        stats = db.query(
            func.avg(Rating.rating),
            func.count(Rating.rating_id)
        ).filter(Rating.movie_id == movie_id).first()

        avg_user_rating = round(float(stats[0]), 2) if stats and stats[0] is not None else float(movie.imdb_rating or 0.0)
        user_ratings_count = int(stats[1]) if stats and stats[1] is not None else 0

        data = movie.to_dict()
        data["user_avg_rating"] = avg_user_rating
        data["user_ratings_count"] = user_ratings_count
        return data

    @staticmethod
    def get_genres(db: Session):
        """Returns all distinct movie genres."""
        genres = db.query(Genre).order_by(Genre.genre_name.asc()).all()
        return [g.to_dict() for g in genres]

    @staticmethod
    def add_or_update_rating(db: Session, user_id: int, movie_id: int, rating_val: float):
        """
        Adds or updates a user rating for a movie.
        """
        # Validate rating
        rating_val = max(0.5, min(5.0, float(rating_val)))

        user = db.query(User).filter(User.user_id == user_id).first()
        movie = db.query(Movie).filter(Movie.movie_id == movie_id).first()
        if not user or not movie:
            return False, "User or Movie not found"

        existing = db.query(Rating).filter(
            Rating.user_id == user_id,
            Rating.movie_id == movie_id
        ).first()

        if existing:
            existing.rating = rating_val
            existing.rating_date = datetime.datetime.utcnow()
        else:
            new_rating = Rating(
                user_id=user_id,
                movie_id=movie_id,
                rating=rating_val
            )
            db.add(new_rating)

        # Also add to watch history if not present
        watched = db.query(WatchHistory).filter(
            WatchHistory.user_id == user_id,
            WatchHistory.movie_id == movie_id
        ).first()
        if not watched:
            db.add(WatchHistory(user_id=user_id, movie_id=movie_id))

        db.commit()
        return True, "Rating recorded successfully"

    @staticmethod
    def add_to_watch_history(db: Session, user_id: int, movie_id: int):
        """
        Records that a user watched a movie.
        """
        user = db.query(User).filter(User.user_id == user_id).first()
        movie = db.query(Movie).filter(Movie.movie_id == movie_id).first()
        if not user or not movie:
            return False, "User or Movie not found"

        existing = db.query(WatchHistory).filter(
            WatchHistory.user_id == user_id,
            WatchHistory.movie_id == movie_id
        ).first()

        if not existing:
            db.add(WatchHistory(user_id=user_id, movie_id=movie_id))
            db.commit()

        return True, "Watch history recorded"
