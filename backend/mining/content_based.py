"""
MovieMine Data Mining Layer: Content-Based Recommendation Engine
Academic Topic: Information Retrieval & Vector Space Models

========================================================================
ACADEMIC FLOW:
INPUT          : Target Movie ID (or user's top-rated movie history)
PREPROCESSING  : Construct combined metadata soup (genres * 3 + description + language)
                 Fit TF-IDF Vectorizer (scikit-learn TfidfVectorizer)
ALGORITHM      : Pairwise Cosine Similarity:
                 CosineSim(A, B) = (A · B) / (||A|| * ||B||)
OUTPUT         : Top-N similar movies with metadata and cosine similarity scores
INTERPRETATION : Higher score (0.0 to 1.0) indicates high semantic/genre overlap
========================================================================
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session
from models.models import Movie, Rating
from mining.preprocessing import get_movies_dataframe

class ContentBasedRecommender:
    def __init__(self, db: Session):
        self.db = db
        self._build_similarity_matrix()

    def _build_similarity_matrix(self):
        """
        Builds the TF-IDF feature space and computes the movie-movie cosine similarity matrix.
        """
        self.movies_df = get_movies_dataframe(self.db)
        if self.movies_df.empty:
            self.similarity_matrix = np.array([])
            self.movie_id_to_idx = {}
            self.idx_to_movie_id = {}
            return

        # Metadata soup: boost genre weight by repeating genres, then append synopsis
        # e.g., "Action Sci-Fi Action Sci-Fi In a dystopian future..."
        soups = []
        for _, row in self.movies_df.iterrows():
            genre_boost = " ".join(row["genres"] * 3)
            desc = row["description"] if pd.notnull(row["description"]) else ""
            lang = row["language"] if pd.notnull(row["language"]) else ""
            soup = f"{genre_boost} {desc} {lang}".strip().lower()
            soups.append(soup)

        self.movies_df["soup"] = soups

        # Vectorization using TF-IDF
        self.tfidf = TfidfVectorizer(
            stop_words="english",
            max_features=5000,
            ngram_range=(1, 2)
        )
        tfidf_matrix = self.tfidf.fit_transform(self.movies_df["soup"])

        # Pairwise Cosine Similarity Matrix
        self.similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

        # Mapping dictionaries
        self.movie_id_to_idx = {mid: idx for idx, mid in enumerate(self.movies_df["movie_id"])}
        self.idx_to_movie_id = {idx: mid for idx, mid in enumerate(self.movies_df["movie_id"])}

    def get_similar_movies(self, movie_id: int, top_n: int = 10) -> list:
        """
        Recommends top_n similar movies for a given movie_id using Cosine Similarity.
        """
        if self.movies_df.empty or movie_id not in self.movie_id_to_idx:
            return []

        idx = self.movie_id_to_idx[movie_id]
        sim_scores = list(enumerate(self.similarity_matrix[idx]))

        # Sort descending by similarity score (excluding the movie itself)
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = [s for s in sim_scores if s[0] != idx][:top_n]

        results = []
        for match_idx, score in sim_scores:
            row = self.movies_df.iloc[match_idx]
            results.append({
                "movie_id": int(row["movie_id"]),
                "title": row["title"],
                "release_year": int(row["release_year"]),
                "genres": row["genres"],
                "imdb_rating": float(row["imdb_rating"]),
                "score": round(float(score), 4),
                "match_percentage": int(min(round(float(score) * 100), 100)),
                "recommendation_method": "Content-Based Filtering"
            })

        return results

    def get_recommendations_for_user(self, user_id: int, top_n: int = 10) -> list:
        """
        Recommends movies for a user by aggregating content similarity from their top-rated movies.
        """
        if self.movies_df.empty:
            return []

        # Find user's highest rated movies (rating >= 3.5)
        user_ratings = self.db.query(Rating).filter(
            Rating.user_id == user_id,
            Rating.rating >= 3.5
        ).order_by(Rating.rating.desc()).limit(5).all()

        if not user_ratings:
            # Cold-start fallback: return top rated movies by IMDb
            top_movies = self.movies_df.sort_values(by="imdb_rating", ascending=False).head(top_n)
            return [{
                "movie_id": int(r["movie_id"]),
                "title": r["title"],
                "release_year": int(r["release_year"]),
                "genres": r["genres"],
                "imdb_rating": float(r["imdb_rating"]),
                "score": round(float(r["imdb_rating"] / 10.0), 4),
                "match_percentage": int(round((r["imdb_rating"] / 10.0) * 100)),
                "recommendation_method": "Content-Based (Popularity Fallback)"
            } for _, r in top_movies.iterrows()]

        watched_movie_ids = {r.movie_id for r in self.db.query(Rating.movie_id).filter(Rating.user_id == user_id).all()}
        
        # Accumulate weighted similarity scores
        aggregated_scores = np.zeros(len(self.movies_df))
        for ur in user_ratings:
            if ur.movie_id in self.movie_id_to_idx:
                m_idx = self.movie_id_to_idx[ur.movie_id]
                weight = float(ur.rating) / 5.0
                aggregated_scores += self.similarity_matrix[m_idx] * weight

        # Sort indices
        candidate_indices = np.argsort(aggregated_scores)[::-1]
        
        recommendations = []
        for idx in candidate_indices:
            mid = self.idx_to_movie_id[idx]
            if mid not in watched_movie_ids:
                row = self.movies_df.iloc[idx]
                norm_score = min(float(aggregated_scores[idx]) / len(user_ratings), 1.0)
                recommendations.append({
                    "movie_id": int(row["movie_id"]),
                    "title": row["title"],
                    "release_year": int(row["release_year"]),
                    "genres": row["genres"],
                    "imdb_rating": float(row["imdb_rating"]),
                    "score": round(norm_score, 4),
                    "match_percentage": int(min(round(norm_score * 100), 100)),
                    "recommendation_method": "Content-Based Filtering"
                })
                if len(recommendations) >= top_n:
                    break

        return recommendations
