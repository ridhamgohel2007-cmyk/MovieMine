# MovieMine: Data Mining Mathematical Formulations & Algorithms

This document provides rigorous mathematical definitions, algorithmic pseudocode, and academic commentary for all Data Mining techniques implemented in **MovieMine**.

---

## 1. Collaborative Filtering (User-Based k-NN)

### Academic Concept
Collaborative Filtering makes recommendations based on user interaction histories. It builds an $M \times N$ matrix $R$ where rows represent users $U = \{u_1, u_2, \dots, u_M\}$ and columns represent movies $I = \{i_1, i_2, \dots, i_N\}$.

### Step 1: User Mean-Centering
To eliminate individual user rating biases (harsh raters vs generous raters):
$$\bar{r}_u = \frac{1}{|I_u|} \sum_{i \in I_u} r_{u, i}$$
Where $I_u$ is the set of movies rated by user $u$.

### Step 2: User Similarity Calculation (Adjusted Cosine / Pearson Correlation)
Let $I_{uv} = I_u \cap I_v$ denote the set of movies rated by both user $u$ and user $v$:
$$\text{sim}(u, v) = \frac{\sum_{i \in I_{uv}} (r_{u, i} - \bar{r}_u)(r_{v, i} - \bar{r}_v)}{\sqrt{\sum_{i \in I_{uv}} (r_{u, i} - \bar{r}_u)^2} \sqrt{\sum_{i \in I_{uv}} (r_{v, i} - \bar{r}_v)^2}}$$

### Step 3: Rating Prediction for Candidate Movie $i \notin I_u$
Select the top-$k$ nearest neighbors $N_k(u)$ with positive similarity ($\text{sim}(u, v) > 0$):
$$\hat{r}_{u, i} = \bar{r}_u + \frac{\sum_{v \in N_k(u)} \text{sim}(u, v) \cdot (r_{v, i} - \bar{r}_v)}{\sum_{v \in N_k(u)} |\text{sim}(u, v)|}$$

Candidate movies are ranked descending by predicted rating $\hat{r}_{u, i}$.

---

## 2. Content-Based Recommendation (TF-IDF & Cosine Similarity)

### Academic Concept
Content-Based Filtering operates on descriptive item metadata (genres, plot synopsis, language). Each movie is transformed into a high-dimensional document vector in Term Frequency-Inverse Document Frequency (TF-IDF) space.

### Step 1: Text Feature Representation
Each movie document $d$ is constructed as a metadata soup:
$$\text{Soup}(d) = (\text{Genres} \times 3) + \text{Plot Overview} + \text{Language}$$

### Step 2: TF-IDF Calculation
For term $t$ in movie document $d$ across catalog corpus $D$:
$$\text{TF}(t, d) = \frac{f_{t, d}}{\sum_{t' \in d} f_{t', d}}$$
$$\text{IDF}(t, D) = \log\left(\frac{|D|}{1 + |\{d \in D : t \in d\}|}\right)$$
$$\mathbf{v}_d(t) = \text{TF}(t, d) \times \text{IDF}(t, D)$$

### Step 3: Pairwise Cosine Similarity
$$\text{CosineSim}(\mathbf{v}_A, \mathbf{v}_B) = \frac{\mathbf{v}_A \cdot \mathbf{v}_B}{\|\mathbf{v}_A\| \|\mathbf{v}_B\|} = \frac{\sum_{k=1}^V v_{A, k} v_{B, k}}{\sqrt{\sum_{k=1}^V v_{A, k}^2} \sqrt{\sum_{k=1}^V v_{B, k}^2}}$$
Scores range in $[0.0, 1.0]$. The top-$N$ highest scoring movies are recommended.

---

## 3. K-Means User Preference Clustering

### Academic Concept
K-Means is an unsupervised clustering algorithm that groups $N$ users into $K$ disjoint clusters $S = \{S_1, S_2, \dots, S_K\}$ by minimizing the Within-Cluster Sum of Squares (WCSS / Inertia).

### Step 1: User Feature Vector Construction
For each user $u$, extract:
$$\mathbf{x}_u = \left[ \bar{r}_u, \text{Count}_u, \text{WatchCnt}_u, w_{u, \text{Action}}, w_{u, \text{SciFi}}, \dots, w_{u, \text{Romance}} \right]^T$$
Where genre weight $w_{u, g}$ is the L1-normalized rating proportion allocated to genre $g$.

### Step 2: Feature Standardization
$$\tilde{x}_{u, j} = \frac{x_{u, j} - \mu_j}{\sigma_j}$$

### Step 3: Objective Function Optimization
$$J = \sum_{j=1}^K \sum_{\mathbf{x} \in S_j} \|\mathbf{x} - \boldsymbol{\mu}_j\|^2$$
Iteratively alternating between:
1. **Assignment:** $S_j^{(t)} = \left\{ \mathbf{x} : \|\mathbf{x} - \boldsymbol{\mu}_j^{(t)}\|^2 \le \|\mathbf{x} - \boldsymbol{\mu}_{j'}^{(t)}\|^2, \forall j' \right\}$
2. **Update:** $\boldsymbol{\mu}_j^{(t+1)} = \frac{1}{|S_j^{(t)}|} \sum_{\mathbf{x} \in S_j^{(t)}} \mathbf{x}$

### Step 4: 2D Principal Component Analysis (PCA) Projection
To visualize the 20-dimensional cluster centroids and user vectors in Recharts:
$$\mathbf{X}_{\text{2D}} = \mathbf{X}_{\text{scaled}} \cdot \mathbf{W}_2$$
Where $\mathbf{W}_2 \in \mathbb{R}^{d \times 2}$ represents the eigenvectors corresponding to the two largest eigenvalues of the covariance matrix $\mathbf{\Sigma} = \frac{1}{n} \mathbf{X}^T \mathbf{X}$.

---

## 4. Association Rule Mining (Apriori Algorithm)

### Academic Concept
Given a transaction database $T = \{t_1, t_2, \dots, t_M\}$ where each transaction $t_k$ represents the set of movies watched or rated $\ge 3.5$ by user $k$, derive rules:
$$A \implies B \quad (A \cap B = \emptyset)$$

### Mathematical Metrics

#### 1. Support
$$\text{Support}(A \implies B) = P(A \cup B) = \frac{|\{t \in T : (A \cup B) \subseteq t\}|}{|T|}$$

#### 2. Confidence
$$\text{Confidence}(A \implies B) = P(B \mid A) = \frac{\text{Support}(A \cup B)}{\text{Support}(A)}$$

#### 3. Lift
$$\text{Lift}(A \implies B) = \frac{\text{Confidence}(A \implies B)}{\text{Support}(B)} = \frac{P(A \cap B)}{P(A) \cdot P(B)}$$
- **$\text{Lift} > 1$:** Positive correlation ($A$ and $B$ co-occur more than random chance).
- **$\text{Lift} = 1$:** Independent occurrences.
- **$\text{Lift} < 1$:** Negative correlation / substitute items.

### Apriori Anti-Monotonicity Principle
$$\forall X, Y : X \subseteq Y \implies \text{Support}(Y) \le \text{Support}(X)$$
If itemset $X$ fails to meet the minimum support threshold, no superset $Y$ can be frequent, pruning exponential search space.

---

## 5. Hybrid Recommendation Formulation

MovieMine creates a balanced composite recommendation score:
$$\text{Hybrid Score}(u, i) = \alpha \cdot \hat{r}_{\text{collab}}(u, i) + \beta \cdot \text{Sim}_{\text{content}}(u, i) + \gamma \cdot \text{Pop}(i)$$

### Parameter Weights
- $\alpha = 0.50$ (Collaborative Filtering Weight)
- $\beta = 0.30$ (Content-Based Similarity Weight)
- $\gamma = 0.20$ (Global Popularity Weight)
- Constraint: $\alpha + \beta + \gamma = 1.0$

All individual component scores are normalized to $[0.0, 1.0]$ prior to linear combination.
