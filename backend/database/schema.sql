-- ====================================================================
-- MovieMine – Data Mining Based Movie Recommendation & Preference Analysis System
-- Relational Database Schema (MySQL Compatible)
-- ====================================================================

-- Create Database if not exists
CREATE DATABASE IF NOT EXISTS moviemine CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE moviemine;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    age INT NOT NULL,
    gender VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_email (email)
) ENGINE=InnoDB;

-- 2. Movies Table
CREATE TABLE IF NOT EXISTS movies (
    movie_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_year INT NOT NULL,
    duration INT NOT NULL COMMENT 'Duration in minutes',
    description TEXT,
    language VARCHAR(50) DEFAULT 'English',
    imdb_rating DECIMAL(3, 1) DEFAULT 0.0,
    poster_url VARCHAR(500),
    INDEX idx_movie_title (title),
    INDEX idx_release_year (release_year)
) ENGINE=InnoDB;

-- 3. Genres Table
CREATE TABLE IF NOT EXISTS genres (
    genre_id INT AUTO_INCREMENT PRIMARY KEY,
    genre_name VARCHAR(50) NOT NULL UNIQUE,
    INDEX idx_genre_name (genre_name)
) ENGINE=InnoDB;

-- 4. Movie Genres Junction Table
CREATE TABLE IF NOT EXISTS movie_genres (
    movie_id INT NOT NULL,
    genre_id INT NOT NULL,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id) ON DELETE CASCADE,
    INDEX idx_mg_genre (genre_id)
) ENGINE=InnoDB;

-- 5. Ratings Table (User-Movie Rating Matrix Core)
CREATE TABLE IF NOT EXISTS ratings (
    rating_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    movie_id INT NOT NULL,
    rating DECIMAL(2, 1) NOT NULL CHECK (rating >= 0.5 AND rating <= 5.0),
    rating_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_user_movie_rating (user_id, movie_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
    INDEX idx_rating_user (user_id),
    INDEX idx_rating_movie (movie_id)
) ENGINE=InnoDB;

-- 6. Watch History Table (Transaction source for Association Rule Mining)
CREATE TABLE IF NOT EXISTS watch_history (
    history_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    movie_id INT NOT NULL,
    watched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
    INDEX idx_watch_user (user_id),
    INDEX idx_watch_movie (movie_id)
) ENGINE=InnoDB;

-- 7. Recommendations Cache Table
CREATE TABLE IF NOT EXISTS recommendations (
    recommendation_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    movie_id INT NOT NULL,
    recommendation_type VARCHAR(50) NOT NULL COMMENT 'collaborative, content_based, hybrid, cluster_popular',
    score DECIMAL(5, 4) NOT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
    INDEX idx_rec_user_type (user_id, recommendation_type)
) ENGINE=InnoDB;

-- 8. Clusters Table (K-Means User Segments)
CREATE TABLE IF NOT EXISTS clusters (
    cluster_id INT PRIMARY KEY,
    cluster_name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 9. User Clusters Junction Table
CREATE TABLE IF NOT EXISTS user_clusters (
    user_id INT PRIMARY KEY,
    cluster_id INT NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (cluster_id) REFERENCES clusters(cluster_id) ON DELETE CASCADE,
    INDEX idx_uc_cluster (cluster_id)
) ENGINE=InnoDB;

-- 10. Association Rules Table (Mined from Apriori Algorithm)
CREATE TABLE IF NOT EXISTS association_rules (
    rule_id INT AUTO_INCREMENT PRIMARY KEY,
    antecedent VARCHAR(500) NOT NULL COMMENT 'Comma-separated movie titles / itemset',
    consequent VARCHAR(500) NOT NULL COMMENT 'Comma-separated movie titles / itemset',
    support DECIMAL(6, 5) NOT NULL,
    confidence DECIMAL(6, 5) NOT NULL,
    lift DECIMAL(6, 5) NOT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_rule_lift (lift)
) ENGINE=InnoDB;
