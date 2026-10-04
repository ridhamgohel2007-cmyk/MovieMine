from sqlalchemy.orm import Session
from sqlalchemy import func, desc, text
from config import Config
from models.models import (
    User, Movie, Rating, WatchHistory, Cluster,
    UserCluster, AssociationRuleModel, Recommendation
)
from mining.clustering import UserClusteringEngine
from mining.association import AssociationRuleMiner
from mining.collaborative import CollaborativeFilteringRecommender
from mining.content_based import ContentBasedRecommender
from mining.classification import MoviePreferenceClassifier
from mining.preprocessing import get_movies_dataframe

class MiningService:
    @staticmethod
    def get_statistics(db: Session) -> dict:
        """
        Gathers comprehensive Data Mining overview statistics for the admin dashboard.
        """
        total_users = db.query(User).count()
        total_movies = db.query(Movie).count()
        total_ratings = db.query(Rating).count()
        total_watch = db.query(WatchHistory).count()
        avg_rating_val = db.query(func.avg(Rating.rating)).scalar() or 0.0

        cluster_count = db.query(Cluster).count()
        rules_count = db.query(AssociationRuleModel).count()
        rec_count = db.query(Recommendation).count()

        # Genre distribution
        movies_df = get_movies_dataframe(db)
        genre_counts = {}
        if not movies_df.empty:
            for genre_list in movies_df["genres"]:
                for g in genre_list:
                    genre_counts[g] = genre_counts.get(g, 0) + 1

        genre_chart_data = [
            {"genre": g, "count": cnt}
            for g, cnt in sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        ]

        return {
            "total_users": total_users,
            "total_movies": total_movies,
            "total_ratings": total_ratings,
            "total_watch_records": total_watch,
            "average_rating": round(float(avg_rating_val), 2),
            "clusters_count": cluster_count,
            "association_rules_count": rules_count,
            "cached_recommendations": rec_count,
            "genre_distribution": genre_chart_data
        }

    @staticmethod
    def run_clustering(db: Session, k: int = 4) -> dict:
        """Runs K-Means user clustering and stores clusters in DB."""
        engine = UserClusteringEngine(db)
        return engine.run_kmeans(k=k)

    @staticmethod
    def get_clusters(db: Session) -> list:
        """Returns existing clusters."""
        engine = UserClusteringEngine(db)
        return engine.get_existing_clusters()

    @staticmethod
    def run_association_rules(db: Session, min_support: float = 0.08, min_confidence: float = 0.40, min_lift: float = 1.0) -> dict:
        """Runs Apriori association rule mining."""
        miner = AssociationRuleMiner(db)
        return miner.mine_rules(
            min_support=min_support,
            min_confidence=min_confidence,
            min_lift=min_lift
        )

    @staticmethod
    def get_association_rules(db: Session) -> list:
        """Returns existing association rules from DB."""
        miner = AssociationRuleMiner(db)
        return miner.get_existing_rules()

    @staticmethod
    def get_hybrid_recommendations(db: Session, user_id: int, top_n: int = 10) -> dict:
        """
        Computes Collaborative, Content-Based, and Hybrid recommendations.
        Formula:
        Hybrid Score = 0.5 * Collab + 0.3 * Content + 0.2 * Popularity
        """
        collab_engine = CollaborativeFilteringRecommender(db)
        content_engine = ContentBasedRecommender(db)

        collab_recs = collab_engine.recommend_for_user(user_id, top_n=top_n * 2)
        content_recs = content_engine.get_recommendations_for_user(user_id, top_n=top_n * 2)

        # Build candidate score dictionary
        scores_map = {}
        movie_meta_map = {}

        # 1. Populate collaborative scores
        for r in collab_recs:
            mid = r["movie_id"]
            scores_map[mid] = {
                "collab": float(r["score"]),
                "content": 0.0,
                "popularity": float(r["imdb_rating"]) / 10.0
            }
            movie_meta_map[mid] = r

        # 2. Populate content-based scores
        for r in content_recs:
            mid = r["movie_id"]
            if mid not in scores_map:
                scores_map[mid] = {
                    "collab": 0.0,
                    "content": float(r["score"]),
                    "popularity": float(r["imdb_rating"]) / 10.0
                }
                movie_meta_map[mid] = r
            else:
                scores_map[mid]["content"] = float(r["score"])

        # 3. Compute Hybrid Weighted Scores
        hybrid_list = []
        for mid, scores in scores_map.items():
            final_score = (
                Config.HYBRID_WEIGHT_COLLAB * scores["collab"] +
                Config.HYBRID_WEIGHT_CONTENT * scores["content"] +
                Config.HYBRID_WEIGHT_POPULARITY * scores["popularity"]
            )
            meta = movie_meta_map[mid]
            hybrid_list.append({
                "movie_id": mid,
                "title": meta["title"],
                "release_year": meta["release_year"],
                "genres": meta["genres"],
                "imdb_rating": meta["imdb_rating"],
                "score": round(final_score, 4),
                "match_percentage": int(min(round(final_score * 100), 100)),
                "collab_component": round(scores["collab"], 3),
                "content_component": round(scores["content"], 3),
                "popularity_component": round(scores["popularity"], 3),
                "recommendation_method": "Hybrid Filtering (0.5 Collab + 0.3 Content + 0.2 Popularity)"
            })

        hybrid_list = sorted(hybrid_list, key=lambda x: x["score"], reverse=True)[:top_n]

        # 4. Save hybrid recommendations to DB recommendations cache
        try:
            db.query(Recommendation).filter(Recommendation.user_id == user_id).delete()
            for rec in hybrid_list:
                db.add(Recommendation(
                    user_id=user_id,
                    movie_id=rec["movie_id"],
                    recommendation_type="hybrid",
                    score=rec["score"]
                ))
            db.commit()
        except Exception:
            db.rollback()

        # 5. Cluster-popular movies: Find what users in the same cluster love
        cluster_recs = []
        user_c = db.query(UserCluster).filter(UserCluster.user_id == user_id).first()
        if user_c:
            cluster_user_ids = [uc.user_id for uc in db.query(UserCluster.user_id).filter(UserCluster.cluster_id == user_c.cluster_id).all()]
            if cluster_user_ids:
                cluster_top = db.query(
                    Rating.movie_id,
                    func.avg(Rating.rating).label("avg_rating"),
                    func.count(Rating.rating_id).label("cnt")
                ).filter(
                    Rating.user_id.in_(cluster_user_ids)
                ).group_by(Rating.movie_id).having(func.count(Rating.rating_id) >= 2).order_by(desc(func.avg(Rating.rating))).limit(top_n).all()

                for row in cluster_top:
                    m = db.query(Movie).filter(Movie.movie_id == row.movie_id).first()
                    if m:
                        cluster_recs.append({
                            "movie_id": m.movie_id,
                            "title": m.title,
                            "release_year": m.release_year,
                            "genres": [g.genre_name for g in m.genres],
                            "imdb_rating": float(m.imdb_rating or 0.0),
                            "score": round(float(row.avg_rating) / 5.0, 4),
                            "match_percentage": int(round((float(row.avg_rating) / 5.0) * 100)),
                            "recommendation_method": f"Popular in Your Cluster: {user_c.cluster.cluster_name if user_c.cluster else 'Cluster ' + str(user_c.cluster_id)}"
                        })

        return {
            "user_id": user_id,
            "collaborative": collab_recs[:top_n],
            "content_based": content_recs[:top_n],
            "hybrid": hybrid_list,
            "cluster_popular": cluster_recs
        }

    @staticmethod
    def train_all_models(db: Session) -> dict:
        """
        Executes full Data Mining Pipeline for Faculty Viva / Admin demo.
        """
        # 1. K-Means
        kmeans_res = MiningService.run_clustering(db, k=Config.DEFAULT_K_CLUSTERS)
        # 2. Association Rules
        apriori_res = MiningService.run_association_rules(
            db,
            min_support=Config.DEFAULT_MIN_SUPPORT,
            min_confidence=Config.DEFAULT_MIN_CONFIDENCE,
            min_lift=Config.DEFAULT_MIN_LIFT
        )
        # 3. Classifier
        classifier = MoviePreferenceClassifier(db)
        clf_res = classifier.train()

        return {
            "success": True,
            "message": "Full Data Mining Pipeline executed successfully!",
            "kmeans": kmeans_res,
            "association_rules": apriori_res,
            "classification": clf_res
        }
