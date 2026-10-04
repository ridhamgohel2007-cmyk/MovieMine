"""
MovieMine Data Mining Layer: Collaborative Filtering Engine
Academic Topic: Memory-Based Collaborative Filtering (User-User & Item-Item)

========================================================================
ACADEMIC FLOW:
INPUT          : User-Movie Rating Matrix R (users x movies)
PREPROCESSING  : 
                 1. Identify co-rated items between user pairs.
                 2. Subtract each user's mean rating (Mean-Centering) to eliminate rater bias:
                    s(u, i) = r(u, i) - mean(r_u)
ALGORITHM      : 
                 1. Compute Pearson / Adjusted Cosine Similarity between users:
                    sim(u, v) = sum((r_ui - r_u_mean)*(r_vi - r_v_mean)) / (sqrt(sum(r_ui - r_u_mean)^2) * sqrt(sum(r_vi - r_v_mean)^2))
                 2. Select K most similar neighbors (k-NN).
                 3. Predict rating for unrated candidate movie i:
                    r_pred(u, i) = r_u_mean + [ sum_{v in K} (sim(u, v) * (r_vi - r_v_mean)) / sum_{v in K} |sim(u, v)| ]
OUTPUT         : Predicted ratings on 1.0 - 5.0 scale, normalized match percentage.
INTERPRETATION : If user A and user B rated past movies similarly, user A will likely
                 appreciate movies highly rated by user B.
========================================================================
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session
from models.models import Rating, Movie
from mining.preprocessing import get_ratings_dataframe, get_movies_dataframe, create_user_movie_matrix

class CollaborativeFilteringRecommender:
    def __init__(self, db: Session, k_neighbors: int = 15):
        self.db = db
        self.k_neighbors = k_neighbors
        self._prepare_matrices()

    def _prepare_matrices(self):
        """
        Creates the rating pivot table, user means, and user similarity matrix.
        """
        self.ratings_df = get_ratings_dataframe(self.db)
        self.movies_df = get_movies_dataframe(self.db)

        if self.ratings_df.empty or self.movies_df.empty:
            self.matrix = pd.DataFrame()
            self.user_sim_df = pd.DataFrame()
            return

        # Pivot table: users x movies
        self.matrix = self.ratings_df.pivot(index="user_id", columns="movie_id", values="rating")
        
        # User mean ratings (ignoring NaNs)
        self.user_means = self.matrix.mean(axis=1)

        # Mean-centered matrix for accurate cosine similarity
        self.matrix_centered = self.matrix.sub(self.user_means, axis=0).fillna(0.0)

        # Pairwise Cosine Similarity between users
        sim_array = cosine_similarity(self.matrix_centered)
        self.user_sim_df = pd.DataFrame(
            sim_array,
            index=self.matrix.index,
            columns=self.matrix.index
        )

    def get_similar_users(self, user_id: int, top_k: int = 5) -> list:
        """
        Returns the top_k most similar users and their similarity scores.
        """
        if self.user_sim_df.empty or user_id not in self.user_sim_df.index:
            return []

        user_sims = self.user_sim_df.loc[user_id].drop(user_id).sort_values(ascending=False)
        top_users = user_sims.head(top_k)

        return [{
            "user_id": int(uid),
            "similarity_score": round(float(sim), 4),
            "similarity_percentage": int(min(round(float(sim) * 100), 100))
        } for uid, sim in top_users.items()]

    def recommend_for_user(self, user_id: int, top_n: int = 10) -> list:
        """
        Generates Collaborative Filtering recommendations for user_id.
        """
        if self.matrix.empty:
            return []

        # Cold start handling
        if user_id not in self.matrix.index:
            # Fallback to globally highest rated movies with >= 5 ratings
            rating_stats = self.ratings_df.groupby("movie_id").agg(
                mean_rating=("rating", "mean"),
                rating_count=("rating", "count")
            )
            top_rated = rating_stats[rating_stats["rating_count"] >= 3].sort_values(by="mean_rating", ascending=False).head(top_n)
            results = []
            for mid, row in top_rated.iterrows():
                m_info = self.movies_df[self.movies_df["movie_id"] == mid]
                if not m_info.empty:
                    m_row = m_info.iloc[0]
                    norm_score = float(row["mean_rating"]) / 5.0
                    results.append({
                        "movie_id": int(mid),
                        "title": m_row["title"],
                        "release_year": int(m_row["release_year"]),
                        "genres": m_row["genres"],
                        "imdb_rating": float(m_row["imdb_rating"]),
                        "score": round(norm_score, 4),
                        "predicted_rating": round(float(row["mean_rating"]), 2),
                        "match_percentage": int(round(norm_score * 100)),
                        "recommendation_method": "Collaborative Filtering (Popularity Fallback)"
                    })
            return results

        user_ratings = self.matrix.loc[user_id]
        unrated_movie_ids = user_ratings[user_ratings.isna()].index.tolist()

        if not unrated_movie_ids:
            return []

        # Find top k similar neighbors with positive similarity
        similar_users = self.user_sim_df.loc[user_id].drop(user_id)
        positive_neighbors = similar_users[similar_users > 0].sort_values(ascending=False).head(self.k_neighbors)

        if positive_neighbors.empty:
            # If no positive neighbors, fallback to top items
            return self.recommend_for_user(-999, top_n=top_n)

        u_mean = self.user_means.loc[user_id]
        predictions = []

        for movie_id in unrated_movie_ids:
            # Get ratings of neighbors who rated this movie
            neighbor_ratings = self.matrix.loc[positive_neighbors.index, movie_id].dropna()
            
            if neighbor_ratings.empty:
                continue

            active_neighbors = neighbor_ratings.index
            sim_weights = positive_neighbors.loc[active_neighbors]
            
            sim_sum = sim_weights.abs().sum()
            if sim_sum == 0:
                continue

            neighbor_means = self.user_means.loc[active_neighbors]
            weighted_diff = np.sum(sim_weights * (neighbor_ratings - neighbor_means))
            
            predicted_rating = u_mean + (weighted_diff / sim_sum)
            # Clip predicted rating to valid range [1.0, 5.0]
            predicted_rating = max(1.0, min(5.0, predicted_rating))

            predictions.append((movie_id, predicted_rating))

        # Sort descending by predicted rating
        predictions = sorted(predictions, key=lambda x: x[1], reverse=True)[:top_n]

        recommendations = []
        for mid, pred_score in predictions:
            m_info = self.movies_df[self.movies_df["movie_id"] == mid]
            if not m_info.empty:
                m_row = m_info.iloc[0]
                norm_score = pred_score / 5.0
                recommendations.append({
                    "movie_id": int(mid),
                    "title": m_row["title"],
                    "release_year": int(m_row["release_year"]),
                    "genres": m_row["genres"],
                    "imdb_rating": float(m_row["imdb_rating"]),
                    "score": round(norm_score, 4),
                    "predicted_rating": round(pred_score, 2),
                    "match_percentage": int(min(round(norm_score * 100), 100)),
                    "recommendation_method": "Collaborative Filtering (User-Based k-NN)"
                })

        return recommendations
