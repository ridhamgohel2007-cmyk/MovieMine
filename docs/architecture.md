# MovieMine: System Architecture & Design Specification

> **Project Name:** MovieMine – Data Mining Based Movie Recommendation and User Preference Analysis System  
> **Course/Subject:** Data Mining & Business Intelligence / Machine Learning

---

## 1. System Overview & Multi-Tier Architecture

MovieMine is structured as a decoupled, multi-tier client-server architecture designed specifically for academic demonstration and reproducible Data Mining pipelines.

```mermaid
flowchart TD
    subgraph Client ["Frontend Tier (React + Vite + Recharts + Tailwind)"]
        UI_Home["Home Dashboard"]
        UI_Catalog["Movie Catalog & Filter"]
        UI_Recs["Multi-Model Recommendations"]
        UI_MineDash["Faculty Mining Dashboard"]
        UI_Cluster["K-Means 2D Scatter & Profiles"]
        UI_Apriori["Apriori Association Rules"]
        UI_Classifier["Supervised Preference Predictor"]
    end

    subgraph API_Gateway ["REST API Tier (Flask + Flask-CORS)"]
        Routes_Movies["/api/movies"]
        Routes_Recs["/api/recommendations"]
        Routes_Mining["/api/mining/*"]
        Routes_Users["/api/users"]
        Routes_Ratings["/api/ratings"]
    end

    subgraph Service_Tier ["Service & Business Logic Tier"]
        MovieSvc["MovieService"]
        MiningSvc["MiningService"]
    end

    subgraph Mining_Tier ["Data Mining Algorithmic Engine"]
        Preprocess["preprocessing.py (Matrix Pivot & Encoding)"]
        Collab["collaborative.py (User-User k-NN & Cosine)"]
        Content["content_based.py (TF-IDF & Cosine Vectors)"]
        ClusterEng["clustering.py (K-Means & 2D PCA)"]
        AssocEng["association.py (Apriori & Lift Metric)"]
        ClassEng["classification.py (Random Forest & Decision Tree)"]
    end

    subgraph Persistence ["Persistence & Database Tier"]
        ORM["SQLAlchemy 2.0 ORM"]
        DB[("MySQL 8.0 / SQLite (moviemine)")]
    end

    Client <-->|JSON over HTTP| API_Gateway
    API_Gateway --> Service_Tier
    Service_Tier --> Mining_Tier
    Mining_Tier --> Preprocess
    Preprocess --> ORM
    Service_Tier --> ORM
    ORM <--> DB
```

---

## 2. Relational Database Schema & Entity Relationships

The relational database enforces 3rd Normal Form (3NF) to support transactional integrity and analytical feature extraction.

```mermaid
erDiagram
    users ||--o{ ratings : "submits"
    users ||--o{ watch_history : "watches"
    users ||--o| user_clusters : "assigned_to"
    movies ||--o{ ratings : "receives"
    movies ||--o{ watch_history : "logged_in"
    movies ||--|{ movie_genres : "categorized_as"
    genres ||--|{ movie_genres : "contains"
    clusters ||--o{ user_clusters : "groups"
    users ||--o{ recommendations : "receives"
    movies ||--o{ recommendations : "recommended_in"

    users {
        int user_id PK
        string name
        string email UK
        int age
        string gender
        timestamp created_at
    }

    movies {
        int movie_id PK
        string title
        int release_year
        int duration
        text description
        string language
        decimal imdb_rating
        string poster_url
    }

    genres {
        int genre_id PK
        string genre_name UK
    }

    movie_genres {
        int movie_id PK, FK
        int genre_id PK, FK
    }

    ratings {
        int rating_id PK
        int user_id FK
        int movie_id FK
        decimal rating
        timestamp rating_date
    }

    watch_history {
        int history_id PK
        int user_id FK
        int movie_id FK
        timestamp watched_at
    }

    clusters {
        int cluster_id PK
        string cluster_name
        text description
        timestamp created_at
    }

    user_clusters {
        int user_id PK, FK
        int cluster_id FK
        timestamp assigned_at
    }

    association_rules {
        int rule_id PK
        string antecedent
        string consequent
        decimal support
        decimal confidence
        decimal lift
        timestamp generated_at
    }

    recommendations {
        int recommendation_id PK
        int user_id FK
        int movie_id FK
        string recommendation_type
        decimal score
        timestamp generated_at
    }
```

---

## 3. The 5-Stage KDD Architecture Mapping

| KDD Stage | MovieMine Implementation Details |
| :--- | :--- |
| **1. Data Selection** | Dynamic extraction of records from tables `users`, `movies`, `ratings`, and `watch_history` via SQLAlchemy queries. |
| **2. Preprocessing** | Missing duration imputation, deduplication of user-movie ratings, text cleaning of plot overviews, and transaction basket extraction. |
| **3. Transformation** | Multi-label genre binarization, user mean-centering ($r_{ui} - \bar{r}_u$), TF-IDF matrix generation, and sparse user-item pivot matrix creation. |
| **4. Data Mining** | Scikit-Learn `KMeans` user segmentation, MLxtend `apriori` rule mining, Pearson correlation Collaborative Filtering, Cosine Similarity Content-Based filtering, and Random Forest classification. |
| **5. Evaluation & Interpretation** | 2D PCA cluster projection, Support/Confidence/Lift rule metrics, hybrid score composition, and interactive Recharts dashboard rendering. |

---

## 4. REST API Specification

### Movie Endpoints
- `GET /api/movies?page=1&per_page=16&genre=Action&sort_by=rating`: Paginated catalog with filters.
- `GET /api/movies/<id>`: Full movie details, average mined user rating, and total rating counts.
- `GET /api/genres`: List of all 18 unique movie genres.

### Recommendation Endpoints
- `GET /api/recommendations/<user_id>?top_n=8`: Computes and returns Hybrid, Collaborative, Content-Based, and Cluster-Popular recommendations.
- `POST /api/recommendations/content-based`: Computes top similar movies using Cosine Similarity for a given `movie_id` or `user_id`.
- `POST /api/recommendations/collaborative`: Computes User-User Collaborative Filtering recommendations for a given `user_id`.

### Data Mining Endpoints
- `GET /api/mining/statistics`: System KPI metrics, database counts, and genre frequency distribution.
- `POST /api/mining/cluster-users`: Body: `{"k": 4}`. Runs K-Means, computes 2D PCA projection coordinates, saves clusters, and returns centroid profiles.
- `GET /api/mining/clusters`: Returns current audience clusters and member counts.
- `POST /api/mining/association-rules`: Body: `{"min_support": 0.08, "min_confidence": 0.40, "min_lift": 1.0}`. Runs Apriori on transaction baskets and saves discovered rules.
- `GET /api/mining/association-rules`: Returns mined association rules.
- `POST /api/mining/classify-preference`: Body: `{"user_id": 1, "movie_id": 10}`. Predicts binary preference ("LIKED" vs "UNLIKELY TO PREFER") using Random Forest and Decision Tree classifiers.
- `POST /api/mining/pipeline/run-all`: Executes full end-to-end data mining pipeline for faculty viva demonstration.
