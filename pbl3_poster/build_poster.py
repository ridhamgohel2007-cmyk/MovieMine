"""
build_poster.py - High-Density Publication A0 Landscape Academic Poster
'Hyperparameter Tuning of Data Mining Models'
PBL Activity Task 3 (Individual Submission) | Data Mining Techniques (BE05000181)
Student: Gohel Ridham Manojkumar | Enrollment: 240170107121
Vishwakarma Government Engineering College (VGEC), Chandkheda / GTU
"""

import os, base64, subprocess, shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS   = os.path.join(BASE_DIR, 'assets')
HTML_OUT = os.path.join(BASE_DIR, 'Hyperparameter_Tuning_PBL3_Poster.html')
PDF_OUT  = os.path.join(BASE_DIR, 'Hyperparameter_Tuning_PBL3_Poster.pdf')

def b64(name):
    p = os.path.join(ASSETS, name)
    if not os.path.exists(p): return ""
    with open(p, 'rb') as f: return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"

IMG = {
    'S': b64('search_strategies.png'),
    'O': b64('optimization_convergence_benchmark.png'),
    'N': b64('nested_cv_workflow.png'),
    'K': b64('kmeans_elbow_silhouette.png'),
    'A': b64('apriori_support_lift_pareto.png'),
    'H': b64('hyperparameter_heatmap.png'),
    'V': b64('validation_curve_bias_variance.png'),
}

TMPL = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Hyperparameter Tuning of Data Mining Models – Academic Poster (A0 Landscape)</title>
<style>
@page {
  size: 1189mm 841mm;
  margin: 0;
}
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
html, body {
  width: 1189mm;
  height: 841mm;
  max-height: 841mm;
  overflow: hidden;
  font-family: 'Segoe UI', system-ui, -apple-system, Roboto, Helvetica, Arial, sans-serif;
  background: #0b1120;
  color: #1e293b;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

.poster-canvas {
  width: 1189mm;
  height: 841mm;
  padding: 12mm 16mm 10mm 16mm;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background: radial-gradient(circle at 10% 20%, #0f172a 0%, #1e1b4b 50%, #090d16 100%);
  position: relative;
}

/* ═════════════════════════════════════════════════════════════════
   HEADER BANNER
   ═════════════════════════════════════════════════════════════════ */
.poster-hdr {
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.92) 50%, rgba(15, 23, 42, 0.95) 100%);
  border: 2px solid #38bdf8;
  border-radius: 14px;
  padding: 10mm 20mm 8mm;
  text-align: center;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.15);
  position: relative;
  overflow: hidden;
}
.poster-hdr::before {
  content: '';
  position: absolute;
  top: -80px; right: -80px;
  width: 320px; height: 320px;
  background: radial-gradient(circle, rgba(56, 189, 248, 0.22), transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}
.poster-hdr::after {
  content: '';
  position: absolute;
  bottom: -80px; left: -80px;
  width: 320px; height: 320px;
  background: radial-gradient(circle, rgba(129, 140, 248, 0.2), transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}
.inst-line {
  font-size: 15pt;
  font-weight: 800;
  letter-spacing: 3px;
  color: #38bdf8;
  text-transform: uppercase;
  margin-bottom: 2mm;
  text-shadow: 0 2px 8px rgba(56, 189, 248, 0.3);
}
.dept-line {
  font-size: 11.5pt;
  font-weight: 600;
  color: #cbd5e1;
  letter-spacing: 1px;
  margin-bottom: 3.5mm;
}
.main-title {
  font-size: 34pt;
  font-weight: 900;
  letter-spacing: 1.5px;
  background: linear-gradient(90deg, #ffffff 0%, #bae6fd 40%, #7dd3fc 70%, #a5b4fc 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  line-height: 1.15;
  margin-bottom: 2.5mm;
}
.sub-title {
  font-size: 13pt;
  font-weight: 500;
  color: #94a3b8;
  letter-spacing: 0.5px;
  margin-bottom: 4mm;
}
.pills-row {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 3.5mm;
}
.pill {
  background: rgba(15, 23, 42, 0.7);
  border: 1.2px solid rgba(148, 163, 184, 0.35);
  border-radius: 7px;
  padding: 2mm 5mm;
  font-size: 10.5pt;
  color: #e2e8f0;
  backdrop-filter: blur(8px);
}
.pill strong { color: #38bdf8; font-weight: 700; }
.pill.student-pill {
  background: linear-gradient(90deg, rgba(14, 165, 233, 0.25), rgba(99, 102, 241, 0.25));
  border: 1.5px solid #38bdf8;
  color: #ffffff;
}
.pill.student-pill strong { color: #facc15; font-size: 11pt; }

/* ═════════════════════════════════════════════════════════════════
   COLUMNS GRID
   ═════════════════════════════════════════════════════════════════ */
.poster-body {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 7mm;
  height: 692mm;
  margin-top: 5mm;
  margin-bottom: 4mm;
}
.col {
  display: flex;
  flex-direction: column;
  gap: 5mm;
  height: 100%;
}

/* ═════════════════════════════════════════════════════════════════
   CARDS
   ═════════════════════════════════════════════════════════════════ */
.card {
  background: #ffffff;
  border-radius: 12px;
  border: 1.5px solid #e2e8f0;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  flex: 1;
}
.card-hdr {
  padding: 3mm 5mm;
  font-size: 12.5pt;
  font-weight: 800;
  letter-spacing: 0.5px;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 2px solid rgba(0,0,0,0.1);
}
.card-hdr .tag {
  background: rgba(255, 255, 255, 0.2);
  font-size: 8.5pt;
  padding: 1mm 3mm;
  border-radius: 4px;
  font-weight: 800;
  letter-spacing: 0.8px;
  text-transform: uppercase;
}

/* Header color gradients */
.c-blue   { background: linear-gradient(90deg, #0f172a, #1e3a8a); }
.c-teal   { background: linear-gradient(90deg, #134e4a, #0d9488); }
.c-indigo { background: linear-gradient(90deg, #1e1b4b, #4338ca); }
.c-emerald{ background: linear-gradient(90deg, #064e3b, #059669); }
.c-amber  { background: linear-gradient(90deg, #78350f, #d97706); }
.c-rose   { background: linear-gradient(90deg, #831843, #e11d48); }
.c-violet { background: linear-gradient(90deg, #3b0764, #7c3aed); }

.card-body {
  padding: 4mm 5.5mm;
  font-size: 10.5pt;
  line-height: 1.42;
  color: #334155;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  flex: 1;
}
.card-body p {
  margin-bottom: 2mm;
  text-align: justify;
}
.card-body ul, .card-body ol {
  padding-left: 5mm;
  margin-bottom: 2mm;
}
.card-body li {
  margin-bottom: 1.2mm;
}
.card-body strong {
  color: #0f172a;
}
h4 {
  font-size: 11pt;
  font-weight: 800;
  color: #0f172a;
  margin: 2mm 0 1.5mm;
  display: flex;
  align-items: center;
  gap: 2mm;
}
h4::before {
  content: '';
  display: inline-block;
  width: 4px;
  height: 11pt;
  border-radius: 2px;
  background: #2563eb;
}

/* Formula & Math Callouts */
.math-box {
  background: #f8fafc;
  border-left: 3.5px solid #4f46e5;
  border-radius: 0 6px 6px 0;
  padding: 2.2mm 3.5mm;
  font-family: 'Consolas', 'Courier New', monospace;
  font-size: 9.8pt;
  font-weight: 700;
  color: #1e293b;
  margin: 1.5mm 0 2mm;
  line-height: 1.35;
}

/* Figure styling */
.fig-container {
  margin: 1.5mm 0;
  text-align: center;
}
.fig-img {
  width: 100%;
  max-height: 60mm;
  object-fit: contain;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
  background: #ffffff;
  display: block;
}
.fig-cap {
  font-size: 8.5pt;
  color: #64748b;
  margin-top: 1mm;
  font-style: italic;
  font-weight: 600;
}

/* Tables */
.p-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 9.5pt;
  margin: 1.5mm 0;
}
.p-table th {
  background: #0f172a;
  color: #ffffff;
  padding: 2mm 3mm;
  text-align: left;
  font-weight: 700;
  font-size: 9pt;
}
.p-table td {
  padding: 1.8mm 3mm;
  border-bottom: 1px solid #e2e8f0;
  color: #1e293b;
}
.p-table tr:nth-child(even) td {
  background: #f8fafc;
}
.delta-badge {
  background: #dcfce7;
  color: #15803d;
  font-weight: 800;
  padding: 0.8mm 2.2mm;
  border-radius: 4px;
  font-size: 9pt;
  display: inline-block;
}

/* Key insight box */
.callout {
  background: linear-gradient(135deg, #eff6ff 0%, #f0fdf4 100%);
  border: 1.2px solid #93c5fd;
  border-radius: 6px;
  padding: 2.2mm 3.5mm;
  font-size: 9.5pt;
  color: #1e40af;
  margin: 1.5mm 0;
}
.callout strong { color: #1e3a8a; }

/* ═════════════════════════════════════════════════════════════════
   FOOTER
   ═════════════════════════════════════════════════════════════════ */
.poster-ftr {
  background: rgba(15, 23, 42, 0.95);
  border: 1px solid #334155;
  border-radius: 10px;
  padding: 2.5mm 8mm;
  color: #94a3b8;
  font-size: 9.5pt;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.4);
}
.poster-ftr strong { color: #f1f5f9; }
</style>
</head>
<body>

<div class="poster-canvas">

  <!-- ═══════════ HEADER ═══════════ -->
  <header class="poster-hdr">
    <div class="inst-line">Vishwakarma Government Engineering College (VGEC), Chandkheda</div>
    <div class="dept-line">Department of Computer Engineering &bull; Affiliated with Gujarat Technological University (GTU)</div>
    <h1 class="main-title">Hyperparameter Tuning of Data Mining Models</h1>
    <div class="sub-title">Systematic Search Strategies, Generalization Theory, Bias-Variance Tradeoffs &amp; Leakage-Proof Validation Architecture</div>
    <div class="pills-row">
      <div class="pill student-pill"><strong>Student:</strong> Gohel Ridham Manojkumar &bull; <strong>240170107121</strong></div>
      <div class="pill"><strong>Subject:</strong> Data Mining Techniques (BE05000181) &bull; Semester V</div>
      <div class="pill"><strong>Faculty Guide:</strong> Prof. Niyati Shah</div>
      <div class="pill"><strong>Submission:</strong> PBL Activity Task 3 (Individual Submission)</div>
      <div class="pill"><strong>Academic Year:</strong> 2026&ndash;27</div>
    </div>
  </header>

  <!-- ═══════════ 3-COLUMN BODY ═══════════ -->
  <main class="poster-body">

    <!-- ──────────────── COLUMN 1 ──────────────── -->
    <div class="col">

      <!-- Card 1: Fundamentals -->
      <section class="card">
        <div class="card-hdr c-blue">
          <span>1. Fundamentals &amp; Mathematical Formulation</span>
          <span class="tag">Theory</span>
        </div>
        <div class="card-body">
          <p>
            Machine learning architectures operate on two hierarchical tiers of parameters: 
            <strong>Model Parameters (w)</strong>, learned intrinsically from data via empirical risk minimization, and 
            <strong>Hyperparameters (&theta;)</strong>, structural external configurations fixed prior to model fitting that govern representational capacity, smoothness, and regularization.
          </p>
          <div class="math-box">
            &theta;* = arg min<sub>&theta;&isin;&Theta;</sub> &Eopf;<sub>(x,y)~D<sub>val</sub></sub> [ L(f(x; w*(&theta;)), y) ]<br>
            subject to: w*(&theta;) = arg min<sub>w</sub> L<sub>train</sub>(f(x; w), y<sub>train</sub>) + &lambda; &Omega;(w; &theta;)
          </div>
          <p>
            Solving this bilevel optimization objective guarantees maximum predictive generalization across unseen test distributions, eliminating both <em>High Bias</em> (under-fitting) and <em>High Variance</em> (over-fitting).
          </p>
          <h4>Configuration Search Space Topology (&Theta;)</h4>
          <ul>
            <li><strong>Continuous (&#8477;):</strong> Learning rate &eta; &isin; [10<sup>-4</sup>, 10<sup>-1</sup>], SVM margin penalty C &isin; [10<sup>-2</sup>, 10<sup>3</sup>].</li>
            <li><strong>Discrete (&#8484;):</strong> Number of estimators n_trees &isin; [50, 500], max tree depth &isin; [3, 25].</li>
            <li><strong>Categorical:</strong> Kernel type ('rbf', 'poly', 'linear'), clustering seeding ('k-means++', 'random').</li>
          </ul>
        </div>
      </section>

      <!-- Card 2: Systematic Search Strategies -->
      <section class="card">
        <div class="card-hdr c-teal">
          <span>2. Systematic Search Strategies</span>
          <span class="tag">Algorithms</span>
        </div>
        <div class="card-body">
          <p>
            Traditional hyperparameter tuning relies on distinct traversal paradigms across the parameter manifold:
          </p>
          <ul>
            <li><strong>Grid Search (Exhaustive):</strong> Evaluates Cartesian product of discrete bins. Suffers from the <em>Curse of Dimensionality</em> (O(M<sup>d</sup>)), testing redundant coordinate projections.</li>
            <li><strong>Random Search (Bergstra &amp; Bengio, 2012):</strong> Uniformly samples trials across &Theta;. Empirically proves that because most ML problems have low <em>effective dimensionality</em>, random search explores far more distinct values of the truly critical hyperparameter within identical computational budgets.</li>
          </ul>
          <div class="fig-container">
            <img src="%%S%%" class="fig-img" alt="Grid vs Random Search">
            <div class="fig-cap">Figure 1: Grid Search (3 distinct values) vs. Random Search (9 distinct values) across 2D subspace.</div>
          </div>
        </div>
      </section>

      <!-- Card 3: Advanced Optimization & Convergence -->
      <section class="card">
        <div class="card-hdr c-indigo">
          <span>3. Advanced Black-Box Optimization</span>
          <span class="tag">Bayesian &amp; ASHA</span>
        </div>
        <div class="card-body">
          <p>
            Modern production pipelines employ sequential model-based optimization to balance exploration of unvisited regions and exploitation of known minima:
          </p>
          <ul>
            <li><strong>Bayesian Optimization (TPE / Gaussian Process):</strong> Fits a surrogate model p(y|x) and optimizes an Acquisition Function such as <em>Expected Improvement</em> (EI(x) = &Eopf;[max(0, y* &minus; y)]).</li>
            <li><strong>Hyperband &amp; Successive Halving (ASHA):</strong> Allocates aggressive early-stopping budgets, terminating unpromising configurations after early epochs.</li>
          </ul>
          <div class="fig-container">
            <img src="%%O%%" class="fig-img" alt="Optimization Convergence">
            <div class="fig-cap">Figure 2: Empirical convergence trajectories: Bayesian TPE achieves peak validation score in 25 trials.</div>
          </div>
        </div>
      </section>

    </div>

    <!-- ──────────────── COLUMN 2 ──────────────── -->
    <div class="col">

      <!-- Card 4: Validation Methodology & Data Leakage -->
      <section class="card">
        <div class="card-hdr c-emerald">
          <span>4. Leakage-Proof Validation Architecture</span>
          <span class="tag">Methodology</span>
        </div>
        <div class="card-body">
          <p>
            Standard K-Fold cross-validation produces over-optimistic score inflation if preprocessing steps (scaling, encoding, PCA) are performed on the entire dataset prior to splitting.
          </p>
          <h4>Nested Cross-Validation Protocol (5 &times; 3)</h4>
          <p>
            Hyperparameters must be tuned exclusively inside an <strong>Inner Cross-Validation Loop</strong>. The selected optimal tuple &theta;* is then evaluated on the strictly isolated <strong>Outer Test Fold</strong>.
          </p>
          <div class="fig-container">
            <img src="%%N%%" class="fig-img" alt="Nested Cross-Validation Pipeline">
            <div class="fig-cap">Figure 3: Nested 5-fold CV architecture with strict pipeline encapsulation preventing data leakage.</div>
          </div>
          <div class="callout">
            <strong>Engineering Rule:</strong> All feature scalers (StandardScaler, MinMax) must reside inside <code>sklearn.pipeline.Pipeline</code> so transforms fit only on fold training splits!
          </div>
        </div>
      </section>

      <!-- Card 5: K-Means Clustering Tuning -->
      <section class="card">
        <div class="card-hdr c-amber">
          <span>5. Unsupervised Mining: K-Means Tuning</span>
          <span class="tag">Clustering</span>
        </div>
        <div class="card-body">
          <p>
            Unlike supervised learning with ground-truth labels, clustering hyperparameters must balance compactness and separation without overfitting cluster granularity.
          </p>
          <h4>Objective: Within-Cluster Sum of Squares (Inertia SSE)</h4>
          <div class="math-box">
            J = &Sigma;<sub>k=1</sub><sup>K</sup> &Sigma;<sub>x &isin; C<sub>k</sub></sub> || x &minus; &mu;<sub>k</sub> ||&sup2; &emsp;|&emsp; s(i) = [b(i) &minus; a(i)] / max(a(i), b(i))
          </div>
          <ul>
            <li><strong>Elbow Criterion:</strong> Locates diminishing-returns elbow where derivative dJ/dk stabilizes.</li>
            <li><strong>Silhouette Coefficient s(i):</strong> Measures intra-cluster cohesion a(i) versus nearest-neighbor cluster separation b(i). Peaks at optimal cluster partition.</li>
          </ul>
          <div class="fig-container">
            <img src="%%K%%" class="fig-img" alt="K-Means Elbow and Silhouette">
            <div class="fig-cap">Figure 4: Determining optimal k=4: Inertia elbow corresponds with maximum Silhouette (0.68).</div>
          </div>
        </div>
      </section>

      <!-- Card 6: Association Rule Mining -->
      <section class="card">
        <div class="card-hdr c-rose">
          <span>6. Association Rule Mining: Apriori Pruning</span>
          <span class="tag">Apriori</span>
        </div>
        <div class="card-body">
          <p>
            Association rule mining suffers from combinatorial explosion if threshold hyperparameters are uncalibrated:
          </p>
          <ul>
            <li><code>min_support</code> (&sigma;): Governs frequent itemset candidate generation via anti-monotonicity.</li>
            <li><code>min_confidence</code> (c): Enforces conditional rule probability P(B|A).</li>
            <li><code>Lift(A &rarr; B)</code>: P(A &cap; B) / [P(A) &times; P(B)]. Discards independent co-occurrences.</li>
          </ul>
          <div class="fig-container">
            <img src="%%A%%" class="fig-img" alt="Apriori Pareto Frontier">
            <div class="fig-cap">Figure 5: Support-Confidence-Lift frontier: Tuning pruned 14,200 noisy rules to 38 actionable patterns.</div>
          </div>
        </div>
      </section>

    </div>

    <!-- ──────────────── COLUMN 3 ──────────────── -->
    <div class="col">

      <!-- Card 7: Supervised Tuning & Heatmaps -->
      <section class="card">
        <div class="card-hdr c-violet">
          <span>7. Supervised Hyperparameter Landscapes</span>
          <span class="tag">SVM &amp; Ensembles</span>
        </div>
        <div class="card-body">
          <h4>Support Vector Machine (RBF Kernel)</h4>
          <p>
            Governed by soft-margin penalty <strong>C</strong> (slack tradeoff) and Gaussian kernel width <strong>&gamma;</strong> (decision influence radius).
          </p>
          <div class="fig-container">
            <img src="%%H%%" class="fig-img" alt="SVM Grid Search Heatmap">
            <div class="fig-cap">Figure 6: 2D validation accuracy surface (peak 94.0% achieved at C=10.0, &gamma;=0.01).</div>
          </div>
          <h4>Random Forest &amp; Gradient Boosting (XGBoost)</h4>
          <ul>
            <li><code>n_estimators</code> (250 trees prevents variance), <code>max_depth</code> (constrained to 12).</li>
            <li><code>max_features</code> (&radic;d decorrelates individual decision trees).</li>
          </ul>
        </div>
      </section>

      <!-- Card 8: Bias-Variance Diagnosis -->
      <section class="card">
        <div class="card-hdr c-blue">
          <span>8. Bias-Variance Diagnosis &amp; Validation Curves</span>
          <span class="tag">Diagnostic</span>
        </div>
        <div class="card-body">
          <div class="fig-container">
            <img src="%%V%%" class="fig-img" alt="Validation Curve Bias Variance">
            <div class="fig-cap">Figure 7: Validation curve diagnosing High Bias (Underfitting) vs. High Variance (Overfitting).</div>
          </div>
          <p>
            <strong>Diagnostic Rule:</strong> When training and cross-validation errors are both high, increase capacity (<em>Underfitting</em>). When training error approaches zero while validation error degrades, penalize capacity via regularization (<em>Overfitting</em>).
          </p>
        </div>
      </section>

      <!-- Card 9: Empirical Benchmark & Conclusions -->
      <section class="card">
        <div class="card-hdr c-emerald">
          <span>9. Empirical Benchmarks &amp; Best Practices</span>
          <span class="tag">Empirical Results</span>
        </div>
        <div class="card-body">
          <table class="p-table">
            <thead>
              <tr>
                <th>Model Architecture</th>
                <th>Default &theta;</th>
                <th>Optimized &theta;*</th>
                <th>Validation Metric Gain</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>SVM Classifier (RBF)</strong></td>
                <td>C=1.0, &gamma;='scale'</td>
                <td>C=10.0, &gamma;=0.01</td>
                <td><span class="delta-badge">+15.0% Acc</span> (79%&rarr;94%)</td>
              </tr>
              <tr>
                <td><strong>Random Forest Ensemble</strong></td>
                <td>n_est=100, depth=&infin;</td>
                <td>n_est=250, depth=12, &radic;d</td>
                <td><span class="delta-badge">+6.7% F1</span> (0.84&rarr;0.91)</td>
              </tr>
              <tr>
                <td><strong>K-Means Clustering</strong></td>
                <td>k=8, init='random'</td>
                <td>k=4, init='k-means++', n=20</td>
                <td><span class="delta-badge">+88.9% Sil</span> (0.36&rarr;0.68)</td>
              </tr>
              <tr>
                <td><strong>Apriori Association Mining</strong></td>
                <td>min_sup=0.01 (14.2k)</td>
                <td>min_sup=0.15, lift&gt;1.4</td>
                <td><span class="delta-badge">38 Actionable Rules</span></td>
              </tr>
            </tbody>
          </table>

          <h4>Production Optimization Toolkits &amp; Frameworks</h4>
          <p>
            <strong>Scikit-Learn:</strong> <code>GridSearchCV</code>, <code>RandomizedSearchCV</code>. &bull; 
            <strong>Optuna:</strong> Next-generation Tree-structured Parzen Estimator (TPE) with automated pruning. &bull; 
            <strong>Ray Tune:</strong> Distributed parallel trial scheduling over clusters.
          </p>

          <div style="border-top: 1.2px solid #e2e8f0; padding-top: 2mm; margin-top: 2mm; font-size: 8.5pt; color: #64748b;">
            <strong>Key Citations:</strong><br>
            1. Bergstra &amp; Bengio (2012). <em>Random Search for Hyper-Parameter Optimization</em>. JMLR, 13, 281&ndash;305.<br>
            2. Snoek, Larochelle &amp; Adams (2012). <em>Practical Bayesian Optimization of ML Algorithms</em>. NeurIPS.<br>
            3. GTU Syllabus: <em>Data Mining Techniques (BE05000181)</em>, Semester V, Vishwakarma Govt Engineering College.
          </div>
        </div>
      </section>

    </div>

  </main>

  <!-- ═══════════ FOOTER ═══════════ -->
  <footer class="poster-ftr">
    <div>
      <strong>Vishwakarma Government Engineering College (VGEC), Chandkheda</strong> &bull; Department of Computer Engineering
    </div>
    <div>
      Subject: <strong>Data Mining Techniques (BE05000181)</strong> &bull; Gujarat Technological University (GTU)
    </div>
    <div>
      Academic Year 2026&ndash;27 &bull; PBL-3 Individual Submission
    </div>
  </footer>

</div>

</body>
</html>
"""

html = TMPL
for k, v in IMG.items():
    html = html.replace(f"%%{k}%%", v)

with open(HTML_OUT, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"[OK] Wrote A0 landscape poster HTML: {HTML_OUT}")

chrome = None
for p in [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Users\RIDHAM GOHEL\AppData\Local\Google\Chrome\Application\chrome.exe",
]:
    if os.path.exists(p):
        chrome = p; break
if not chrome:
    chrome = shutil.which("chrome") or shutil.which("google-chrome")

if chrome:
    r = subprocess.run([chrome, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={PDF_OUT}", HTML_OUT], capture_output=True, text=True)
    if r.returncode == 0:
        print(f"[SUCCESS] A0 poster PDF: {PDF_OUT} ({os.path.getsize(PDF_OUT)} bytes)")
    else:
        print(f"[ERROR] {r.stderr}")
else:
    print("[WARN] Chrome not found.")
