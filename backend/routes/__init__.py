from routes.movies import movies_bp
from routes.users import users_bp
from routes.ratings import ratings_bp
from routes.recommendations import recommendations_bp
from routes.mining import mining_bp

__all__ = ["movies_bp", "users_bp", "ratings_bp", "recommendations_bp", "mining_bp"]
