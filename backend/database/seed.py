"""
MovieMine Database Seeder Script
Loads realistic Kaggle / MovieLens processed data into MySQL or SQLite database.
Executes initial Data Mining pipelines (K-Means & Apriori).
"""

import os
import sys
import datetime
import pandas as pd
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(backend_dir))

from config import Config, DATA_DIR
from database.db import SessionLocal, init_db
from database.kaggle_loader import generate_full_dataset
from models.models import (
    User, Movie, Genre, MovieGenre, Rating,
    WatchHistory, Cluster, UserCluster, AssociationRuleModel
)
from services.mining_service import MiningService

def seed_database(force_refresh=True):
    print("=" * 65)
    print(">> MovieMine: Seeding Database with Kaggle/MovieLens Dataset")
    print("=" * 65)

    # 1. Initialize schema
    init_db()
    db = SessionLocal()

    try:
        # Check if CSV files exist, else generate them
        movies_csv = DATA_DIR / "movies.csv"
        users_csv = DATA_DIR / "users.csv"
        ratings_csv = DATA_DIR / "ratings.csv"
        watch_csv = DATA_DIR / "watch_history.csv"

        if force_refresh or not movies_csv.exists() or not users_csv.exists():
            print(f"[1/5] Generating Kaggle-derived processed CSVs in {DATA_DIR}...")
            generate_full_dataset(DATA_DIR)
        else:
            print(f"[1/5] Found existing dataset files in {DATA_DIR}...")

        # 2. Clear existing records in proper relational order
        print("[2/5] Cleaning existing database records...")
        db.query(AssociationRuleModel).delete()
        db.query(UserCluster).delete()
        db.query(Cluster).delete()
        db.query(WatchHistory).delete()
        db.query(Rating).delete()
        db.query(MovieGenre).delete()
        db.query(Movie).delete()
        db.query(Genre).delete()
        db.query(User).delete()
        db.commit()

        # 3. Load Movies and Genres
        print("[3/5] Inserting Movies and Genre junction records...")
        df_movies = pd.read_csv(movies_csv)
        
        # Collect unique genres
        all_genres = set()
        for g_str in df_movies["genres"].dropna():
            for g in str(g_str).split("|"):
                all_genres.add(g.strip())

        genre_obj_map = {}
        for g_name in sorted(list(all_genres)):
            g = Genre(genre_name=g_name)
            db.add(g)
            genre_obj_map[g_name] = g
        db.flush()

        for _, row in df_movies.iterrows():
            m = Movie(
                movie_id=int(row["movie_id"]),
                title=str(row["title"]),
                release_year=int(row["release_year"]),
                duration=int(row["duration"]),
                description=str(row["description"]),
                language=str(row["language"]),
                imdb_rating=float(row["imdb_rating"]),
                poster_url=str(row["poster_url"])
            )
            # Link genres
            if pd.notnull(row["genres"]):
                for g_name in str(row["genres"]).split("|"):
                    g_name = g_name.strip()
                    if g_name in genre_obj_map:
                        m.genres.append(genre_obj_map[g_name])
            db.add(m)
        db.commit()
        print(f"  [OK] {len(df_movies)} Movies and {len(genre_obj_map)} Genres inserted.")

        # 4. Load Users
        print("[4/5] Inserting Users, Ratings, and Watch History...")
        df_users = pd.read_csv(users_csv)
        for _, row in df_users.iterrows():
            u = User(
                user_id=int(row["user_id"]),
                name=str(row["name"]),
                email=str(row["email"]),
                age=int(row["age"]),
                gender=str(row["gender"]),
                created_at=datetime.datetime.strptime(str(row["created_at"]), "%Y-%m-%d %H:%M:%S")
            )
            db.add(u)
        db.commit()
        print(f"  [OK] {len(df_users)} Users inserted.")

        # Load Ratings
        df_ratings = pd.read_csv(ratings_csv)
        for _, row in df_ratings.iterrows():
            r = Rating(
                rating_id=int(row["rating_id"]),
                user_id=int(row["user_id"]),
                movie_id=int(row["movie_id"]),
                rating=float(row["rating"]),
                rating_date=datetime.datetime.strptime(str(row["rating_date"]), "%Y-%m-%d %H:%M:%S")
            )
            db.add(r)
        db.commit()
        print(f"  [OK] {len(df_ratings)} User Ratings populated.")

        # Load Watch History
        df_watch = pd.read_csv(watch_csv)
        for _, row in df_watch.iterrows():
            w = WatchHistory(
                history_id=int(row["history_id"]),
                user_id=int(row["user_id"]),
                movie_id=int(row["movie_id"]),
                watched_at=datetime.datetime.strptime(str(row["watched_at"]), "%Y-%m-%d %H:%M:%S")
            )
            db.add(w)
        db.commit()
        print(f"  [OK] {len(df_watch)} Watch History records populated.")

        # 5. Execute Initial Data Mining Pipeline
        print("[5/5] Executing initial Data Mining algorithms (K-Means & Apriori)...")
        pipeline_res = MiningService.train_all_models(db)
        print(f"  [OK] K-Means: {len(pipeline_res['kmeans'].get('clusters', []))} User Segments formed.")
        print(f"  [OK] Apriori: {pipeline_res['association_rules'].get('rules_count', 0)} Association Rules discovered.")
        print(f"  [OK] Classification: Supervised model trained ({pipeline_res['classification'].get('training_accuracy', '')} accuracy).")

        print("=" * 65)
        print("[SUCCESS] MovieMine Database successfully populated and ready for viva!")
        print("=" * 65)

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error during seeding: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
