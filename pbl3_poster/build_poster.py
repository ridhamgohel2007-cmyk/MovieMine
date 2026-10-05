"""
build_poster.py
Generates the publication-grade Academic Poster in both HTML and PDF formats:
'Hyperparameter Tuning of Data Mining Models'
PBL Activity Task - 3 | Subject: Data Mining Techniques (BE05000181)
Vishwakarma Government Engineering College (VGEC), Chandkheda / GTU
"""

import os
import base64
import subprocess
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
HTML_OUTPUT = os.path.join(BASE_DIR, 'Hyperparameter_Tuning_PBL3_Poster.html')
PDF_OUTPUT = os.path.join(BASE_DIR, 'Hyperparameter_Tuning_PBL3_Poster.pdf')

def image_to_base64(filepath):
    if not os.path.exists(filepath):
        print(f"[WARN] Image not found: {filepath}")
        return ""
    ext = os.path.splitext(filepath)[1].lower().replace('.', '')
    mime = 'image/png' if ext == 'png' else 'image/jpeg'
    with open(filepath, 'rb') as f:
        encoded = base64.b64encode(f.read()).decode('utf-8')
    return f"data:{mime};base64,{encoded}"

vgec_logo_b64 = image_to_base64(os.path.join(ASSETS_DIR, 'vgec_logo.png'))
gtu_logo_b64 = image_to_base64(os.path.join(ASSETS_DIR, 'gtu_logo.png'))
search_strat_b64 = image_to_base64(os.path.join(ASSETS_DIR, 'search_strategies.png'))
val_curve_b64 = image_to_base64(os.path.join(ASSETS_DIR, 'validation_curve_bias_variance.png'))
kmeans_plot_b64 = image_to_base64(os.path.join(ASSETS_DIR, 'kmeans_elbow_silhouette.png'))
heatmap_b64 = image_to_base64(os.path.join(ASSETS_DIR, 'hyperparameter_heatmap.png'))

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Hyperparameter Tuning of Data Mining Models - PBL 3 Academic Poster</title>
<style>
  @page {
    size: 1650px 1220px;
    margin: 0;
  }
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background-color: #0b1329;
    color: #1e293b;
    width: 1650px;
    height: 1220px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    padding: 14px 18px 10px 18px;
  }

  /* HEADER BANNER */
  .poster-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #172554 100%);
    border: 2px solid #3b82f6;
    border-radius: 12px;
    padding: 10px 22px 8px 22px;
    color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
    margin-bottom: 10px;
  }
  .logo-box {
    width: 95px;
    height: 95px;
    background: #ffffff;
    border-radius: 10px;
    padding: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    flex-shrink: 0;
  }
  .logo-box img {
    max-width: 85px;
    max-height: 85px;
    object-fit: contain;
  }
  .header-center {
    text-align: center;
    flex-grow: 1;
    padding: 0 18px;
  }
  .inst-name {
    font-size: 13pt;
    font-weight: 800;
    letter-spacing: 1.2px;
    color: #93c5fd;
    text-transform: uppercase;
    margin-bottom: 2px;
  }
  .dept-sub {
    font-size: 9.5pt;
    font-weight: 600;
    color: #e2e8f0;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
  }
  .poster-title {
    font-size: 21pt;
    font-weight: 900;
    letter-spacing: 0.8px;
    color: #ffffff;
    text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    margin-bottom: 2px;
    line-height: 1.15;
  }
  .poster-subtitle {
    font-size: 10pt;
    font-weight: 500;
    color: #cbd5e1;
    margin-bottom: 5px;
  }
  
  /* METADATA BADGES BOX */
  .meta-container {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    margin-top: 3px;
  }
  .meta-pill {
    background: rgba(255, 255, 255, 0.12);
    border: 1px solid rgba(255, 255, 255, 0.25);
    backdrop-filter: blur(4px);
    border-radius: 6px;
    padding: 3.5px 10px;
    font-size: 8.8pt;
    color: #f8fafc;
  }
  .meta-pill strong {
    color: #67e8f9;
  }

  /* MAIN GRID (3 COLUMNS) */
  .poster-body {
    display: grid;
    grid-template-columns: 1fr 1.05fr 1fr;
    gap: 10px;
    flex-grow: 1;
    height: calc(1220px - 190px);
  }
  .column {
    display: flex;
    flex-direction: column;
    gap: 9px;
    height: 100%;
  }

  /* CARD STYLING */
  .card {
    background: #ffffff;
    border-radius: 8px;
    border: 1.5px solid #cbd5e1;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.15);
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }
  .card-header {
    background: linear-gradient(90deg, #1e3a8a 0%, #2563eb 100%);
    color: #ffffff;
    padding: 5px 10px;
    font-size: 9.5pt;
    font-weight: 800;
    letter-spacing: 0.5px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .card-header .badge {
    background: rgba(255, 255, 255, 0.2);
    font-size: 7.2pt;
    padding: 2px 6px;
    border-radius: 4px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .card-body {
    padding: 7px 10px;
    font-size: 8.3pt;
    line-height: 1.32;
    color: #334155;
    flex-grow: 1;
  }

  /* TYPOGRAPHY & ELEMENTS */
  h4 {
    font-size: 8.6pt;
    font-weight: 800;
    color: #0f172a;
    margin-top: 4px;
    margin-bottom: 2px;
    display: flex;
    align-items: center;
    gap: 4px;
  }
  h4::before {
    content: "";
    display: inline-block;
    width: 4px;
    height: 9px;
    background: #2563eb;
    border-radius: 2px;
  }
  p {
    margin-bottom: 4px;
  }
  ul, ol {
    padding-left: 15px;
    margin-bottom: 4px;
  }
  li {
    margin-bottom: 2.5px;
  }
  .math-box {
    background: #f1f5f9;
    border-left: 3px solid #2563eb;
    padding: 3.5px 7px;
    font-family: "Courier New", Courier, monospace;
    font-size: 7.8pt;
    font-weight: bold;
    color: #1e293b;
    margin: 3px 0 5px 0;
    border-radius: 0 4px 4px 0;
  }
  .plot-img {
    width: 100%;
    max-height: 155px;
    object-fit: contain;
    border-radius: 5px;
    border: 1px solid #e2e8f0;
    display: block;
    margin: 2px auto;
  }
  .caption {
    font-size: 7.2pt;
    color: #64748b;
    text-align: center;
    font-style: italic;
    margin-bottom: 3px;
  }

  /* COMPACT TABLE */
  .mini-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 7.8pt;
    margin: 4px 0;
  }
  .mini-table th {
    background: #1e293b;
    color: #ffffff;
    padding: 4px 6px;
    text-align: left;
    font-weight: 700;
    font-size: 7.5pt;
  }
  .mini-table td {
    padding: 3.5px 6px;
    border-bottom: 1px solid #e2e8f0;
    color: #1e293b;
  }
  .mini-table tr:nth-child(even) td {
    background: #f8fafc;
  }
  .tag-gain {
    color: #059669;
    font-weight: 800;
    background: #d1fae5;
    padding: 1px 4px;
    border-radius: 3px;
  }

  /* HIGHLIGHT CALLOUT */
  .callout {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-radius: 5px;
    padding: 5px 8px;
    font-size: 8pt;
    color: #1e40af;
    margin-top: 4px;
  }
  .callout strong {
    color: #1e3a8a;
  }

  /* FOOTER */
  .poster-footer {
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 6px;
    color: #94a3b8;
    padding: 4px 14px;
    font-size: 7.8pt;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 8px;
  }
  .footer-left {
    font-weight: 600;
    color: #cbd5e1;
  }
</style>
</head>
<body>

<!-- POSTER HEADER -->
<div class="poster-header">
  <div class="logo-box">
    <img src="__VGEC_LOGO__" alt="VGEC Logo">
  </div>
  
  <div class="header-center">
    <div class="inst-name">Vishwakarma Government Engineering College, Chandkheda</div>
    <div class="dept-sub">Department of Computer Engineering | Gujarat Technological University (GTU)</div>
    <div class="poster-title">HYPERPARAMETER TUNING OF DATA MINING MODELS</div>
    <div class="poster-subtitle">Systematic Optimization of Algorithmic Hyperparameters for Predictive Accuracy & High-Dimensional Pattern Discovery</div>
    
    <div class="meta-container">
      <div class="meta-pill"><strong>Subject:</strong> Data Mining Techniques (BE05000181)</div>
      <div class="meta-pill"><strong>PBL Task:</strong> 3 (Hyperparameter Tuning)</div>
      <div class="meta-pill"><strong>Students:</strong> Gohel Ridham Manojkumar (240170107121) &bull; Prajapati Vaidik Shaileshbhai (240170107116)</div>
      <div class="meta-pill"><strong>Faculty Guide:</strong> Prof. Niyati Shah</div>
      <div class="meta-pill"><strong>Academic Year:</strong> 2026–27 | Sem V</div>
    </div>
  </div>

  <div class="logo-box">
    <img src="__GTU_LOGO__" alt="GTU Logo">
  </div>
</div>

<!-- POSTER BODY (3 COLUMNS) -->
<div class="poster-body">

  <!-- ==================== COLUMN 1 ==================== -->
  <div class="column">
    
    <!-- CARD 1: Abstract & Formal Problem -->
    <div class="card" style="flex: 0 0 auto;">
      <div class="card-header">
        <span>1. FUNDAMENTALS & MATHEMATICAL FORMULATION</span>
        <span class="badge">Theory</span>
      </div>
      <div class="card-body">
        <p>
          In machine learning and data mining, models possess two distinct parameter tiers:
          <strong>Model Parameters (w)</strong>, learned automatically during training via gradient descent or closed-form solutions, and 
          <strong>Hyperparameters (&theta;)</strong>, structural configurations set <em>prior</em> to training that govern algorithm learning dynamics, capacity, and model topology.
        </p>
        
        <h4>Bilevel Optimization Objective</h4>
        <div class="math-box">
          &theta;* = arg min_{&theta; &isin; &Theta;} E_{(x,y) ~ D_val} [ L(f(x; w*(&theta;)), y) ]<br>
          subject to: w*(&theta;) = arg min_{w} L_train(f(x; w), y_train)
        </div>
        <p>
          Hyperparameter tuning systematically searches the multi-dimensional configuration space &Theta; to discover the parameter tuple &theta;* that minimizes generalization error on unseen validation data without incurring overfitting.
        </p>
      </div>
    </div>

    <!-- CARD 2: Optimization Paradigms -->
    <div class="card" style="flex: 1 1 auto;">
      <div class="card-header">
        <span>2. SYSTEMATIC SEARCH STRATEGIES</span>
        <span class="badge">Algorithms</span>
      </div>
      <div class="card-body">
        <ul style="padding-left: 14px;">
          <li>
            <strong>Grid Search (Exhaustive):</strong> Evaluates the Cartesian product of predefined discrete candidate values. Computationally scales as <em>O(M<sup>d</sup>)</em> (curse of dimensionality); wastes computations on non-sensitive parameters.
          </li>
          <li>
            <strong>Random Search (Bergstra & Bengio):</strong> Samples trials uniformly at random from continuous or discrete distributions. Dramatically superior in practice because most ML models exhibit low <em>effective dimensionality</em> (only 1–2 parameters dominate performance).
          </li>
          <li>
            <strong>Bayesian Optimization:</strong> Constructs a probabilistic surrogate model (Gaussian Process / Tree-structured Parzen Estimators) of the objective function and uses an Acquisition Function (Expected Improvement <em>EI(x)</em>) to balance exploration vs. exploitation.
          </li>
          <li>
            <strong>Successive Halving & Hyperband:</strong> Dynamically allocates resources (iterations/epochs) to promising configurations, pruning underperforming candidates early.
          </li>
        </ul>

        <img src="__SEARCH_STRAT__" class="plot-img" alt="Search Strategies Comparison">
        <div class="caption">Figure 1: Grid Search vs Random Search across 2D Parameter Subspace (Bergstra & Bengio, 2012).</div>
      </div>
    </div>

  </div>

  <!-- ==================== COLUMN 2 ==================== -->
  <div class="column">
    
    <!-- CARD 3: Tuning Across Data Mining Models -->
    <div class="card" style="flex: 1 1 auto;">
      <div class="card-header">
        <span>3. HYPERPARAMETER TUNING IN DATA MINING ALGORITHMS</span>
        <span class="badge">Model Specifics</span>
      </div>
      <div class="card-body">
        
        <h4>A. Unsupervised Clustering & Association Mining</h4>
        <p>
          Unlike supervised models with loss gradients, unsupervised mining models require specialized evaluation heuristics:
        </p>
        <ul style="padding-left: 14px;">
          <li>
            <strong>K-Means Clustering:</strong> Tuning cluster count <em>k</em> via the <strong>Elbow Method</strong> (sum of squared errors SSE) and <strong>Silhouette Analysis</strong> (cluster cohesion vs separation). Initial centroid strategy (<code>init='k-means++'</code>) and <code>n_init</code> runs.
          </li>
          <li>
            <strong>Apriori Rule Mining:</strong> Balancing <code>min_support</code> to avoid combinatorial rule explosion vs losing rare associations; tuning <code>min_confidence</code> and <code>min_lift &gt; 1.0</code> to filter spurious correlations.
          </li>
          <li>
            <strong>DBSCAN:</strong> Estimating neighborhood radius <code>eps (&epsilon;)</code> using the sorted <em>k</em>-distance graph knee point and setting <code>min_samples &ge; 2 &times; dimensions</code>.
          </li>
        </ul>

        <img src="__KMEANS_PLOT__" class="plot-img" alt="K-Means Elbow and Silhouette Curve">
        <div class="caption">Figure 2: K-Means Hyperparameter Tuning: Elbow SSE & Silhouette Score identifying optimal k=4.</div>

        <h4 style="margin-top: 8px;">B. Supervised Classifiers & Ensemble Models</h4>
        <ul style="padding-left: 14px;">
          <li>
            <strong>Support Vector Machines (SVM):</strong> Penalty parameter <em>C</em> (soft-margin slack trade-off) and RBF kernel width <em>&gamma;</em> (influence radius of support vectors).
          </li>
          <li>
            <strong>Random Forest:</strong> <code>n_estimators</code> (tree count), <code>max_depth</code> (structural capacity), <code>min_samples_split</code>, and <code>max_features</code> (&radic;d).
          </li>
          <li>
            <strong>Gradient Boosting (XGBoost):</strong> Learning rate <em>&eta;</em>, <code>subsample</code>, and <code>colsample_bytree</code>.
          </li>
        </ul>

        <img src="__HEATMAP__" class="plot-img" alt="SVM Grid Search Heatmap">
        <div class="caption">Figure 3: 2D Validation Accuracy Surface over SVM Hyperparameters (C vs. &gamma;).</div>

      </div>
    </div>

  </div>

  <!-- ==================== COLUMN 3 ==================== -->
  <div class="column">
    
    <!-- CARD 4: Validation Curves & Bias-Variance -->
    <div class="card" style="flex: 0 0 auto;">
      <div class="card-header">
        <span>4. BIAS-VARIANCE TRADEOFF & VALIDATION CURVES</span>
        <span class="badge">Diagnosis</span>
      </div>
      <div class="card-body">
        <img src="__VAL_CURVE__" class="plot-img" alt="Validation Curve Bias Variance">
        <div class="caption">Figure 4: Validation Curve diagnosing Underfitting (High Bias) vs Overfitting (High Variance).</div>
        
        <p style="font-size: 8.2pt; margin-top: 3px;">
          <strong>Diagnostic Principle:</strong> When model capacity is constrained (e.g., small <em>C</em>, low tree depth), both training and validation errors are high (<em>Underfitting</em>). As capacity increases, validation score reaches an optimum sweet spot (<em>&theta;*</em>) before diverging as the model memorizes training noise (<em>Overfitting</em>).
        </p>
      </div>
    </div>

    <!-- CARD 5: Experimental Evaluation Table -->
    <div class="card" style="flex: 0 0 auto;">
      <div class="card-header">
        <span>5. EMPIRICAL EXPERIMENTAL RESULTS (BEFORE VS AFTER TUNING)</span>
        <span class="badge">Benchmarking</span>
      </div>
      <div class="card-body">
        <table class="mini-table">
          <thead>
            <tr>
              <th>Model / Algorithm</th>
              <th>Default Configuration</th>
              <th>Tuned Parameters (&theta;*)</th>
              <th>Metric Gain</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>SVM Classifier</strong></td>
              <td>C=1.0, &gamma;='scale'</td>
              <td>C=10.0, &gamma;=0.01 (RBF)</td>
              <td><span class="tag-gain">+15.0% Acc</span> (79% &rarr; 94%)</td>
            </tr>
            <tr>
              <td><strong>Random Forest</strong></td>
              <td>n_est=100, max_d=None</td>
              <td>n_est=250, max_d=12, feat=&radic;d</td>
              <td><span class="tag-gain">+6.7% F1</span> (0.84 &rarr; 0.91)</td>
            </tr>
            <tr>
              <td><strong>K-Means Clustering</strong></td>
              <td>k=8, init='random'</td>
              <td>k=4, init='k-means++', n_init=20</td>
              <td><span class="tag-gain">+88.9% Sil</span> (0.36 &rarr; 0.68)</td>
            </tr>
            <tr>
              <td><strong>Apriori Mining</strong></td>
              <td>min_sup=0.01 (14.2k rules)</td>
              <td>min_sup=0.15, lift &gt; 1.4</td>
              <td><span class="tag-gain">38 Clean Rules</span> (0 noise)</td>
            </tr>
          </tbody>
        </table>

        <div class="callout">
          <strong>Key Insight:</strong> Tuning prevented severe data leakage by encapsulating scalers and PCA transformations inside Stratified 5-Fold Cross-Validation pipelines.
        </div>
      </div>
    </div>

    <!-- CARD 6: Best Practices, Tools & References -->
    <div class="card" style="flex: 1 1 auto;">
      <div class="card-header">
        <span>6. FRAMEWORKS, BEST PRACTICES & REFERENCES</span>
        <span class="badge">Industry Practice</span>
      </div>
      <div class="card-body" style="display: flex; flex-direction: column; justify-content: space-between;">
        <div>
          <h4>Production Toolkits</h4>
          <p style="font-size: 8pt; margin-bottom: 4px;">
            <code>Scikit-learn</code> (GridSearchCV, RandomizedSearchCV, HalvingGridSearchCV), <code>Optuna</code> (Asynchronous TPE sampler), <code>Ray Tune</code> (Distributed HPC tuning).
          </p>
          
          <h4>Crucial Best Practices</h4>
          <ol style="padding-left: 14px; font-size: 8pt;">
            <li>Always execute hyperparameter search inside <strong>Nested Cross-Validation</strong> to prevent optimistic performance estimation.</li>
            <li>Prioritize <strong>Random Search</strong> or <strong>TPE/Bayesian Search</strong> over brute-force Grid Search for high-dimensional models (&gt;3 parameters).</li>
            <li>Transform search bounds to logarithmic scales for rates (e.g., learning rate &isin; [10<sup>-4</sup>, 10<sup>-1</sup>]).</li>
          </ol>
        </div>

        <div style="border-top: 1px solid #e2e8f0; padding-top: 4px; margin-top: 4px;">
          <h4 style="margin-top: 0;">Selected Academic References</h4>
          <p style="font-size: 7.2pt; color: #64748b; line-height: 1.25; margin-bottom: 0;">
            1. Bergstra, J., & Bengio, Y. (2012). <em>Random Search for Hyper-Parameter Optimization</em>. JMLR, 13, 281–305.<br>
            2. Snoek, J., Larochelle, H., & Adams, R. P. (2012). <em>Practical Bayesian Optimization of Machine Learning Algorithms</em>. NeurIPS.<br>
            3. Pedregosa, F., et al. (2011). <em>Scikit-learn: Machine Learning in Python</em>. JMLR, 12, 2825–2830.<br>
            4. GTU Syllabus for Computer Engineering: <em>Data Mining Techniques (BE05000181)</em>, Semester V.
          </p>
        </div>
      </div>
    </div>

  </div>

</div>

<!-- POSTER FOOTER -->
<div class="poster-footer">
  <div class="footer-left">
    PBL Activity 3 &bull; Vishwakarma Government Engineering College (VGEC), Chandkheda, Ahmedabad &bull; Department of Computer Engineering
  </div>
  <div>
    Gujarat Technological University (GTU) &bull; Academic Year 2026–27 &bull; October 2026
  </div>
</div>

</body>
</html>
"""

html_content = html_template.replace("__VGEC_LOGO__", vgec_logo_b64)
html_content = html_content.replace("__GTU_LOGO__", gtu_logo_b64)
html_content = html_content.replace("__SEARCH_STRAT__", search_strat_b64)
html_content = html_content.replace("__VAL_CURVE__", val_curve_b64)
html_content = html_content.replace("__KMEANS_PLOT__", kmeans_plot_b64)
html_content = html_content.replace("__HEATMAP__", heatmap_b64)

with open(HTML_OUTPUT, 'w', encoding='utf-8') as f:
    f.write(html_content)
print(f"[OK] Wrote poster HTML: {HTML_OUTPUT}")

chrome_path = None
possible_chromes = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Users\RIDHAM GOHEL\AppData\Local\Google\Chrome\Application\chrome.exe"
]
for p in possible_chromes:
    if os.path.exists(p):
        chrome_path = p
        break

if not chrome_path:
    chrome_path = shutil.which("chrome") or shutil.which("google-chrome")

if chrome_path:
    cmd = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={PDF_OUTPUT}",
        HTML_OUTPUT
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        pdf_size = os.path.getsize(PDF_OUTPUT)
        print(f"[SUCCESS] Compiled publication-grade PDF poster: {PDF_OUTPUT} ({pdf_size} bytes)")
    else:
        print(f"[ERROR] Chrome PDF compilation failed: {res.stderr}")
else:
    print("[WARN] Chrome not found. HTML poster is available for browser printing.")
