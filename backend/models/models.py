import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Text,
    DateTime, ForeignKey, UniqueConstraint, Numeric
)
from sqlalchemy.orm import relationship
from database.db import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    age = Column(Integer, nullable=False)
    gender = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    ratings = relationship("Rating", back_populates="user", cascade="all, delete-orphan")
    watch_history = relationship("WatchHistory", back_populates="user", cascade="all, delete-orphan")
    cluster_membership = relationship("UserCluster", back_populates="user", uselist=False, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "age": self.age,
            "gender": self.gender,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "cluster": self.cluster_membership.cluster.to_dict() if self.cluster_membership and self.cluster_membership.cluster else None
        }

class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    release_year = Column(Integer, nullable=False, index=True)
    duration = Column(Integer, nullable=False)  # in minutes
    description = Column(Text, nullable=True)
    language = Column(String(50), default="English")
    imdb_rating = Column(Float, default=0.0)
    poster_url = Column(String(500), nullable=True)

    # Relationships
    genres = relationship("Genre", secondary="movie_genres", back_populates="movies")
    ratings = relationship("Rating", back_populates="movie", cascade="all, delete-orphan")
    watch_history = relationship("WatchHistory", back_populates="movie", cascade="all, delete-orphan")

    def to_dict(self, include_genres=True):
        data = {
            "movie_id": self.movie_id,
            "title": self.title,
            "release_year": self.release_year,
            "duration": self.duration,
            "description": self.description or "No synopsis available.",
            "language": self.language or "English",
            "imdb_rating": float(self.imdb_rating) if self.imdb_rating is not None else 0.0,
            "poster_url": self.poster_url or "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=600&q=80"
        }
        if include_genres:
            data["genres"] = [g.genre_name for g in self.genres]
        return data

class Genre(Base):
    __tablename__ = "genres"

    genre_id = Column(Integer, primary_key=True, autoincrement=True)
    genre_name = Column(String(50), unique=True, nullable=False, index=True)

    # Relationships
    movies = relationship("Movie", secondary="movie_genres", back_populates="genres")

    def to_dict(self):
        return {
            "genre_id": self.genre_id,
            "genre_name": self.genre_name
        }

class MovieGenre(Base):
    __tablename__ = "movie_genres"

    movie_id = Column(Integer, ForeignKey("movies.movie_id", ondelete="CASCADE"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.genre_id", ondelete="CASCADE"), primary_key=True)

class Rating(Base):
    __tablename__ = "ratings"

    rating_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    movie_id = Column(Integer, ForeignKey("movies.movie_id", ondelete="CASCADE"), nullable=False, index=True)
    rating = Column(Float, nullable=False)
    rating_date = Column(DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("user_id", "movie_id", name="uq_user_movie_rating"),
    )

    # Relationships
    user = relationship("User", back_populates="ratings")
    movie = relationship("Movie", back_populates="ratings")

    def to_dict(self):
        return {
            "rating_id": self.rating_id,
            "user_id": self.user_id,
            "movie_id": self.movie_id,
            "movie_title": self.movie.title if self.movie else None,
            "movie_poster": self.movie.poster_url if self.movie else None,
            "rating": float(self.rating),
            "rating_date": self.rating_date.isoformat() if self.rating_date else None
        }

class WatchHistory(Base):
    __tablename__ = "watch_history"

    history_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    movie_id = Column(Integer, ForeignKey("movies.movie_id", ondelete="CASCADE"), nullable=False, index=True)
    watched_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="watch_history")
    movie = relationship("Movie", back_populates="watch_history")

    def to_dict(self):
        return {
            "history_id": self.history_id,
            "user_id": self.user_id,
            "movie_id": self.movie_id,
            "movie_title": self.movie.title if self.movie else None,
            "watched_at": self.watched_at.isoformat() if self.watched_at else None
        }

class Recommendation(Base):
    __tablename__ = "recommendations"

    recommendation_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.movie_id", ondelete="CASCADE"), nullable=False)
    recommendation_type = Column(String(50), nullable=False)  # 'collaborative', 'content_based', 'hybrid'
    score = Column(Float, nullable=False)
    generated_at = Column(DateTime, default=datetime.datetime.utcnow)

    movie = relationship("Movie")

    def to_dict(self):
        return {
            "recommendation_id": self.recommendation_id,
            "user_id": self.user_id,
            "movie_id": self.movie_id,
            "movie": self.movie.to_dict() if self.movie else None,
            "recommendation_type": self.recommendation_type,
            "score": round(float(self.score), 4),
            "match_percentage": int(min(round(float(self.score) * 100), 100)),
            "generated_at": self.generated_at.isoformat() if self.generated_at else None
        }

class Cluster(Base):
    __tablename__ = "clusters"

    cluster_id = Column(Integer, primary_key=True)
    cluster_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    user_members = relationship("UserCluster", back_populates="cluster")

    def to_dict(self):
        return {
            "cluster_id": self.cluster_id,
            "cluster_name": self.cluster_name,
            "description": self.description
        }

class UserCluster(Base):
    __tablename__ = "user_clusters"

    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    cluster_id = Column(Integer, ForeignKey("clusters.cluster_id", ondelete="CASCADE"), nullable=False, index=True)

    user = relationship("User", back_populates="cluster_membership")
    cluster = relationship("Cluster", back_populates="user_members")

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "cluster_id": self.cluster_id,
            "cluster_name": self.cluster.cluster_name if self.cluster else None
        }

class AssociationRuleModel(Base):
    __tablename__ = "association_rules"

    rule_id = Column(Integer, primary_key=True, autoincrement=True)
    antecedent = Column(String(500), nullable=False)
    consequent = Column(String(500), nullable=False)
    support = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)
    lift = Column(Float, nullable=False)

    def to_dict(self):
        return {
            "rule_id": self.rule_id,
            "antecedent": self.antecedent,
            "consequent": self.consequent,
            "support": round(float(self.support), 4),
            "confidence": round(float(self.confidence), 4),
            "lift": round(float(self.lift), 4)
        }
