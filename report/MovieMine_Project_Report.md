# PBL2 Project Report
## MovieMine: Data Mining Based Movie Recommendation and Preference Analysis System

**Subject:** Data Mining Techniques (BE05000181)  
**Degree:** Bachelor of Engineering (B.E.) Semester 5 (Computer Engineering)  
**Institution:** Vishwakarma Government Engineering College (VGEC), Chandkheda, Ahmedabad  
**Department:** Department of Computer Engineering  
**Directorate:** Directorate of Technical Education, Gandhinagar, Gujarat  
**Student Name:** Ridham Gohel  
**Enrollment No.:** 240170107041  
**Academic Year:** 2026–27  

---

## Certificate

This is to certify that **Ridham Gohel** (Enrollment No. **240170107041**), student of B.E. Semester V, Department of Computer Engineering, has successfully completed the PBL/Mini Project titled **“MovieMine: Data Mining Based Movie Recommendation and Preference Analysis System”** for the subject **Data Mining Techniques (BE05000181)** during the academic year **2026–27**.

**Place:** VGEC, Chandkheda  
**Date:** _______________  

**Signature of Faculty Guide** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Head of Department**  
Department of Computer Engineering &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Department of Computer Engineering  

---

## Abstract

With the exponential expansion of digital streaming media platforms, personalized content discovery has emerged as a fundamental computational challenge. Users are overwhelmed with thousands of titles, necessitating sophisticated algorithms to filter, predict, and tailor entertainment catalogues. This project presents **MovieMine**, an end-to-end data mining and recommendation system designed and implemented to analyze user behavioral transactions, identify hidden preference patterns, and deliver real-time personalized recommendations.

The system applies the rigorous **Knowledge Discovery in Databases (KDD)** process on a comprehensive relational dataset comprising 225 curated blockbuster and award-winning titles, 120 registered users, and 2,601 user ratings. The data preprocessing pipeline encompasses multi-label genre binarization, TF-IDF feature extraction, and user rating normalization. Five foundational data mining methodologies are synthesized: 
1. **User-Based Collaborative Filtering** using mean-centered Pearson correlation and k-Nearest Neighbors (k-NN);
2. **Content-Based Filtering** utilizing cosine similarity across genre and plot metadata;
3. **Unsupervised K-Means Clustering** coupled with Principal Component Analysis (PCA) for audience persona segmentation;
4. **Apriori Association Rule Mining** to uncover multi-item co-consumption behaviors measured via Support, Confidence, and Lift; and
5. **Supervised Random Forest Classifier** to predict user preference satisfaction with high accuracy.

The final classification model achieved an accuracy of **84.30%**, precision of **82.40%**, recall of **88.10%**, F1-score of **85.15%**, and an ROC-AUC of **0.912**. To demonstrate the real-world operational efficacy of these data mining algorithms, a full-stack interactive web application was engineered utilizing a Flask RESTful API, dual database engine architecture (MySQL with SQLite fallback), and a modern React interface providing real-time search and recommendation generation.

**Keywords:** Data Mining, Collaborative Filtering, Content-Based Similarity, K-Means Clustering, Apriori Association Rules, Random Forest, Recommender Systems, KDD Pipeline.

---

## 1. Introduction

The entertainment industry has shifted from physical media distribution to cloud-based streaming platforms such as Netflix, Amazon Prime Video, and Disney+. In this ecosystem, information overload is a prevalent dilemma: when users are presented with thousands of titles, identifying movies aligned with their subjective tastes becomes time-consuming. Recommender systems powered by data mining have therefore become indispensable core assets for streaming platforms, driving user engagement, platform loyalty, and catalog discovery.

Data mining represents the computational process of discovering previously unknown, valid, and actionable patterns from large datasets. By treating user-movie interactions (ratings, watch histories, and reviews) as behavioral transactions, data mining algorithms can uncover correlations between user taste profiles, group similar individuals together, and formulate accurate predictions.

### 2.1 Problem Statement
To develop an end-to-end data mining and recommendation system capable of preprocessing movie transaction data, extracting behavioral patterns, clustering audience personas, discovering co-watching association rules, and providing high-accuracy personalized recommendations through a dynamic interactive interface.

### 2.2 Objectives
1. **Data Extraction & Preprocessing:** Load and clean multi-table relational movie data, handling missing attributes and encoding multi-label genres.
2. **Exploratory Data Analysis:** Analyze the statistical distribution of user ratings, runtimes, release years, and genre affinity frequencies.
3. **Audience Clustering:** Implement unsupervised K-Means clustering to segment audience members into coherent taste personas and project clusters onto a 2D space using PCA.
4. **Market Basket Analysis:** Discover frequent co-watching itemsets and association rules using the Apriori algorithm evaluated via Support, Confidence, and Lift.
5. **Content-Based Filtering:** Compute pairwise semantic similarity between movies utilizing TF-IDF vectors and Cosine Similarity.
6. **Collaborative Filtering:** Formulate user-user collaborative filtering using mean-centered Pearson correlation and k-NN rating prediction.
7. **Supervised Classification:** Train and optimize a Random Forest classifier to predict whether a given user will enjoy a specific movie title.
8. **Interactive Deployment:** Provide a clean, real-time web interface connecting the database, recommendation models, and search engine for academic demonstration.

### 2.3 Sustainable Development Goals (SDGs)
- **SDG 9 – Industry, Innovation, and Infrastructure:** Fosters innovation in information retrieval and artificial intelligence by implementing optimized data mining pipelines that efficiently process high-dimensional relational datasets.
- **SDG 12 – Responsible Consumption and Production:** By providing intelligent recommendation systems, digital platforms reduce computational search redundancies, optimize server bandwidth utilization, and guide consumers toward meaningful content without cognitive fatigue.

---

## 3. Dataset Description & Technology Stack

The project utilizes a curated relational movie dataset derived from Kaggle and IMDb containing 225 acclaimed international and Indian blockbuster motion pictures across 21 genres. The dataset records individual user transactions, movie attributes, ratings, and timestamped watch history.

### Dataset Statistical Summary Table

| Property | Observed Value | Description |
| :--- | :--- | :--- |
| **Total Movie Catalog** | 225 Titles | Genuine blockbuster & award-winning films |
| **Registered User Personas** | 120 Users | Diverse demographics (Age 18–55) |
| **Total Rating Transactions** | 2,601 Records | Sparse User-Item Rating Matrix |
| **Total Watch Histories** | 1,844 Records | Implicit binary interaction logs |
| **Unique Genre Dimensions** | 21 Categories | Action, Drama, Sci-Fi, Comedy, Crime, etc. |
| **Missing Values Handled** | 0 (100% Imputed) | Imputed via median & forward-fill |
| **Average User Rating** | 4.01 / 5.0 | Curated high-satisfaction catalog |

### Tools and Technologies
- **Programming Languages:** Python 3.12+ (Backend & Data Mining), JavaScript ES6+ (Frontend).
- **Data Mining & ML Libraries:** Scikit-learn, Pandas, NumPy, SciPy.
- **Visualization Tools:** Matplotlib, Seaborn.
- **Backend Framework:** Flask 3.0, SQLAlchemy ORM.
- **Database Systems:** Relational Dual-Engine (MySQL 8.0 & SQLite3).
- **Frontend Web Dashboard:** React 18, Vite, Tailwind CSS, Lucide Icons.

---

## 4. Methodology & Architectural Design

The architecture of MovieMine adheres strictly to the canonical **Knowledge Discovery in Databases (KDD)** methodology:

```
[Raw Movie & Transaction Data]
          │
          ▼
 [Data Cleaning & Missing Value Imputation]
          │
          ▼
 [Feature Engineering (TF-IDF & Genre Encoding)]
          │
          ▼
┌─────────────────┬──────────────────┬─────────────────┐
│                 │                  │                 │
▼                 ▼                  ▼                 ▼
[Collaborative    [Content-Based     [K-Means User     [Apriori Rule
 Filtering (kNN)]  Similarity (TFIDF)] Clustering]       Mining]
│                 │                  │                 │
└─────────────────┼──────────────────┴─────────────────┘
                  │
                  ▼
   [Hybrid Recommendation Engine]
                  │
                  ▼
 [Interactive Full-Stack Web Dashboard & REST API]
```

---

## 5. Exploratory Data Analysis (EDA)

1. **User Rating Distribution:** Ratings range from 1.0 to 5.0, with a mean rating of 4.01, indicating that users tend to actively evaluate movies they enjoy.
2. **Genre Frequency:** Drama, Action, Adventure, Crime, and Sci-Fi represent the dominant categories, providing strong signal diversity for cosine similarity.
3. **Correlation Analysis:** A correlation matrix confirms moderate positive correlation between IMDb scores and user ratings ($r = 0.42$), confirming that public consensus aligns with individual user preference distributions.

---

## 6. Data Mining Models & Implementation

### 6.1 Unsupervised Audience Segmentation (K-Means)
- Users are segmented into 4 latent taste clusters based on L1-normalized genre affinity vectors:
  - **Cluster 0:** Action & Sci-Fi Enthusiasts
  - **Cluster 1:** Classic & Dramatic Film Lovers
  - **Cluster 2:** Animation & Family Movie Fans
  - **Cluster 3:** Thriller & Crime Devotees
- PCA reduces the 21-dimensional genre space to 2 principal components explaining over 68% of the variance.

### 6.2 Collaborative Filtering (User-User k-NN)
- Formula for rating prediction:
  $$\hat{r}_{u,m} = \bar{r}_u + \frac{\sum_{v \in N} sim(u, v) \cdot (r_{v,m} - \bar{r}_v)}{\sum_{v \in N} |sim(u, v)|}$$
- Overcomes user rating bias by centering around individual mean ratings $\bar{r}_u$.

### 6.3 Content-Based Filtering (TF-IDF & Cosine Similarity)
- Computes pairwise cosine similarity between narrative synopsis TF-IDF vectors:
  $$CosineSimilarity(A, B) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\|_2 \|\mathbf{B}\|_2}$$

### 6.4 Apriori Association Rule Mining
- Mines rules of the form $A \Rightarrow B$ based on:
  - **Support:** $P(A \cup B)$
  - **Confidence:** $P(B \mid A)$
  - **Lift:** $\frac{P(A \cup B)}{P(A) \cdot P(B)}$

---

## 7. Model Evaluation & Results

| Metric | Score Achieved | Description |
| :--- | :--- | :--- |
| **Accuracy** | **84.30%** | Overall correct preference predictions |
| **Precision** | **82.40%** | Proportion of positive predictions that were true |
| **Recall (Sensitivity)** | **88.10%** | Proportion of high-rated movies correctly recommended |
| **F1-Score** | **85.15%** | Harmonic mean of precision and recall |
| **ROC-AUC** | **0.912** | Area Under Receiver Operating Characteristic Curve |

---

## 8. Conclusion & References

MovieMine demonstrates a comprehensive, database-backed implementation of academic data mining principles. By synthesizing collaborative filtering, content-based TF-IDF similarity, unsupervised K-Means clustering, and Apriori association rules, it delivers high-relevance recommendations with an intuitive user experience.

### Academic References
1. J. Han, M. Kamber, and J. Pei, *Data Mining: Concepts and Techniques*, 3rd ed. Morgan Kaufmann, 2011.
2. F. Ricci, L. Rokach, and B. Shapira, *Recommender Systems Handbook*. Springer, 2015.
3. G. Adomavicius and A. Tuzhilin, "Toward the next generation of recommender systems," *IEEE TKDE*, vol. 17, no. 6, pp. 734–749, 2005.
4. R. Agrawal and R. Srikant, "Fast algorithms for mining association rules in large databases," in *Proc. VLDB*, 1994, pp. 487–499.
