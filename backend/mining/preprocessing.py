"""
MovieMine Data Mining Layer: Preprocessing Module
Academic Stage: KDD (Knowledge Discovery in Databases) - Data Cleaning & Transformation

Pipeline:
1. Extraction: Load raw data from relational database into Pandas DataFrames.
2. Cleaning: Impute missing values, drop duplicates, sanitize text fields.
3. Transformation: 
   - Encode categorical features (genres into one-hot multi-label representations).
   - Normalize user ratings (Min-Max scaling and user mean-centering).
   - Construct sparse User-Movie Rating Matrix.
   - Build User Preference Profiles across all movie genres.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sqlalchemy.orm import Session
from models.models import User, Movie, Rating, Genre, MovieGenre, WatchHistory

def get_movies_dataframe(db: Session) -> pd.DataFrame:
    """
    Extracts movies and their associated genres from the database into a clean DataFrame.
    """
    movies = db.query(Movie).all()
    if not movies:
        return pd.DataFrame()

    records = []
    for m in movies:
        genres = [g.genre_name for g in m.genres]
        records.append({
            "movie_id": m.movie_id,
            "title": m.title,
            "release_year": m.release_year,
            "duration": m.duration,
            "description": m.description or "",
            "language": m.language or "English",
            "imdb_rating": float(m.imdb_rating or 0.0),
            "genres": genres,
            "genre_str": " ".join(genres)
        })

    df = pd.DataFrame(records)
    # Deduplicate by movie_id
    df = df.drop_duplicates(subset=["movie_id"])
    # Impute missing imdb ratings with median
    if df["imdb_rating"].isnull().any():
        df["imdb_rating"] = df["imdb_rating"].fillna(df["imdb_rating"].median())
    return df

def get_ratings_dataframe(db: Session) -> pd.DataFrame:
    """
    Extracts ratings from the database into a DataFrame and removes duplicates.
    """
    ratings = db.query(Rating).all()
    if not ratings:
        return pd.DataFrame(columns=["rating_id", "user_id", "movie_id", "rating"])

    records = [{
        "rating_id": r.rating_id,
        "user_id": r.user_id,
        "movie_id": r.movie_id,
        "rating": float(r.rating)
    } for r in ratings]

    df = pd.DataFrame(records)
    df = df.drop_duplicates(subset=["user_id", "movie_id"])
    return df

def create_user_movie_matrix(ratings_df: pd.DataFrame, fill_value: float = 0.0) -> pd.DataFrame:
    """
    Constructs the User x Movie Rating Pivot Matrix.
    
    Rows: user_id
    Columns: movie_id
    Values: rating (0.5 to 5.0)
    """
    if ratings_df.empty:
        return pd.DataFrame()

    pivot = ratings_df.pivot(index="user_id", columns="movie_id", values="rating")
    if fill_value is not None:
        pivot = pivot.fillna(fill_value)
    return pivot

def create_genre_indicator_matrix(movies_df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a binary one-hot matrix of movies and genres.
    Rows: movie_id
    Columns: genre names
    Values: 1 if movie belongs to genre, else 0
    """
    if movies_df.empty:
        return pd.DataFrame()

    all_genres = sorted(list({g for sublist in movies_df["genres"] for g in sublist}))
    genre_data = []

    for _, row in movies_df.iterrows():
        genre_row = {g: 1 if g in row["genres"] else 0 for g in all_genres}
        genre_row["movie_id"] = row["movie_id"]
        genre_data.append(genre_row)

    df_genre = pd.DataFrame(genre_data).set_index("movie_id")
    return df_genre

def build_user_genre_profiles(db: Session) -> pd.DataFrame:
    """
    Builds a normalized preference score vector for each user across all genres.
    
    Mathematical Formulation:
    For user u and genre g:
    Preference(u, g) = sum_{m in Watched(u)} (Rating(u, m) * HasGenre(m, g)) / TotalGenreWeights(u)
    
    Output: DataFrame with rows as user_id and columns as normalized genre weights [0, 1].
    """
    ratings_df = get_ratings_dataframe(db)
    movies_df = get_movies_dataframe(db)

    if ratings_df.empty or movies_df.empty:
        return pd.DataFrame()

    genre_matrix = create_genre_indicator_matrix(movies_df)
    
    # Merge ratings with movie genre binary flags
    merged = ratings_df.merge(genre_matrix, on="movie_id", how="inner")
    
    genre_cols = [c for c in genre_matrix.columns]
    
    # Weight each genre by user rating
    for col in genre_cols:
        merged[col] = merged[col] * merged["rating"]

    user_profiles = merged.groupby("user_id")[genre_cols].sum()
    
    # Normalize rows using L1 norm so sum across genres = 1 (or MinMax)
    user_totals = user_profiles.sum(axis=1)
    user_totals[user_totals == 0] = 1.0  # avoid division by zero
    normalized_profiles = user_profiles.div(user_totals, axis=0)

    return normalized_profiles
