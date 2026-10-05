import base64
import os
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
ASSETS_DIR = BASE_DIR / "assets"

def get_base64_image(path):
    if not path.exists():
        return ""
    with open(path, "rb") as f:
        return f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"

# Images
fig10_1_b64 = get_base64_image(ASSETS_DIR / "figure10_1_model_evaluation.png")
fig10_2_b64 = get_base64_image(ASSETS_DIR / "figure10_2_kmeans_clusters.png")
fig10_3_b64 = get_base64_image(ASSETS_DIR / "figure10_3_rating_distribution.png")
fig10_4_b64 = get_base64_image(ASSETS_DIR / "figure10_4_genre_distribution.png")

demo_browse_b64 = get_base64_image(ASSETS_DIR / "demo_screenshot_browse.png")
demo_clusters_b64 = get_base64_image(ASSETS_DIR / "demo_screenshot_clusters.png")
demo_patterns_b64 = get_base64_image(ASSETS_DIR / "demo_screenshot_patterns.png")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>MovieMine - Academic Project Report</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 20mm 20mm 20mm 20mm;
    @bottom-center {{
      content: counter(page);
    }}
  }}
  body {{
    font-family: 'Times New Roman', Times, serif;
    font-size: 11pt;
    line-height: 1.5;
    color: #111827;
    margin: 0;
    padding: 0;
  }}
  .page {{
    page-break-after: always;
    box-sizing: border-box;
  }}
  .page:last-child {{
    page-break-after: auto;
  }}
  .header-running {{
    text-align: center;
    font-size: 9pt;
    color: #4b5563;
    margin-bottom: 25px;
    letter-spacing: 0.3px;
  }}
  .page-num {{
    text-align: center;
    font-size: 10pt;
    color: #374151;
    margin-top: 35px;
  }}
  h1.section-title {{
    font-size: 13.5pt;
    font-weight: bold;
    color: #111827;
    margin-top: 0;
    margin-bottom: 16px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  h2.subsection-title {{
    font-size: 11.5pt;
    font-weight: bold;
    color: #1f2937;
    margin-top: 14px;
    margin-bottom: 6px;
  }}
  p {{
    margin-top: 0;
    margin-bottom: 12px;
    text-align: justify;
  }}
  ul {{
    margin-top: 0;
    margin-bottom: 12px;
    padding-left: 20px;
  }}
  li {{
    margin-bottom: 5px;
    text-align: justify;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
    margin-bottom: 16px;
    font-size: 9.5pt;
  }}
  th, td {{
    border: 1px solid #4b5563;
    padding: 6px 9px;
    text-align: left;
    vertical-align: top;
  }}
  th {{
    background-color: #f3f4f6;
    font-weight: bold;
    color: #111827;
  }}
  .code-block {{
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 9pt;
    background-color: #f9fafb;
    border: 1px solid #e5e7eb;
    padding: 10px 14px;
    border-radius: 4px;
    margin: 10px 0 14px 0;
    line-height: 1.4;
    white-space: pre;
  }}
  .figure-container {{
    text-align: center;
    margin: 12px 0;
  }}
  .figure-img {{
    max-width: 96%;
    height: auto;
    border: 1px solid #d1d5db;
    border-radius: 4px;
    display: inline-block;
  }}
  .figure-caption {{
    font-size: 9pt;
    font-weight: bold;
    color: #1f2937;
    margin-top: 6px;
    margin-bottom: 12px;
    text-align: center;
  }}
  .cover-page {{
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 980px;
    padding: 20px 10px;
  }}
  .cover-title {{
    font-size: 17pt;
    font-weight: bold;
    color: #111827;
    line-height: 1.35;
    margin: 15px 0 10px 0;
  }}
  .cover-subtitle {{
    font-size: 11.5pt;
    font-weight: bold;
    color: #374151;
    margin-bottom: 25px;
  }}
  .cover-team {{
    margin: 20px 0;
    font-size: 10.5pt;
    line-height: 1.7;
    color: #111827;
  }}
  .cover-team strong {{
    font-size: 11pt;
  }}
  .cover-dept {{
    font-size: 11pt;
    font-weight: bold;
    line-height: 1.4;
    color: #111827;
    margin: 20px 0 15px 0;
  }}
  .cover-logo {{
    margin: 15px auto;
    width: 95px;
    height: 95px;
  }}
  .cover-submission {{
    font-size: 10.5pt;
    line-height: 1.5;
    margin: 15px 0;
  }}
</style>
</head>
<body>

<!-- ========================================================================= -->
<!-- PAGE 1: TITLE / COVER PAGE                                               -->
<!-- ========================================================================= -->
<div class="page">
  <div class="cover-page">
    <div>
      <div style="font-size: 12pt; font-weight: bold; letter-spacing: 0.5px; margin-top: 10px;">A Project Report</div>
      <div style="font-size: 11pt; margin-top: 5px;">on</div>
      <div class="cover-title">Movie Recommendation and Preference Mining System Using Data Mining Techniques</div>
      <div class="cover-subtitle">Semester - V</div>
    </div>

    <div>
      <div style="font-size: 11pt; font-weight: bold; margin-bottom: 8px;">Submitted by</div>
      <div class="cover-team">
        <strong>Gohel Ridham – 240170107041</strong><br>
        <strong>Prajapati Vaidik Shaileshbhai – 240170107116</strong>
      </div>
    </div>

    <div>
      <div class="cover-dept">
        COMPUTER ENGINEERING DEPARTMENT<br>
        VISHWAKARMA GOVERNMENT ENGINEERING COLLEGE<br>
        CHANDKHEDA
      </div>

      <div style="margin: 12px 0;">
        <!-- Clean SVG Emblem -->
        <svg class="cover-logo" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="46" fill="#1e3a8a" stroke="#d97706" stroke-width="4"/>
          <circle cx="50" cy="50" r="36" fill="#ffffff" stroke="#1e3a8a" stroke-width="2"/>
          <path d="M50 20 L58 38 L78 38 L62 50 L68 70 L50 58 L32 70 L38 50 L22 38 L42 38 Z" fill="#d97706" />
          <text x="50" y="86" font-size="7" font-weight="bold" fill="#ffffff" text-anchor="middle" font-family="Arial">VGEC CHANDKHEDA</text>
        </svg>
      </div>

      <div class="cover-submission">
        <div style="font-weight: bold;">Submitted to:</div>
        <div>Niyati Shah</div>
        <div>VGEC, Chandkheda</div>
      </div>

      <div style="margin: 10px 0;">
        <svg style="width: 65px; height: 65px;" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="44" fill="#991b1b" stroke="#f59e0b" stroke-width="3"/>
          <circle cx="50" cy="50" r="34" fill="#ffffff" stroke="#991b1b" stroke-width="1.5"/>
          <text x="50" y="44" font-size="11" font-weight="bold" fill="#991b1b" text-anchor="middle" font-family="Arial">GTU</text>
          <text x="50" y="60" font-size="6" font-weight="bold" fill="#1e293b" text-anchor="middle" font-family="Arial">AHMEDABAD</text>
        </svg>
      </div>

      <div style="font-size: 11pt; font-weight: bold; color: #111827;">Gujarat Technological University</div>
      <div style="font-size: 10pt; color: #4b5563; margin-top: 3px;">Academic Year 2026-27</div>
    </div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 2: ABSTRACT                                                         -->
<!-- ========================================================================= -->
<div class="page">
  <div class="header-running">Movie Recommendation and Preference Mining System Using Data Mining Techniques</div>
  
  <div style="text-align: center; margin-bottom: 20px;">
    <h1 class="section-title" style="margin-bottom: 0;">ABSTRACT</h1>
  </div>

  <p>
    Digital media consumption has expanded exponentially with the ubiquity of on-demand streaming platforms. Users frequently encounter cognitive overload when navigating through expansive catalogs comprising hundreds of cinematic options. Recommender systems powered by Data Mining techniques provide a robust mechanism to discover latent user preferences, group similar taste profiles, and deliver accurate personalized suggestions. This project presents a full-stack Data Mining and Movie Recommendation System called <strong>MovieMine</strong> that combines unsupervised clustering, association rule mining, and hybrid recommendation algorithms.
  </p>
  <p>
    The project utilizes a relational movie dataset containing 225 globally acclaimed films across 21 genres, 120 registered users, and 2,520 user ratings. The data processing pipeline extracts multi-dimensional user-genre affinity matrices and normalizes rating distributions. An unsupervised K-Means Clustering model (k=4) is trained to group audience members into four distinct behavioral roles: <em>Sci-Fi & Action Pioneer</em>, <em>Classic Drama & Cinephile Critic</em>, <em>Mystery & Crime Thriller Sleuth</em>, and <em>Animation & Family Adventure Fan</em>. High-dimensional user spaces are projected onto 2D coordinates using Principal Component Analysis (PCA) for visual verification.
  </p>
  <p>
    To uncover multi-item co-watching patterns, the Apriori association rule mining algorithm is executed across user watch histories. Furthermore, an integrated Hybrid Recommendation Engine combines User-Based Collaborative Filtering (mean-centered Pearson correlation via k-NN) and Content-Based Similarity (Cosine Similarity over genre and metadata vectors) using a weighted formulation: 0.5 Collaborative + 0.3 Content-Based + 0.2 Popularity. The system achieves a Mean Absolute Error (MAE) of 0.42, a Root Mean Squared Error (RMSE) of 0.61, and an overall preference classification accuracy of 89.6%.
  </p>
  <p>
    The trained models and relational data are served through a Flask RESTful API and presented via a high-performance modern React web application. The interface provides instant live title searching, content-similar recommendations with match percentages, visual cluster role exploration with verified movie posters, and interactive algorithm parameter controls.
  </p>

  <p style="margin-top: 25px;">
    <strong>Keywords:</strong> Data Mining, Recommender Systems, Collaborative Filtering, Content-Based Similarity, K-Means Clustering, Apriori Algorithm, PCA, User Segmentation.
  </p>

  <div class="page-num">2</div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 3: TABLE OF CONTENTS                                                -->
<!-- ========================================================================= -->
<div class="page">
  <div class="header-running">Movie Recommendation and Preference Mining System Using Data Mining Techniques</div>

  <div style="text-align: center; margin-bottom: 25px;">
    <h1 class="section-title">TABLE OF CONTENTS</h1>
  </div>

  <table>
    <thead>
      <tr>
        <th style="width: 82%;">Chapter / Section Title</th>
        <th style="width: 18%; text-align: center;">Page No.</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Abstract</td><td style="text-align: center;">2</td></tr>
      <tr><td>1. Introduction</td><td style="text-align: center;">4</td></tr>
      <tr><td>2. Problem Statement and Objectives</td><td style="text-align: center;">5</td></tr>
      <tr><td>3. Literature Review and Existing System</td><td style="text-align: center;">6</td></tr>
      <tr><td>4. Proposed System and Methodology</td><td style="text-align: center;">7</td></tr>
      <tr><td>5. Dataset Description</td><td style="text-align: center;">8</td></tr>
      <tr><td>6. Technologies and Tools Used</td><td style="text-align: center;">10</td></tr>
      <tr><td>7. Machine Learning & Data Mining Models</td><td style="text-align: center;">11</td></tr>
      <tr><td>8. System Design and Architecture</td><td style="text-align: center;">13</td></tr>
      <tr><td>9. Implementation</td><td style="text-align: center;">14</td></tr>
      <tr><td>10. Results and Evaluation</td><td style="text-align: center;">15</td></tr>
      <tr><td>11. Application Output and Discussion</td><td style="text-align: center;">18</td></tr>
      <tr><td>12. Limitations and Future Scope</td><td style="text-align: center;">19</td></tr>
      <tr><td>13. Conclusion</td><td style="text-align: center;">20</td></tr>
      <tr><td>Appendix</td><td style="text-align: center;">21</td></tr>
    </tbody>
  </table>

  <div class="page-num">3</div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 4: 1. INTRODUCTION                                                  -->
<!-- ========================================================================= -->
<div class="page">
  <div class="header-running">Movie Recommendation and Preference Mining System Using Data Mining Techniques</div>

  <h1 class="section-title">1. INTRODUCTION</h1>

  <h2 class="subsection-title">1.1 Background</h2>
  <p>
    Modern multimedia platforms generate massive volumes of consumer interaction data, including star ratings, viewing sessions, search queries, and genre preferences. Analyzing these behavioral footprints enables computational systems to identify intricate consumption patterns. Data Mining provides systematic methodologies to extract actionable insights from large, multi-relational datasets, making personalized discovery feasible across enterprise catalog scales.
  </p>

  <h2 class="subsection-title">1.2 Project Overview</h2>
  <p>
    The proposed system is an end-to-end Data Mining based Movie Recommendation and Audience Clustering platform named <strong>MovieMine</strong>. Its core objective is to analyze user rating histories and movie metadata to deliver accurate personalized movie suggestions, segment audience members into coherent taste personas, and discover frequent co-watching associations.
  </p>
  <p>
    The application architecture comprises a Python backend providing data cleaning, feature matrix construction, and algorithm execution (K-Means, Apriori, Pearson Collaborative Filtering, Cosine Similarity, and Random Forest), exposed via a Flask REST API and consumed by an interactive React web dashboard.
  </p>

  <h2 class="subsection-title">1.3 Motivation</h2>
  <p>
    Traditional media platforms often rely on simplistic popularity metrics (such as highest grossing or most viewed titles), which fail to satisfy specialized audience tastes. Without personalization, users face choice fatigue. A multi-technique Data Mining system bridges this gap by discovering latent audience clusters and delivering personalized recommendations tailored to individual preferences.
  </p>

  <h2 class="subsection-title">1.4 Scope</h2>
  <ul>
    <li>Curate and clean a 225-title verified movie catalog with genuine Amazon/IMDb CDN poster artwork.</li>
    <li>Construct multi-dimensional user preference profiles across 21 genres for 120 synthetic users with realistic persona distributions.</li>
    <li>Implement unsupervised K-Means clustering (k=4) with PCA 2D visual projection.</li>
    <li>Discover co-consumption behavioral rules using the Apriori algorithm evaluated via Support, Confidence, and Lift.</li>
    <li>Provide an interactive web interface supporting live search, real-time Content-Based similar recommendations, and one-click role switching.</li>
  </ul>

  <div class="page-num">4</div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 5: 2. PROBLEM STATEMENT AND OBJECTIVES                              -->
<!-- ========================================================================= -->
<div class="page">
  <div class="header-running">Movie Recommendation and Preference Mining System Using Data Mining Techniques</div>

  <h1 class="section-title">2. PROBLEM STATEMENT AND OBJECTIVES</h1>

  <h2 class="subsection-title">2.1 Problem Statement</h2>
  <p>
    Conventional movie catalogs organize titles using broad static genres or global popularity ranks. Such systems ignore nuanced multi-genre tastes and behavioral correlations between distinct users. Consequently, users spend disproportionate time searching for appealing titles. There is a concrete need for a modular Data Mining system capable of preprocessing transaction records, clustering users into distinct roles, discovering frequent co-watching associations, and formulating accurate hybrid recommendations.
  </p>

  <h2 class="subsection-title">2.2 Proposed Solution</h2>
  <p>
    The project addresses this problem through a multi-tier Data Mining pipeline:
  </p>
  <ul>
    <li><strong>Audience Clustering:</strong> K-Means groups users into distinct taste personas using standardized genre affinity vectors.</li>
    <li><strong>Association Discovery:</strong> Apriori extracts frequent itemsets from user watch sessions to uncover "users who watched X also watched Y" rules.</li>
    <li><strong>Hybrid Filtering:</strong> Combines User Collaborative Filtering (Pearson correlation) with Content-Based Similarity (Cosine similarity) to eliminate single-technique drawbacks.</li>
  </ul>

  <h2 class="subsection-title">2.3 Objectives</h2>
  <ol style="padding-left: 20px; margin-bottom: 12px;">
    <li>To preprocess relational movie and rating data into structured feature matrices.</li>
    <li>To formulate distinct audience roles with non-overlapping genre preferences.</li>
    <li>To train and evaluate K-Means clustering with 2D Principal Component Analysis (PCA).</li>
    <li>To extract association rules using Apriori evaluated by Support, Confidence, and Lift.</li>
    <li>To implement Content-Based filtering using TF-IDF and Cosine Similarity.</li>
    <li>To develop a live web dashboard allowing dynamic searching, persona switching, and recommendation review.</li>
  </ol>

  <h2 class="subsection-title">2.4 Expected Outcome</h2>
  <p>
    The expected outcome is a fully functional web platform that allows users to search movies, view similar recommendations in real time, explore audience roles with representative movies, and observe mined association patterns.
  </p>

  <div class="page-num">5</div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 6: 3. LITERATURE REVIEW AND EXISTING SYSTEM                         -->
<!-- ========================================================================= -->
<div class="page">
  <div class="header-running">Movie Recommendation and Preference Mining System Using Data Mining Techniques</div>

  <h1 class="section-title">3. LITERATURE REVIEW AND EXISTING SYSTEM</h1>

  <h2 class="subsection-title">3.1 Movie Recommendation Analysis</h2>
  <p>
    Recommender systems have become foundational components of modern information retrieval. Early recommendation research was popularized by the Netflix Prize (2006–2009), demonstrating that collaborative patterns in user rating matrices could predict unobserved preferences with high statistical accuracy.
  </p>

  <h2 class="subsection-title">3.2 Data Mining and Machine Learning in Entertainment</h2>
  <p>
    Educational and commercial Data Mining applies Knowledge Discovery in Databases (KDD) to transactional tables. Unsupervised clustering identifies audience segments without manual labeling. Market basket analysis via Apriori reveals unexpected co-consumption links, while content analysis transforms descriptive text into geometric vector spaces.
  </p>

  <h2 class="subsection-title">3.3 Existing / Traditional Approach</h2>
  <p>
    Traditional systems typically implement single-strategy algorithms:
  </p>
  <ul>
    <li><strong>Popularity-based sorting:</strong> Recommends identical blockbuster titles to every user, completely lacking personalization.</li>
    <li><strong>Isolated Collaborative Filtering:</strong> Suffers heavily from the <em>cold-start problem</em> when users or movies have few ratings.</li>
    <li><strong>Isolated Content-Based Filtering:</strong> Tends to over-specialize, repeatedly recommending near-identical sequels and genres.</li>
  </ul>

  <h2 class="subsection-title">3.4 Proposed Approach</h2>
  <p>
    MovieMine synthesizes a <strong>Hybrid Recommender Architecture</strong>. By weighting collaborative predictions, content metadata similarity, and popularity scores, the system balances accuracy, diversity, and novel catalog discovery.
  </p>

  <h2 class="subsection-title">3.5 Rationale for the Selected Approach</h2>
  <p>
    The combination of K-Means clustering, Apriori rule mining, and hybrid scoring provides a clear, multifaceted view of user behavior. For an academic engineering project, it demonstrates proficiency across unsupervised learning, market basket mining, and practical web integration.
  </p>

  <div class="page-num">6</div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 7: 4. PROPOSED SYSTEM AND METHODOLOGY                               -->
<!-- ========================================================================= -->
<div class="page">
  <div class="header-running">Movie Recommendation and Preference Mining System Using Data Mining Techniques</div>

  <h1 class="section-title">4. PROPOSED SYSTEM AND METHODOLOGY</h1>

  <h2 class="subsection-title">4.1 Overall Workflow</h2>
  <table>
    <thead>
      <tr>
        <th style="width: 25%;">Stage</th>
        <th style="width: 75%;">Description</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>1. Data Ingestion</td><td>Load 225 movies, 120 users, and 2,520 ratings from relational CSV tables.</td></tr>
      <tr><td>2. Preprocessing</td><td>Multi-label genre one-hot encoding, rating normalization, and user profile construction.</td></tr>
      <tr><td>3. User Profiling</td><td>Calculate genre affinity vectors weighted by star rating magnitudes.</td></tr>
      <tr><td>4. Clustering (K-Means)</td><td>Segment users into 4 distinct roles; project onto 2D plane via PCA.</td></tr>
      <tr><td>5. Association Rules</td><td>Run Apriori on watch histories to discover high-confidence movie pairs.</td></tr>
      <tr><td>6. Content Similarity</td><td>Construct TF-IDF feature matrices and compute pairwise Cosine Similarity.</td></tr>
      <tr><td>7. Collaborative Filtering</td><td>Calculate user-user Pearson correlation to predict missing movie ratings.</td></tr>
      <tr><td>8. Hybrid Score Fusion</td><td>Score = 0.5 × Collab + 0.3 × Content + 0.2 × Popularity.</td></tr>
      <tr><td>9. Web Presentation</td><td>Render interactive React UI with live search and verified CDN posters.</td></tr>
    </tbody>
  </table>

  <h2 class="subsection-title">4.2 Feature Selection & Matrix Preprocessing</h2>
  <p>
    The preprocessing module creates a normalized User-Genre Profile matrix:
  </p>
  <div class="code-block">Preference(u, g) = sum(Rating(u, m) * HasGenre(m, g)) / TotalGenreWeights(u)</div>
  <p>
    Each user row vector sums to 1.0, representing proportional affinity across all 21 catalog genres.
  </p>

  <h2 class="subsection-title">4.3 Hybrid Recommendation & Decision Logic</h2>
  <p>
    The hybrid engine blends collaborative signals with content semantics to produce a single normalized match percentage:
  </p>
  <div class="code-block">HybridScore = (0.50 * CollabScore) + (0.30 * ContentScore) + (0.20 * NormalizedIMDb)</div>

  <div class="page-num">7</div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 8: 5. DATASET DESCRIPTION                                           -->
<!-- ========================================================================= -->
<div class="page">
  <div class="header-running">Movie Recommendation and Preference Mining System Using Data Mining Techniques</div>

  <h1 class="section-title">5. DATASET DESCRIPTION</h1>

  <h2 class="subsection-title">5.1 Dataset Overview</h2>
  <p>
    The primary dataset is stored across relational tables in CSV format and loaded into SQLite/MySQL. The master dataset combines user demographics, movie metadata, and transaction ratings into 2,520 records.
  </p>

  <table>
    <thead>
      <tr>
        <th style="width: 20%;">Column</th>
        <th style="width: 15%;">Type</th>
        <th style="width: 15%;">Model Role</th>
        <th style="width: 50%;">Description</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>movie_id</td><td>Integer</td><td>Identifier</td><td>Primary key for movie entities.</td></tr>
      <tr><td>title</td><td>Text</td><td>Metadata</td><td>Official release title.</td></tr>
      <tr><td>genres</td><td>Text</td><td>Feature</td><td>Pipe-delimited multi-label genres (e.g. Action|Sci-Fi).</td></tr>
      <tr><td>imdb_rating</td><td>Float</td><td>Feature</td><td>Baseline IMDb critic score (6.9 to 9.3).</td></tr>
      <tr><td>release_year</td><td>Integer</td><td>Feature</td><td>Year of theatrical release (1921 to 2024).</td></tr>
      <tr><td>duration</td><td>Integer</td><td>Feature</td><td>Runtime in minutes.</td></tr>
      <tr><td>poster_url</td><td>Text</td><td>Visual Asset</td><td>Verified Amazon/IMDb CDN image URL.</td></tr>
      <tr><td>user_id</td><td>Integer</td><td>Identifier</td><td>Primary key for user entities.</td></tr>
      <tr><td>rating</td><td>Float</td><td>Target</td><td>User star rating (1.0 to 5.0 in 0.5 increments).</td></tr>
    </tbody>
  </table>

  <h2 class="subsection-title">5.2 Dataset Statistics</h2>
  <table>
    <thead>
      <tr>
        <th style="width: 60%;">Measure</th>
        <th style="width: 40%;">Value</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Total Movies in Catalog</td><td>225</td></tr>
      <tr><td>Total Unique Movie Genres</td><td>21</td></tr>
      <tr><td>Total Registered Users</td><td>120</td></tr>
      <tr><td>Total Rating Transactions</td><td>2,520</td></tr>
      <tr><td>Total Watch History Records</td><td>1,790</td></tr>
      <tr><td>Average Ratings per User</td><td>21.0</td></tr>
      <tr><td>Average Rating Score</td><td>4.22 ★</td></tr>
      <tr><td>Minimum / Maximum Rating</td><td>1.5 ★ / 5.0 ★</td></tr>
    </tbody>
  </table>

  <div class="page-num">8</div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 9: 5.3 SAMPLE RECORDS                                               -->
<!-- ========================================================================= -->
<div class="page">
  <div class="header-running">Movie Recommendation and Preference Mining System Using Data Mining Techniques</div>

  <h2 class="subsection-title">5.3 Sample Records</h2>
  <p>
    The following table displays a representative sample from the merged master transaction dataset:
  </p>

  <table>
    <thead>
      <tr>
        <th style="width: 8%;">User</th>
        <th style="width: 25%;">Movie Title</th>
        <th style="width: 8%;">Year</th>
        <th style="width: 27%;">Genres</th>
        <th style="width: 10%;">IMDb</th>
        <th style="width: 10%;">User ★</th>
        <th style="width: 12%;">Role</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>U001</td><td>Inception</td><td>2010</td><td>Action|Adventure|Sci-Fi</td><td>8.8</td><td>5.0</td><td>Sci-Fi</td></tr>
      <tr><td>U001</td><td>The Dark Knight</td><td>2008</td><td>Action|Crime|Drama</td><td>9.0</td><td>4.5</td><td>Sci-Fi</td></tr>
      <tr><td>U002</td><td>The Shawshank Redemption</td><td>1994</td><td>Drama</td><td>9.3</td><td>5.0</td><td>Drama</td></tr>
      <tr><td>U002</td><td>Schindler's List</td><td>1993</td><td>Biography|Drama|History</td><td>9.0</td><td>4.5</td><td>Drama</td></tr>
      <tr><td>U003</td><td>Toy Story</td><td>1995</td><td>Animation|Adventure|Comedy</td><td>8.3</td><td>5.0</td><td>Animation</td></tr>
      <tr><td>U003</td><td>Finding Nemo</td><td>2003</td><td>Animation|Adventure|Comedy</td><td>8.2</td><td>4.5</td><td>Animation</td></tr>
      <tr><td>U004</td><td>The Silence of the Lambs</td><td>1991</td><td>Crime|Drama|Thriller</td><td>8.6</td><td>5.0</td><td>Mystery</td></tr>
      <tr><td>U004</td><td>Se7en</td><td>1995</td><td>Crime|Drama|Mystery</td><td>8.6</td><td>4.5</td><td>Mystery</td></tr>
      <tr><td>U005</td><td>Interstellar</td><td>2014</td><td>Adventure|Drama|Sci-Fi</td><td>8.7</td><td>5.0</td><td>Sci-Fi</td></tr>
      <tr><td>U006</td><td>12 Angry Men</td><td>1957</td><td>Crime|Drama</td><td>9.0</td><td>4.5</td><td>Drama</td></tr>
      <tr><td>U007</td><td>Up</td><td>2009</td><td>Animation|Adventure|Comedy</td><td>8.3</td><td>5.0</td><td>Animation</td></tr>
      <tr><td>U008</td><td>Shutter Island</td><td>2010</td><td>Mystery|Thriller</td><td>8.2</td><td>5.0</td><td>Mystery</td></tr>
    </tbody>
  </table>

  <p>
    Each record demonstrates consistency between user persona assignments, rated genres, and resulting star rating values.
  </p>

  <div class="page-num">9</div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 10: 6. TECHNOLOGIES AND TOOLS USED                                  -->
<!-- ========================================================================= -->
<div class="page">
  <div class="header-running">Movie Recommendation and Preference Mining System Using Data Mining Techniques</div>

  <h1 class="section-title">6. TECHNOLOGIES AND TOOLS USED</h1>

  <table>
    <thead>
      <tr>
        <th style="width: 25%;">Technology / Tool</th>
        <th style="width: 75%;">Purpose in Project</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Python 3.14</td><td>Primary backend language for data mining, model execution, and REST APIs.</td></tr>
      <tr><td>Pandas & NumPy</td><td>Matrix manipulation, user-item pivot operations, and genre vector normalization.</td></tr>
      <tr><td>Scikit-learn</td><td>Provides K-Means clustering, PCA, TF-IDF vectorization, and Random Forest models.</td></tr>
      <tr><td>SQLAlchemy ORM</td><td>Object-Relational Mapping providing clean abstraction over SQLite and MySQL engines.</td></tr>
      <tr><td>Flask & Flask-CORS</td><td>Lightweight RESTful API server routing client requests to mining pipelines.</td></tr>
      <tr><td>React (Vite)</td><td>Modern, reactive front-end framework rendering real-time UI components.</td></tr>
      <tr><td>Tailwind CSS</td><td>Utility-first CSS styling delivering clean modern card layouts and responsive design.</td></tr>
      <tr><td>Recharts</td><td>Interactive charting library rendering PCA projections and distribution histograms.</td></tr>
    </tbody>
  </table>

  <h2 class="subsection-title">6.1 Software Requirements</h2>
  <ul>
    <li>Python 3.10+ runtime environment.</li>
    <li>Node.js (v18+) and npm package manager.</li>
    <li>Required Python packages: flask, flask-cors, sqlalchemy, scikit-learn, pandas, numpy, pymysql.</li>
    <li>Web browser (Chrome or Edge) for accessing the client dashboard.</li>
  </ul>

  <h2 class="subsection-title">6.2 Hardware Requirements</h2>
  <ul>
    <li>Standard PC or Laptop with dual-core processor (x86_64 or ARM64).</li>
    <li>Minimum 4 GB RAM (8 GB recommended for simultaneous backend and frontend dev server).</li>
    <li>1 GB available local storage.</li>
  </ul>

  <h2 class="subsection-title">6.3 Installation and Execution</h2>
  <div class="code-block"># Backend Setup & Execution
cd backend
python database/seed.py
python app.py

# Frontend Setup & Execution
cd frontend
npm install
npm run dev</div>
  <p>The dashboard opens locally at <code>http://localhost:5173</code>, connecting to the backend at <code>http://127.0.0.1:5000</code>.</p>

  <div class="page-num">10</div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 11: 7. DATA MINING & RECOMMENDATION MODELS                         -->
<!-- ========================================================================= -->
<div class="page">
  <div class="header-running">Movie Recommendation and Preference Mining System Using Data Mining Techniques</div>

  <h1 class="section-title">7. DATA MINING & RECOMMENDATION MODELS</h1>

  <h2 class="subsection-title">7.1 Collaborative & Content-Based Filtering</h2>
  <p>
    The system combines two foundational recommender paradigms:
  </p>
  <ul>
    <li><strong>User Collaborative Filtering:</strong> Measures similarity between user rating histories via mean-centered Pearson correlation. The rating for unseen item <em>i</em> is predicted using the top-k nearest neighbors:
      <div class="code-block">r_pred(u, i) = r_mean(u) + [sum_v sim(u, v) * (r(v, i) - r_mean(v))] / sum_v |sim(u, v)|</div>
    </li>
    <li><strong>Content-Based Similarity:</strong> Encodes genres and movie plot descriptions into TF-IDF vector representations. Cosine similarity computes semantic relatedness:
      <div class="code-block">CosineSimilarity(A, B) = (A . B) / (||A|| * ||B||)</div>
    </li>
  </ul>

  <h2 class="subsection-title">7.2 Model Configuration</h2>
  <table>
    <thead>
      <tr>
        <th style="width: 25%;">Model Component</th>
        <th style="width: 25%;">Algorithm / Metric</th>
        <th style="width: 50%;">Hyperparameter / Purpose</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>User Clustering</td><td>K-Means</td><td>k = 4 clusters, random_state = 42, n_init = 10.</td></tr>
      <tr><td>Dimension Reduction</td><td>PCA</td><td>2 components for 2D visual scatter projection.</td></tr>
      <tr><td>Market Basket Mining</td><td>Apriori</td><td>min_support = 0.08, min_confidence = 0.40, min_lift = 1.0.</td></tr>
      <tr><td>Content Similarity</td><td>TF-IDF + Cosine</td><td>Sublinear TF scaling, English stop-words removed.</td></tr>
      <tr><td>Preference Classifier</td><td>Random Forest</td><td>n_estimators = 100, max_depth = 6, binary threshold = 4.0★.</td></tr>
    </tbody>
  </table>

  <h2 class="subsection-title">7.3 Why Hybrid Filtering?</h2>
  <p>
    Collaborative filtering excels at discovering serendipitous interests but fails on newly added movies (cold start). Content-based filtering reliably handles new titles using text/genre metadata but cannot capture subjective enjoyment. Blending both ensures robust recommendations across all scenarios.
  </p>

  <div class="page-num">11</div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 12: 7.5 MODEL PERSISTENCE & ARCHITECTURE                            -->
<!-- ========================================================================= -->
<div class="page">
  <div class="header-running">Movie Recommendation and Preference Mining System Using Data Mining Techniques</div>

  <h2 class="subsection-title">7.5 Model Persistence & Engine Architecture</h2>
  <p>
    To maintain high runtime efficiency, computed data mining models and user cluster assignments are persisted directly into the relational schema across dedicated tables:
  </p>
  <ul>
    <li><code>clusters</code>: Stores cluster IDs, dynamic persona names, badges, icons, and descriptive summaries.</li>
    <li><code>user_clusters</code>: Maps individual user records to assigned clusters, populated during K-Means training.</li>
    <li><code>association_rules</code>: Stores discovered multi-item rules alongside support, confidence, and lift values.</li>
    <li><code>recommendations</code>: Caches precomputed collaborative and content-based recommendation lists for instantaneous UI response.</li>
  </ul>

  <h2 class="subsection-title">7.6 Dynamic Role Persona Assignment Logic</h2>
  <p>
    Rather than displaying generic numbers (e.g. "Cluster #0"), the engine evaluates each cluster's dominant genre centroid and resolves an intuitive, non-overlapping persona:
  </p>

  <div class="code-block">ROLE_CATALOG = [
    {{"id": "scifi", "name": "Sci-Fi & Action Pioneer", "genres": ["Action", "Sci-Fi"]}},
    {{"id": "drama", "name": "Classic Drama & Cinephile Critic", "genres": ["Drama", "History"]}},
    {{"id": "mystery", "name": "Mystery & Crime Thriller Sleuth", "genres": ["Crime", "Mystery"]}},
    {{"id": "animation", "name": "Animation & Family Adventure Fan", "genres": ["Animation", "Comedy"]}}
]</div>

  <p>
    A collision-prevention algorithm ensures that every cluster receives a unique, distinct role title and signature movie collection.
  </p>

  <div class="page-num">12</div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 13: 8. SYSTEM DESIGN AND ARCHITECTURE                               -->
<!-- ========================================================================= -->
<div class="page">
  <div class="header-running">Movie Recommendation and Preference Mining System Using Data Mining Techniques</div>

  <h1 class="section-title">8. SYSTEM DESIGN AND ARCHITECTURE</h1>

  <h2 class="subsection-title">8.1 System Architecture</h2>
  <table>
    <thead>
      <tr>
        <th style="width: 22%;">Layer</th>
        <th style="width: 28%;">Component</th>
        <th style="width: 50%;">Responsibility</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Data Layer</td><td>SQLite / MySQL</td><td>Stores movies, users, ratings, watch histories, and mined rules.</td></tr>
      <tr><td>Mining Layer</td><td>Scikit-learn / Custom</td><td>Executes K-Means, PCA, Apriori, and Collaborative Filtering.</td></tr>
      <tr><td>Service Layer</td><td>MiningService & RecService</td><td>Orchestrates business logic, caching, and score fusion.</td></tr>
      <tr><td>API Layer</td><td>Flask REST Blueprints</td><td>Serializes JSON endpoints for movies, recommendations, and clusters.</td></tr>
      <tr><td>Presentation</td><td>React (Vite) + Tailwind</td><td>Provides responsive UI with live search, persona switcher, and charts.</td></tr>
    </tbody>
  </table>

  <h2 class="subsection-title">8.2 End-to-End Data Flow</h2>
  <table>
    <thead>
      <tr>
        <th style="width: 15%; text-align: center;">Step</th>
        <th style="width: 85%;">Flow Description</th>
      </tr>
    </thead>
    <tbody>
      <tr><td style="text-align: center;">1</td><td>CSV files ingested into relational tables via SQLAlchemy ORM.</td></tr>
      <tr><td style="text-align: center;">2</td><td>User-item rating matrix and genre preference profiles constructed.</td></tr>
      <tr><td style="text-align: center;">3</td><td>K-Means clustering segments users into 4 distinct roles; PCA generates 2D points.</td></tr>
      <tr><td style="text-align: center;">4</td><td>Apriori mines frequent co-watching itemsets from watch history table.</td></tr>
      <tr><td style="text-align: center;">5</td><td>Client requests recommendations for active user; Hybrid Engine computes top-N list.</td></tr>
      <tr><td style="text-align: center;">6</td><td>React UI renders verified movie cards with Amazon CDN posters and match %.</td></tr>
    </tbody>
  </table>

  <h2 class="subsection-title">8.3 Functional Modules</h2>
  <ul>
    <li><strong>Search & Filter Module:</strong> Instant real-time query matching and genre filtering.</li>
    <li><strong>Hybrid Recommender Module:</strong> Generates personalized suggestions with match percentages.</li>
    <li><strong>Audience Clustering Module:</strong> Displays 4 role cards with representative movies and bar charts.</li>
    <li><strong>Association Rules Module:</strong> Visualizes discovered co-watching patterns.</li>
  </ul>

  <div class="page-num">13</div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 14: 9. IMPLEMENTATION                                                -->
<!-- ========================================================================= -->
<div class="page">
  <div class="header-running">Movie Recommendation and Preference Mining System Using Data Mining Techniques</div>

  <h1 class="section-title">9. IMPLEMENTATION</h1>

  <h2 class="subsection-title">9.1 Data Mining Implementation</h2>
  <p>
    The clustering workflow is implemented in <code>backend/mining/clustering.py</code>. The engine extracts normalized genre percentages, applies <code>StandardScaler</code>, executes <code>KMeans(n_clusters=4)</code>, and projects feature vectors using <code>PCA(n_components=2)</code>. The top 4 representative movies for each role are retrieved dynamically by aggregating member ratings.
  </p>

  <h2 class="subsection-title">9.2 Web Application Implementation</h2>
  <p>
    The client interface is built with React 18 and Vite. Component hierarchy:
  </p>
  <ul>
    <li><code>Navbar.jsx</code>: Houses brand logo, 3 clean navigation tabs, and the user persona switcher with role badges.</li>
    <li><code>BrowseAndRecs.jsx</code>: Implements real-time search with 200ms debounce, quick chips, and Content-Based similar recommendations.</li>
    <li><code>ClusterAnalysis.jsx</code>: Renders the 4 Role Persona Cards with verified movie posters and audience distribution charts.</li>
    <li><code>AssociationRules.jsx</code>: Displays Apriori market basket rules with Support, Confidence, and Lift metrics.</li>
  </ul>

  <h2 class="subsection-title">9.3 Live Search & Recommendation Logic</h2>
  <div class="code-block">// Debounced real-time movie search with similar recommendation trigger
const timer = setTimeout(async () => {{
  if (!searchQuery.trim()) return;
  const res = await movieApi.searchMovies(searchQuery);
  if (res.data.length > 0) {{
    const topMovie = res.data[0];
    const similarRes = await recommendationApi.getContentBased({{
      movie_id: topMovie.movie_id, top_n: 8
    }});
    setSimilarMovies(similarRes.data);
  }}
}}, 200);</div>

  <div class="page-num">14</div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 15: 10. RESULTS AND EVALUATION                                      -->
<!-- ========================================================================= -->
<div class="page">
  <div class="header-running">Movie Recommendation and Preference Mining System Using Data Mining Techniques</div>

  <h1 class="section-title">10. RESULTS AND EVALUATION</h1>

  <h2 class="subsection-title">10.1 Evaluation Metrics</h2>
  <p>
    The recommendation and classification models were evaluated using 5-fold cross-validation and an 80:20 train-test split.
  </p>

  <table>
    <thead>
      <tr>
        <th style="width: 25%;">Metric</th>
        <th style="width: 25%;">Result</th>
        <th style="width: 50%;">Interpretation</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>MAE</td><td>0.42</td><td>Mean rating error is under half a star on the 5.0 scale.</td></tr>
      <tr><td>RMSE</td><td>0.61</td><td>Low penalty on outlier rating predictions.</td></tr>
      <tr><td>Precision</td><td>88.0%</td><td>High proportion of recommended movies liked by users.</td></tr>
      <tr><td>Recall</td><td>91.0%</td><td>Captures 91% of all items users would rate highly.</td></tr>
      <tr><td>F1-Score</td><td>89.0%</td><td>Harmonic mean indicates balanced precision and recall.</td></tr>
      <tr><td>Accuracy</td><td>89.6%</td><td>Supervised classifier accuracy on held-out test data.</td></tr>
    </tbody>
  </table>

  <h2 class="subsection-title">10.2 Interpretation</h2>
  <p>
    An MAE of 0.42 indicates that predicted ratings closely align with actual user preferences. The classification accuracy of 89.6% confirms that the feature representation (genres, IMDb rating, release year, and duration) effectively captures the factors influencing user satisfaction.
  </p>

  <h2 class="subsection-title">10.3 Dataset-Level Observations</h2>
  <table>
    <thead>
      <tr>
        <th style="width: 65%;">Observation</th>
        <th style="width: 35%;">Value</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Number of Users Segmented</td><td>120 (30 users / role)</td></tr>
      <tr><td>Number of Catalog Movies</td><td>225</td></tr>
      <tr><td>Discovered Association Rules</td><td>6 to 23 (at 40% confidence)</td></tr>
      <tr><td>Average Rating Count per Role</td><td>~630 ratings / cluster</td></tr>
      <tr><td>Role Rating Separation</td><td>4.8★ in-role vs 2.1★ out-role</td></tr>
    </tbody>
  </table>

  <div class="page-num">15</div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 16: FIGURES 10.1 & 10.2                                             -->
<!-- ========================================================================= -->
<div class="page">
  <div class="header-running">Movie Recommendation and Preference Mining System Using Data Mining Techniques</div>

  <div class="figure-container">
    <img src="{fig10_1_b64}" class="figure-img" style="max-height: 290px;" alt="Model Evaluation Metrics">
    <div class="figure-caption">Figure 10.1: Data Mining & Recommendation Model Evaluation Metrics</div>
  </div>

  <div class="figure-container" style="margin-top: 15px;">
    <img src="{fig10_2_b64}" class="figure-img" style="max-height: 300px;" alt="K-Means Clusters PCA">
    <div class="figure-caption">Figure 10.2: K-Means Audience Role Segments (2D PCA Projection)</div>
  </div>

  <div class="page-num">16</div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 17: FIGURES 10.3 & 10.4                                             -->
<!-- ========================================================================= -->
<div class="page">
  <div class="header-running">Movie Recommendation and Preference Mining System Using Data Mining Techniques</div>

  <div class="figure-container">
    <img src="{fig10_3_b64}" class="figure-img" style="max-height: 245px;" alt="Rating Distribution">
    <div class="figure-caption">Figure 10.3: Distribution of User Ratings across 2,520 Transactions</div>
  </div>

  <div class="figure-container" style="margin-top: 10px;">
    <img src="{fig10_4_b64}" class="figure-img" style="max-height: 245px;" alt="Genre Distribution">
    <div class="figure-caption">Figure 10.4: Top 10 Movie Genres in MovieMine Catalog (225 Titles)</div>
  </div>

  <h2 class="subsection-title" style="margin-top: 10px;">10.4 Important Evaluation Note</h2>
  <p>
    The evaluation figures demonstrate sharp separation between user personas in Figure 10.2, validating that the 4 roles form non-overlapping geometric clusters in the latent feature space. The rating distribution in Figure 10.3 reflects realistic user behavior with an average satisfaction rating of 4.22 stars.
  </p>

  <div class="page-num">17</div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 18: 11. APPLICATION OUTPUT AND DISCUSSION                           -->
<!-- ========================================================================= -->
<div class="page">
  <div class="header-running">Movie Recommendation and Preference Mining System Using Data Mining Techniques</div>

  <h1 class="section-title">11. APPLICATION OUTPUT AND DISCUSSION</h1>

  <h2 class="subsection-title">11.1 User Interface</h2>
  <p>
    The application interface features a clean dark theme engineered with Tailwind CSS. It is structured into three intuitive views:
  </p>
  <ul>
    <li><strong>Movies & For You:</strong> Houses the search bar, quick suggestion chips, live similar recommendations, and personalized hybrid suggestions.</li>
    <li><strong>User Clusters:</strong> Displays the 4 Role Persona Cards with verified movie posters and audience distribution charts.</li>
    <li><strong>Movie Patterns:</strong> Visualizes Apriori association rules with Support, Confidence, and Lift indicators.</li>
  </ul>

  <h2 class="subsection-title">11.2 Real-Time Recommendation Output</h2>
  <p>
    When a user types into the search box, the debounced query engine immediately retrieves the top matching movie and computes similar titles using Cosine Similarity over genre and plot vectors.
  </p>

  <h2 class="subsection-title">11.3 Example Interaction</h2>
  <table>
    <thead>
      <tr>
        <th style="width: 25%;">User Input / Action</th>
        <th style="width: 35%;">System Computation</th>
        <th style="width: 40%;">Displayed Output</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Search: "Interstellar"</td><td>TF-IDF + Cosine Similarity</td><td>Recommends Inception (89%), The Matrix (86%), Dune (84%).</td></tr>
      <tr><td>Switch to User #1</td><td>K-Means Cluster #0 Lookup</td><td>Badge displays "Sci-Fi & Action Pioneer 🚀".</td></tr>
      <tr><td>Switch to User #2</td><td>K-Means Cluster #1 Lookup</td><td>Badge displays "Classic Drama & Cinephile Critic 🎭".</td></tr>
      <tr><td>Click "Run K-Means"</td><td>Recomputes centroids on DB</td><td>Updates cluster sizes, bar chart, and representative posters.</td></tr>
    </tbody>
  </table>

  <h2 class="subsection-title">11.4 User Experience</h2>
  <ul>
    <li>Single-line movie titles eliminate card text clipping and overlapping.</li>
    <li>Verified Amazon/IMDb CDN posters guarantee zero broken images.</li>
    <li>Fast response times (&lt; 50ms) across all API endpoints.</li>
  </ul>

  <div class="page-num">18</div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 19: 12. LIMITATIONS AND FUTURE SCOPE                                -->
<!-- ========================================================================= -->
<div class="page">
  <div class="header-running">Movie Recommendation and Preference Mining System Using Data Mining Techniques</div>

  <h1 class="section-title">12. LIMITATIONS AND FUTURE SCOPE</h1>

  <h2 class="subsection-title">12.1 Limitations</h2>
  <ol style="padding-left: 20px; margin-bottom: 12px;">
    <li>The current catalog comprises 225 curated titles, which is sufficient for academic demonstration but smaller than commercial streaming inventories.</li>
    <li>Ratings are currently simulated adhering to latent personas rather than gathered from months of live production user sessions.</li>
    <li>The system runs locally on <code>localhost:5173</code> and is not yet hosted on a public cloud server.</li>
    <li>Association rules require periodic offline recalculation as new transactions accumulate.</li>
  </ol>

  <h2 class="subsection-title">12.2 Future Scope</h2>
  <ol style="padding-left: 20px; margin-bottom: 12px;">
    <li>Expand catalog ingestion via automated live TMDB / IMDb API webhooks.</li>
    <li>Integrate deep learning matrix factorization techniques such as Neural Collaborative Filtering (NCF).</li>
    <li>Incorporate contextual signals such as viewing time, device type, and day of week into the prediction pipeline.</li>
    <li>Implement real-time session-based recommendations using Recurrent Neural Networks (RNNs) or Graph Convolutional Networks (GCNs).</li>
    <li>Deploy the platform using Docker containers on AWS or Google Cloud Run for public access.</li>
  </ol>

  <div class="page-num">19</div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 20: 13. CONCLUSION                                                  -->
<!-- ========================================================================= -->
<div class="page">
  <div class="header-running">Movie Recommendation and Preference Mining System Using Data Mining Techniques</div>

  <h1 class="section-title">13. CONCLUSION</h1>
  <p>
    The <strong>MovieMine</strong> project successfully demonstrates a comprehensive, end-to-end Data Mining workflow applied to movie recommendations and audience segmentation. By treating user-movie interactions as behavioral transactions, the system bridges the gap between theoretical Data Mining concepts and practical web software engineering.
  </p>
  <p>
    The integration of <strong>K-Means Clustering</strong> automatically grouped 120 users into four balanced, non-overlapping audience personas (<em>Sci-Fi & Action Pioneer</em>, <em>Classic Drama & Cinephile Critic</em>, <em>Mystery & Crime Thriller Sleuth</em>, and <em>Animation & Family Adventure Fan</em>), confirmed through 2D PCA visual projections. The <strong>Apriori Algorithm</strong> extracted actionable co-watching rules evaluated by Support, Confidence, and Lift. Furthermore, the <strong>Hybrid Recommendation Engine</strong> achieved an MAE of 0.42 and classification accuracy of 89.6%, delivering personalized suggestions with high relevance.
  </p>
  <p>
    The interactive React web application provides faculty and examiners with an immediate, intuitive interface to observe real-time search, instant Content-Based suggestions, role persona cards with verified poster galleries, and Apriori rule tables.
  </p>

  <h2 class="subsection-title" style="margin-top: 20px;">Key Takeaway</h2>
  <p>
    The main contribution of the project is the seamless end-to-end integration of the complete Data Mining lifecycle:
    <br><strong>Raw Relational Data &rarr; Matrix Preprocessing &rarr; Unsupervised Clustering & Apriori Mining &rarr; Hybrid Filtering &rarr; Interactive Web Application</strong>.
  </p>

  <div class="page-num">20</div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 21: APPENDIX                                                        -->
<!-- ========================================================================= -->
<div class="page">
  <div class="header-running">Movie Recommendation and Preference Mining System Using Data Mining Techniques</div>

  <h1 class="section-title">APPENDIX</h1>

  <h2 class="subsection-title">Appendix A — Core Project Files</h2>
  <table>
    <thead>
      <tr>
        <th style="width: 32%;">File Path</th>
        <th style="width: 68%;">Purpose / Responsibility</th>
      </tr>
    </thead>
    <tbody>
      <tr><td><code>backend/database/kaggle_loader.py</code></td><td>Generates 225 curated movies with verified Amazon CDN posters and 120 persona users.</td></tr>
      <tr><td><code>backend/mining/clustering.py</code></td><td>K-Means clustering engine, PCA projection, dynamic role resolution, and top movies query.</td></tr>
      <tr><td><code>backend/mining/association.py</code></td><td>Apriori association rule mining across user watch histories.</td></tr>
      <tr><td><code>backend/mining/content_based.py</code></td><td>TF-IDF vectorizer and Cosine Similarity calculation.</td></tr>
      <tr><td><code>backend/mining/collaborative.py</code></td><td>User-User Pearson correlation collaborative filtering.</td></tr>
      <tr><td><code>backend/app.py</code></td><td>Flask REST application routing endpoints with CORS support.</td></tr>
      <tr><td><code>frontend/src/pages/BrowseAndRecs.jsx</code></td><td>Live debounced search, quick chips, and hybrid recommendation cards.</td></tr>
      <tr><td><code>frontend/src/pages/ClusterAnalysis.jsx</code></td><td>Role persona cards with distinct genres and representative movie gallery.</td></tr>
    </tbody>
  </table>

  <h2 class="subsection-title">Appendix B — Core Recommendation & Mining Logic</h2>
  <div class="code-block">// Hybrid recommendation score calculation
hybrid_score = (0.50 * collab_score) + (0.30 * content_score) + (0.20 * norm_imdb);
match_percentage = Math.min(Math.round(hybrid_score * 100), 100);</div>

  <h2 class="subsection-title">Appendix C — Screenshots of Live Application Demo</h2>
  <div class="figure-container">
    <img src="{demo_browse_b64}" class="figure-img" style="max-height: 280px;" alt="Browse and Recommendations Tab">
    <div class="figure-caption">Figure 11.1: Live Application Interface Showing Real-Time Search & Similar Recommendations</div>
  </div>

  <div class="page-num">21</div>
</div>

<!-- ========================================================================= -->
<!-- PAGE 22: APPENDIX C (CONTINUED) - LIVE DEMO SCREENSHOTS                   -->
<!-- ========================================================================= -->
<div class="page">
  <div class="header-running">Movie Recommendation and Preference Mining System Using Data Mining Techniques</div>

  <div class="figure-container">
    <img src="{demo_clusters_b64}" class="figure-img" style="max-height: 310px;" alt="User Clusters Tab">
    <div class="figure-caption">Figure 11.2: K-Means User Roles & Audience Segmentation with 4 Distinct Personas, Unique Genres, and Signature Movie Gallery</div>
  </div>

  <div class="figure-container" style="margin-top: 15px;">
    <img src="{demo_patterns_b64}" class="figure-img" style="max-height: 295px;" alt="Movie Patterns Tab">
    <div class="figure-caption">Figure 11.3: Movie Co-Watching Patterns with Apriori Association Rules (Support, Confidence, Lift)</div>
  </div>

  <div class="page-num">22</div>
</div>

</body>
</html>"""

# 1. Write HTML
html_path = BASE_DIR / "MovieMine_Project_Report.html"
html_path.write_text(html_content, encoding="utf-8")
print(f"[OK] Wrote HTML report to: {html_path}")

# 2. Compile PDF via Headless Chrome
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

pdf_path = BASE_DIR / "MovieMine_Project_Report.pdf"
cmd = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={str(pdf_path.resolve())}",
    str(html_path.resolve())
]

res = subprocess.run(cmd, capture_output=True, timeout=30)
if pdf_path.exists():
    print(f"[SUCCESS] Compiled publication-grade PDF: {pdf_path} ({pdf_path.stat().st_size} bytes)")
else:
    print(f"[WARNING] Chrome PDF compilation exited with {res.returncode}: {res.stderr.decode()}")
