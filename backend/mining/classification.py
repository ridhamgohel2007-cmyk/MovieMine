"""
MovieMine Data Mining Layer: Classification Engine
Academic Topic: Supervised Machine Learning (Decision Tree / Random Forest Classification)

========================================================================
ACADEMIC FLOW:
INPUT          : User Profile Features & Candidate Movie Metadata
PREPROCESSING  : 
                 Target Variable (y): 1 if Rating >= 3.5 (LIKED), else 0 (DISLIKED)
                 Feature Vector (X):
                 - user_avg_rating
                 - user_ratings_count
                 - genre_affinity_score (User's historical preference for this movie's genres)
                 - movie_imdb_rating
                 - movie_duration
                 - release_year
ALGORITHM      : 
                 Decision Tree Classifier (max_depth=4 for interpretability)
                 Random Forest Ensemble (n_estimators=50)
OUTPUT         : Prediction ("LIKED" vs "DISLIKED"), Confidence Probability,
                 Feature Importances / Decision Factors.
INTERPRETATION : Supervised model predicting explicit preference before recommendation.
========================================================================
"""

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sqlalchemy.orm import Session
from models.models import Rating, Movie, User
from mining.preprocessing import get_ratings_dataframe, get_movies_dataframe, build_user_genre_profiles

class MoviePreferenceClassifier:
    def __init__(self, db: Session):
        self.db = db
        self.model = None
        self.feature_names = [
            "user_avg_rating",
            "user_total_ratings",
            "genre_affinity",
            "movie_imdb_rating",
            "movie_duration",
            "movie_year"
        ]

    def _prepare_training_data(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Prepares training dataset from historic user ratings.
        """
        ratings_df = get_ratings_dataframe(self.db)
        movies_df = get_movies_dataframe(self.db)
        genre_profiles = build_user_genre_profiles(self.db)

        if ratings_df.empty or movies_df.empty or len(ratings_df) < 20:
            return np.array([]), np.array([])

        # Precompute user stats
        user_stats = ratings_df.groupby("user_id").agg(
            user_avg=("rating", "mean"),
            user_cnt=("rating", "count")
        )

        movies_indexed = movies_df.set_index("movie_id")

        X_rows = []
        y_labels = []

        for _, r in ratings_df.iterrows():
            uid = int(r["user_id"])
            mid = int(r["movie_id"])
            rating = float(r["rating"])

            if mid not in movies_indexed.index or uid not in user_stats.index:
                continue

            m_row = movies_indexed.loc[mid]
            u_avg = user_stats.loc[uid, "user_avg"]
            u_cnt = user_stats.loc[uid, "user_cnt"]

            # Compute genre affinity
            m_genres = m_row["genres"]
            affinity = 0.0
            if uid in genre_profiles.index and m_genres:
                user_prof = genre_profiles.loc[uid]
                matched_weights = [user_prof.get(g, 0.0) for g in m_genres if g in user_prof]
                affinity = float(np.mean(matched_weights)) if matched_weights else 0.0

            feat = [
                float(u_avg),
                float(u_cnt),
                float(affinity),
                float(m_row["imdb_rating"]),
                float(m_row["duration"]),
                float(m_row["release_year"])
            ]

            # Binary label: 1 if rating >= 3.5, else 0
            label = 1 if rating >= 3.5 else 0

            X_rows.append(feat)
            y_labels.append(label)

        return np.array(X_rows), np.array(y_labels)

    def train(self) -> dict:
        """
        Trains the Decision Tree and Random Forest classifiers.
        """
        X, y = self._prepare_training_data()
        if len(X) == 0:
            return {"success": False, "message": "Insufficient data to train classifier."}

        # Train Decision Tree
        self.dt_model = DecisionTreeClassifier(max_depth=4, random_state=42)
        self.dt_model.fit(X, y)

        # Train Random Forest
        self.rf_model = RandomForestClassifier(n_estimators=30, max_depth=5, random_state=42)
        self.rf_model.fit(X, y)

        # Feature importances
        importances = {
            name: round(float(imp) * 100, 1)
            for name, imp in zip(self.feature_names, self.rf_model.feature_importances_)
        }

        train_acc = round(float(self.rf_model.score(X, y)) * 100, 1)

        return {
            "success": True,
            "samples_trained": len(X),
            "training_accuracy": f"{train_acc}%",
            "feature_importances": importances,
            "algorithm": "Random Forest & Decision Tree"
        }

    def predict_user_movie_preference(self, user_id: int, movie_id: int) -> dict:
        """
        Predicts whether a user will like a specific movie.
        """
        user = self.db.query(User).filter(User.user_id == user_id).first()
        movie = self.db.query(Movie).filter(Movie.movie_id == movie_id).first()

        if not user or not movie:
            return {"success": False, "message": "User or Movie not found."}

        # Ensure model is trained
        if not hasattr(self, "rf_model") or self.rf_model is None:
            self.train()

        ratings_df = get_ratings_dataframe(self.db)
        u_ratings = ratings_df[ratings_df["user_id"] == user_id] if not ratings_df.empty else pd.DataFrame()
        u_avg = float(u_ratings["rating"].mean()) if not u_ratings.empty else 3.5
        u_cnt = len(u_ratings)

        genre_profiles = build_user_genre_profiles(self.db)
        m_genres = [g.genre_name for g in movie.genres]
        affinity = 0.0
        if user_id in genre_profiles.index and m_genres:
            user_prof = genre_profiles.loc[user_id]
            matched = [user_prof.get(g, 0.0) for g in m_genres if g in user_prof]
            affinity = float(np.mean(matched)) if matched else 0.0

        feat = np.array([[
            u_avg,
            u_cnt,
            affinity,
            float(movie.imdb_rating or 7.0),
            float(movie.duration or 120),
            float(movie.release_year or 2015)
        ]])

        prob = float(self.rf_model.predict_proba(feat)[0][1])
        prediction = "LIKED (Positive Preference)" if prob >= 0.50 else "UNLIKELY TO PREFER"

        return {
            "success": True,
            "user_id": user_id,
            "user_name": user.name,
            "movie_id": movie_id,
            "movie_title": movie.title,
            "prediction": prediction,
            "like_probability": round(prob, 4),
            "like_percentage": int(round(prob * 100)),
            "features_analyzed": {
                "user_avg_rating": round(u_avg, 2),
                "user_genre_affinity": f"{round(affinity * 100, 1)}%",
                "movie_imdb_rating": float(movie.imdb_rating or 0.0),
                "movie_genres": m_genres
            }
        }
