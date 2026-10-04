# MovieMine – Data Mining Based Movie Recommendation and User Preference Analysis System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Backend-Flask%203.1-black.svg)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/Frontend-React%2019%20%2B%20Vite-61dafb.svg)](https://react.dev/)
[![TailwindCSS](https://img.shields.io/badge/CSS-Tailwind%20v4-38bdf8.svg)](https://tailwindcss.com/)
[![Database](https://img.shields.io/badge/Database-MySQL%20%7C%20SQLite-00758f.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/Academic-College%20Data%20Mining%20Mini%20Project-success.svg)]()

> A database-driven Data Mining college project built for academic viva demonstration. MovieMine stores real-world user interactions, ratings, and catalog metadata in a normalized relational database, preprocesses the data, and applies multiple foundational Data Mining algorithms with live interactive dashboards.

---

## 📌 Kaggle Dataset Provenance & Attribution

The dataset ingested and processed by MovieMine is sourced and curated from official open datasets:

1. **The Movies Dataset (Kaggle):**  
   🔗 **Link:** [https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset)  
   *Metadata extracted from TMDB and MovieLens covering 225 curated famous movies across 18 genres.*
2. **MovieLens Small Latest Dataset (Kaggle / GroupLens Research):**  
   🔗 **Link:** [https://www.kaggle.com/datasets/shubhammehta21/movie-lens-small-latest-dataset](https://www.kaggle.com/datasets/shubhammehta21/movie-lens-small-latest-dataset)  
   🔗 **Official GroupLens:** [https://grouplens.org/datasets/movielens/latest/](https://grouplens.org/datasets/movielens/latest/)  
   *Real rating interactions processed through the KDD pipeline into 120 user personas, 2,560 ratings, and 1,819 watch logs.*

---

## 🚀 Key Data Mining Techniques Implemented

| Data Mining Technique | Algorithmic Formulation | Academic Purpose |
| :--- | :--- | :--- |
| **A. Collaborative Filtering** | Adjusted Cosine / Pearson Correlation on Mean-Centered Pivot Matrix + $k$-NN | Predicts unrated items based on similar user preferences |
| **B. Content-Based Filtering** | TF-IDF (Unigrams + Bigrams) & Pairwise Cosine Similarity | Measures thematic and genre overlap between movies |
| **C. K-Means Clustering** | Minimizes WCSS Inertia $J = \sum \sum \|\mathbf{x} - \boldsymbol{\mu}\|^2$ with 2D PCA | Unsupervised audience segmentation into distinct personas |
| **D. Association Rule Mining** | Apriori Frequent Itemsets (Support, Confidence, Lift) | Discovers frequent co-viewing patterns in transaction baskets |
| **E. Supervised Classification** | Decision Tree (`max_depth=4`) & Random Forest Ensemble | Predicts whether user $X$ will LIKE candidate movie $Y$ |
| **F. Hybrid Recommendation** | $\text{Score} = 0.5 \times \text{Collab} + 0.3 \times \text{Content} + 0.2 \times \text{Popularity}$ | Solves cold-start and sparsity limitations |

---

## 🛠️ Technology Stack

- **Backend:** Python 3.10+, Flask, SQLAlchemy 2.0 ORM, PyMySQL
- **Data Science & Mining:** Pandas, NumPy, Scikit-Learn, MLxtend
- **Database:** MySQL 8.0 (with automatic zero-downtime fallback to SQLite `moviemine.db`)
- **Frontend:** React 19, Vite, Tailwind CSS v4, Lucide Icons, Recharts (Bar, Pie, Scatter)
- **API Architecture:** RESTful JSON API with CORS support

---

## 📂 Project Architecture

```
MovieMine/
├── backend/
│   ├── app.py                      # Flask Application entry point & Blueprint registration
│   ├── config.py                   # Configuration (MySQL / SQLite database URI & hyperparameters)
│   ├── requirements.txt            # Python dependencies
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py               # 10 SQLAlchemy Relational ORM models
│   ├── database/
│   │   ├── db.py                   # Engine, scoped session, init_db()
│   │   ├── schema.sql              # MySQL DDL relational schema script
│   │   ├── kaggle_loader.py        # Kaggle/MovieLens processor & synthetic seed generator
│   │   ├── seed.py                 # Automatic database populator & mining runner
│   │   └── mysql_setup.py          # MySQL migration & setup utility
│   ├── mining/
│   │   ├── __init__.py
│   │   ├── preprocessing.py        # Data cleaning, pivot matrix, and L1 genre profiles
│   │   ├── collaborative.py        # User-User k-NN & Pearson correlation
│   │   ├── content_based.py        # TF-IDF & Cosine Similarity vector space
│   │   ├── clustering.py           # K-Means clustering & 2D PCA projection
│   │   ├── association.py          # Apriori frequent patterns & association rules
│   │   └── classification.py       # Decision Tree & Random Forest preference classifier
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── movies.py               # Movie catalog, search, pagination, genres
│   │   ├── users.py                # User profiles, ratings, genre preference vectors
│   │   ├── ratings.py              # Rating submission & watch history
│   │   ├── recommendations.py      # Hybrid, Collaborative, Content-based endpoints
│   │   └── mining.py               # Stats, clustering runner, Apriori runner, pipeline
│   └── services/
│       ├── __init__.py
│       ├── movie_service.py        # Catalog & rating business logic
│       └── mining_service.py       # Data mining orchestrator & hybrid fusion
│
├── frontend/
│   ├── package.json                # React, Vite, Tailwind, Recharts, Lucide
│   ├── vite.config.js              # Vite config with Tailwind v4 & API reverse proxy
│   ├── index.html
│   └── src/
│       ├── App.jsx                 # Main application router
│       ├── main.jsx
│       ├── index.css               # Tailwind CSS v4 setup & dark theme
│       ├── context/
│       │   └── UserContext.jsx     # Active persona management across all pages
│       ├── components/
│       │   ├── Navbar.jsx          # Header with user persona switcher
│       │   ├── MovieCard.jsx       # Card with poster, rating, match %, rate action
│       │   ├── MetricCard.jsx      # Glowing KPI dashboard metric card
│       │   ├── AlgorithmFlowDiagram.jsx # INPUT -> PREPROCESSING -> ALGORITHM -> OUTPUT flow
│       │   └── RatingModal.jsx     # Interactive 1-5 star rating modal
│       ├── pages/
│       │   ├── Home.jsx            # Hero, quick KPIs, recommendations, top rated
│       │   ├── Movies.jsx          # Catalog with live search, genre filter, pagination
│       │   ├── MovieDetail.jsx     # Synopsis, ratings count, watch history, similar movies
│       │   ├── Recommendations.jsx # Hybrid, Collaborative, Content-Based, Cluster-Popular
│       │   ├── MyRatings.jsx       # Active user rating history & statistics
│       │   ├── UserProfile.jsx     # Demographics, cluster card, genre preference chart
│       │   ├── DataMiningDashboard.jsx # Faculty viva console with pipeline runner
│       │   ├── ClusterAnalysis.jsx # K-Means runner, K-selector, 2D PCA scatter plot
│       │   ├── AssociationRules.jsx # Apriori runner, Support/Confidence/Lift sliders
│       │   ├── ClassificationDemo.jsx # Predict User Preference with Random Forest
│       │   └── SystemInfo.jsx      # Architecture breakdown & 40+ Viva Q&A guide
│       └── services/
│           └── api.js              # Axios API service
│
├── data/
│   ├── kaggle_source_info.json     # Dataset provenance and citations
│   ├── movies.csv                  # 225 curated movies with TMDB posters
│   ├── users.csv                   # 120 user personas
│   ├── ratings.csv                 # 2,560 ratings
│   └── watch_history.csv           # 1,819 watch logs
│
├── docs/
│   ├── architecture.md             # System design & Mermaid diagrams
│   ├── algorithms.md               # Mathematical formulations for viva
│   └── viva_questions.md           # 40+ Comprehensive Viva Q&As
│
└── README.md
```

---

## 💾 Relational Database Tables

The database schema includes 10 normalized tables with primary keys, foreign keys, and indexes:
1. `users` (user_id, name, email, age, gender, created_at)
2. `movies` (movie_id, title, release_year, duration, description, language, imdb_rating, poster_url)
3. `genres` (genre_id, genre_name)
4. `movie_genres` (movie_id, genre_id)
5. `ratings` (rating_id, user_id, movie_id, rating, rating_date)
6. `watch_history` (history_id, user_id, movie_id, watched_at)
7. `recommendations` (recommendation_id, user_id, movie_id, recommendation_type, score, generated_at)
8. `clusters` (cluster_id, cluster_name, description)
9. `user_clusters` (user_id, cluster_id)
10. `association_rules` (rule_id, antecedent, consequent, support, confidence, lift)

---

## ⚡ Installation & Setup Guide

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### 2. Backend Setup
```bash
# Navigate to backend
cd MovieMine/backend

# Install Python dependencies
pip install -r requirements.txt

# Seed database and execute initial mining algorithms
python database/seed.py
```
> **Note on MySQL vs SQLite:**  
> By default, if MySQL is running on `localhost:3306`, MovieMine connects to MySQL. If MySQL is offline or not installed, MovieMine **automatically falls back to SQLite (`moviemine.db`) with zero downtime**.  
> To configure MySQL credentials explicitly, create a `.env` file in `backend/`:
> ```env
> DATABASE_URL=mysql+pymysql://root:password@localhost:3306/moviemine
> FORCE_SQLITE=false
> ```
> To migrate directly into MySQL, start your MySQL service (e.g., XAMPP or MySQL Workbench) and run:
> ```bash
> python database/mysql_setup.py
> ```

### 3. Run Backend Server
```bash
# From MovieMine/backend
python app.py
```
*Backend will be running on `http://127.0.0.1:5000`*

### 4. Frontend Setup & Run
Open a new terminal:
```bash
# Navigate to frontend
cd MovieMine/frontend

# Install dependencies (already prepared)
npm install

# Start Vite dev server
npm run dev
```
*Frontend will open on `http://localhost:5173`*

---

## 🎓 Faculty Demonstration Sequence (College Viva Walkthrough)

Follow this exact sequence during your viva demonstration to present the project:

### Step 1: System Overview & Data Provenance
1. Open the web interface at `http://localhost:5173`.
2. Navigate to **System Information / Viva Guide** tab.
3. Show faculty the **Kaggle Dataset Provenance** link (`The Movies Dataset` & `MovieLens`).
4. Walk through the 5-stage KDD Architecture diagram.

### Step 2: Show Database Persistence
1. Navigate to **Mining Dashboard**.
2. Point out the live database counts: **225 Movies, 120 Users, 2560 Ratings, 1819 Watch Records**.
3. Emphasize that all data resides in normalized relational tables with foreign keys and unique constraints.

### Step 3: Run the Live Data Mining Pipeline
1. In the **Mining Dashboard**, click **[Run Full Mining Pipeline]**.
2. Watch the pipeline tracker sequentially execute:
   - Step 1: Dataset Extraction
   - Step 2: Data Preprocessing & Rating Mean-Centering
   - Step 3: K-Means User Segmentation
   - Step 4: Apriori Association Rule Extraction
   - Step 5: Supervised Classification Model Training

### Step 4: Inspect K-Means Audience Clusters
1. Switch to the **K-Means Clusters** page.
2. Show the **2D PCA Scatter Plot**: explain how high-dimensional user vectors were projected onto 2D space.
3. Change the cluster slider to $K=3$ or $K=5$ and click **[RUN K-MEANS]**.
4. Show that cluster names (e.g., *"Action & Sci-Fi Enthusiasts"*, *"Drama Lovers"*) and dominant genres are computed dynamically from actual cluster centroids.

### Step 5: Demonstrate Apriori Association Rules
1. Switch to the **Association Rules** page.
2. Adjust **Min Support** (e.g. 8%) and **Min Confidence** (e.g. 40%).
3. Click **[GENERATE RULES]**.
4. Explain the difference between **Confidence** (conditional probability) and **Lift** (correlation over random independence). Sort the table by Lift.

### Step 6: Test Multi-Model Recommendations
1. Switch to the **Recommendations** page.
2. Toggle between the tabs:
   - **Hybrid Model:** Show the formula $0.5 \times \text{Collab} + 0.3 \times \text{Content} + 0.2 \times \text{Pop}$ with breakdown percentages.
   - **Collaborative Filtering:** Explain user-user Pearson correlation.
   - **Content-Based:** Explain TF-IDF and Cosine similarity.
   - **Cluster Popular:** Show what users in the active user's cluster prefer.

### Step 7: Persona Switching & Real-Time Adaptation
1. Click the **User Persona Switcher** dropdown in the top-right navbar.
2. Switch from an Action lover (e.g. *User #1*) to a Romance/Drama lover (e.g. *User #2*).
3. Show how the recommendations and the **Profile Genre Preference Chart** instantly re-adapt to the new persona!

### Step 8: Supervised Preference Prediction
1. Open the **Predict Preference** page.
2. Pick any user and candidate movie.
3. Click **[PREDICT PREFERENCE]** to demonstrate Random Forest classification predicting a binary LIKED / DISLIKED verdict with probability percentage.
