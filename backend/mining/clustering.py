"""
MovieMine Data Mining Layer: K-Means Clustering Engine
Academic Topic: Unsupervised Machine Learning & Customer / User Segmentation

========================================================================
ACADEMIC FLOW:
INPUT          : User feature matrix extracted from ratings, genres, and watch history
PREPROCESSING  : 
                 1. Calculate genre preference percentages for each user
                 2. Include behavioral indicators: average rating, total ratings count, watch count
                 3. Apply StandardScaler (zero mean, unit variance)
ALGORITHM      : 
                 K-Means Clustering:
                 Objective: Minimize within-cluster sum of squares (Inertia):
                 J = sum_{k=1}^K sum_{i in S_k} || x_i - mu_k ||^2
                 Also applies PCA (2 components) for 2D visual projection.
OUTPUT         : 
                 - Cluster assignment for each user
                 - Centroid vectors and dominant genres
                 - Dynamic academic cluster naming based on centroid characteristics
                 - 2D scatter coordinates (x, y) for Recharts visualization
INTERPRETATION : Automatically discovers natural audience personas without labeled ground truth.
========================================================================
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from models.models import User, Movie, Rating, WatchHistory, Cluster, UserCluster
from mining.preprocessing import (
    get_ratings_dataframe,
    get_movies_dataframe,
    build_user_genre_profiles
)

ROLE_CATALOG = [
    {
        "id": "scifi_action",
        "name": "Sci-Fi & Action Pioneer",
        "badge": "Sci-Fi & Action",
        "icon": "🚀",
        "keywords": ["action", "sci-fi", "adventure"],
        "description": "Devoted to high-octane blockbusters, mind-bending futuristic concepts, superhero sagas, and galactic exploration."
    },
    {
        "id": "classic_drama",
        "name": "Classic Drama & Cinephile Critic",
        "badge": "Classic Drama",
        "icon": "🎭",
        "keywords": ["drama", "biography", "history"],
        "description": "Aficionado of character studies, Academy Award masterpieces, deep human narratives, and historical epics."
    },
    {
        "id": "animation_family",
        "name": "Animation & Family Adventure Fan",
        "badge": "Animation & Family",
        "icon": "🎨",
        "keywords": ["animation", "family", "comedy"],
        "description": "Loves heartwarming animation, Pixar and Ghibli wonderlands, witty humor, and wholesome storytelling."
    },
    {
        "id": "crime_mystery",
        "name": "Mystery & Crime Thriller Sleuth",
        "badge": "Crime & Mystery",
        "icon": "🔍",
        "keywords": ["crime", "mystery", "thriller", "horror"],
        "description": "Drawn to psychological suspense, unsolved mysteries, noir crime investigations, and shocking plot twists."
    },
    {
        "id": "romance_music",
        "name": "Romance & Musical Dreamer",
        "badge": "Romance & Music",
        "icon": "💖",
        "keywords": ["romance", "music", "musical"],
        "description": "Celebrates emotional journeys, timeless love stories, poetic soundtracks, and uplifting musicals."
    }
]

def resolve_role_metadata(dominant_genre_names: list, cluster_index: int = 0, assigned_role_ids: set = None) -> dict:
    """
    Maps dominant genres to a unique, non-overlapping persona with badges, icons, and descriptions.
    """
    if assigned_role_ids is None:
        assigned_role_ids = set()

    g_str = " ".join(dominant_genre_names).lower()
    
    best_role = None
    best_score = -1

    for role in ROLE_CATALOG:
        if role["id"] in assigned_role_ids:
            continue
        # Check match count
        score = sum(2 if kw in g_str else 0 for kw in role["keywords"])
        if score > best_score:
            best_score = score
            best_role = role

    # Fallback to available unassigned role
    if not best_role or best_score <= 0:
        available = [r for r in ROLE_CATALOG if r["id"] not in assigned_role_ids]
        if available:
            best_role = available[cluster_index % len(available)]
        else:
            best_role = ROLE_CATALOG[cluster_index % len(ROLE_CATALOG)]

    assigned_role_ids.add(best_role["id"])
    return best_role

class UserClusteringEngine:
    def __init__(self, db: Session):
        self.db = db

    def extract_user_features(self) -> pd.DataFrame:
        """
        Extracts multi-dimensional feature matrix for all users in the database.
        """
        users = self.db.query(User).all()
        if not users:
            return pd.DataFrame()

        ratings_df = get_ratings_dataframe(self.db)
        genre_profiles = build_user_genre_profiles(self.db)

        # Basic user stats
        stats_list = []
        for u in users:
            u_ratings = ratings_df[ratings_df["user_id"] == u.user_id] if not ratings_df.empty else pd.DataFrame()
            avg_rating = float(u_ratings["rating"].mean()) if not u_ratings.empty else 3.0
            num_ratings = len(u_ratings)
            
            # Watch history count
            watch_count = self.db.query(WatchHistory).filter(WatchHistory.user_id == u.user_id).count()

            stats_list.append({
                "user_id": u.user_id,
                "name": u.name,
                "age": u.age,
                "gender": u.gender,
                "avg_rating": avg_rating,
                "num_ratings": num_ratings,
                "watch_count": watch_count
            })

        df_stats = pd.DataFrame(stats_list).set_index("user_id")

        # Join with genre preference vectors
        if not genre_profiles.empty:
            feature_df = df_stats.join(genre_profiles, how="left").fillna(0.0)
        else:
            feature_df = df_stats

        return feature_df

    def run_kmeans(self, k: int = 4, random_state: int = 42) -> dict:
        """
        Executes K-Means clustering, generates 2D PCA coordinates, dynamic cluster labels,
        and saves results to relational database tables 'clusters' and 'user_clusters'.
        """
        df_features = self.extract_user_features()
        if df_features.empty or len(df_features) < k:
            return {
                "success": False,
                "message": f"Insufficient users in database ({len(df_features)}) to form {k} clusters."
            }

        # Exclude demographic text fields from clustering space
        numeric_cols = [c for c in df_features.columns if c not in ["name", "gender"]]
        X = df_features[numeric_cols].values

        # 1. Standardization
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # 2. KMeans Algorithm
        kmeans = KMeans(n_clusters=k, random_state=random_state, n_init=10)
        labels = kmeans.fit_predict(X_scaled)
        df_features["cluster_id"] = labels

        # 3. PCA for 2D projection (Visualizing high-dimensional clusters in Recharts)
        pca = PCA(n_components=2, random_state=random_state)
        pca_coords = pca.fit_transform(X_scaled)
        df_features["pca_x"] = np.round(pca_coords[:, 0], 3)
        df_features["pca_y"] = np.round(pca_coords[:, 1], 3)

        # Identify genre columns (all columns except stats)
        stat_cols = ["name", "age", "gender", "avg_rating", "num_ratings", "watch_count", "cluster_id", "pca_x", "pca_y"]
        genre_cols = [c for c in df_features.columns if c not in stat_cols]

        # 4. Profile each cluster and assign academic titles
        cluster_summaries = []
        assigned_role_ids = set()
        
        # Clear previous cluster records in DB
        self.db.query(UserCluster).delete()
        self.db.query(Cluster).delete()
        self.db.commit()

        for c_id in range(k):
            cluster_users = df_features[df_features["cluster_id"] == c_id]
            user_count = len(cluster_users)
            mean_rating = round(float(cluster_users["avg_rating"].mean()), 2)
            mean_activity = round(float(cluster_users["num_ratings"].mean()), 1)

            # Determine dominant genres
            dominant_genres = []
            top_genre_names = []
            if genre_cols and not cluster_users.empty:
                genre_means = cluster_users[genre_cols].mean().sort_values(ascending=False)
                dominant_genres = [f"{g} ({round(val*100)}%)" for g, val in genre_means.head(3).items() if val > 0]
                top_genre_names = list(genre_means.head(3).index)
            else:
                top_genre_names = ["General"]

            # Role persona resolution
            role_meta = resolve_role_metadata(top_genre_names, c_id, assigned_role_ids)
            cluster_name = role_meta["name"]
            description = role_meta["description"]

            # Query top movies representative of this cluster
            c_uids = list(cluster_users.index)
            top_movies = self.get_cluster_top_movies(c_uids, limit=4)

            # Persist Cluster entity
            new_cluster = Cluster(
                cluster_id=c_id,
                cluster_name=cluster_name,
                description=description
            )
            self.db.add(new_cluster)

            cluster_summaries.append({
                "cluster_id": c_id,
                "cluster_name": cluster_name,
                "role_badge": role_meta["badge"],
                "role_icon": role_meta["icon"],
                "user_count": user_count,
                "percentage": round((user_count / len(df_features)) * 100, 1),
                "avg_rating": mean_rating,
                "avg_activity": mean_activity,
                "dominant_genres": dominant_genres,
                "description": description,
                "top_movies": top_movies
            })

        self.db.commit()

        # 5. Persist user cluster memberships
        user_points = []
        for uid, row in df_features.iterrows():
            c_id = int(row["cluster_id"])
            uc = UserCluster(user_id=int(uid), cluster_id=c_id)
            self.db.add(uc)

            user_points.append({
                "user_id": int(uid),
                "name": str(row["name"]),
                "cluster_id": c_id,
                "x": float(row["pca_x"]),
                "y": float(row["pca_y"]),
                "avg_rating": round(float(row["avg_rating"]), 2),
                "num_ratings": int(row["num_ratings"])
            })

        self.db.commit()

        return {
            "success": True,
            "k": k,
            "total_users": len(df_features),
            "inertia": round(float(kmeans.inertia_), 2),
            "clusters": cluster_summaries,
            "scatter_points": user_points
        }

    def get_cluster_top_movies(self, user_ids: list, limit: int = 4) -> list:
        """
        Finds the highest rated movies for a group of users belonging to the cluster.
        """
        if not user_ids:
            return []

        top_movie_ratings = (
            self.db.query(
                Rating.movie_id,
                func.avg(Rating.rating).label("avg_rating"),
                func.count(Rating.rating).label("rating_count")
            )
            .filter(Rating.user_id.in_(user_ids))
            .group_by(Rating.movie_id)
            .order_by(desc("avg_rating"), desc("rating_count"))
            .limit(limit * 2)
            .all()
        )

        movies_list = []
        for r in top_movie_ratings:
            m = self.db.query(Movie).filter(Movie.movie_id == r.movie_id).first()
            if m:
                movies_list.append({
                    "movie_id": m.movie_id,
                    "title": m.title,
                    "release_year": m.release_year,
                    "poster_url": m.poster_url,
                    "imdb_rating": float(m.imdb_rating or 0.0),
                    "cluster_rating": round(float(r.avg_rating), 1),
                    "genres": [g.genre_name for g in m.genres]
                })
            if len(movies_list) >= limit:
                break

        return movies_list

    def get_existing_clusters(self) -> list:
        """
        Retrieves saved clusters, their user distributions, and representative movies from DB.
        """
        clusters = self.db.query(Cluster).all()
        if not clusters:
            return []

        results = []
        total_users = self.db.query(User).count()

        for c in clusters:
            member_user_records = self.db.query(UserCluster).filter(UserCluster.cluster_id == c.cluster_id).all()
            member_uids = [uc.user_id for uc in member_user_records]
            member_count = len(member_uids)
            pct = round((member_count / total_users * 100), 1) if total_users > 0 else 0

            top_movies = self.get_cluster_top_movies(member_uids, limit=4)
            matched_role = next((r for r in ROLE_CATALOG if r["name"] == c.cluster_name), None)
            if not matched_role:
                matched_role = resolve_role_metadata([c.cluster_name], c.cluster_id)

            results.append({
                "cluster_id": c.cluster_id,
                "cluster_name": c.cluster_name,
                "role_badge": matched_role["badge"],
                "role_icon": matched_role["icon"],
                "description": c.description,
                "user_count": member_count,
                "percentage": pct,
                "top_movies": top_movies
            })

        return results
