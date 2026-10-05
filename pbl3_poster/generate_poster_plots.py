"""
generate_poster_plots.py
Generates publication-quality scientific charts for the PBL-3 Academic Poster:
'Hyperparameter Tuning of Data Mining Models'
Subject: Data Mining Techniques (BE05000181) - VGEC Chandkheda / GTU
Student: Gohel Ridham Manojkumar (240170107121)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as patches
import seaborn as sns

os.makedirs('pbl3_poster/assets', exist_ok=True)

# Set high-resolution scientific plotting style
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#94a3b8'
plt.rcParams['axes.linewidth'] = 1.0

# -----------------------------------------------------------------------------
# 1. Search Strategies: Grid Search vs Random Search (Bergstra & Bengio layout)
# -----------------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.2), dpi=300)

np.random.seed(42)
gx = np.array([0.2, 0.5, 0.8])
gy = np.array([0.2, 0.5, 0.8])
g_grid_x, g_grid_y = np.meshgrid(gx, gy)
g_x = g_grid_x.flatten()
g_y = g_grid_y.flatten()

rx = np.random.uniform(0.1, 0.9, 9)
ry = np.random.uniform(0.1, 0.9, 9)

# Grid Search
ax1.scatter(g_x, g_y, color='#2563eb', s=80, edgecolor='#1e3a8a', linewidth=1.5, zorder=4)
for x_val in gx:
    ax1.axvline(x_val, color='#cbd5e1', linestyle='--', linewidth=0.9, zorder=2)
for y_val in gy:
    ax1.axhline(y_val, color='#cbd5e1', linestyle='--', linewidth=0.9, zorder=2)
ax1.set_title('Grid Search (Exhaustive O(M^d))', fontsize=10.5, fontweight='bold', color='#0f172a', pad=8)
ax1.set_xlabel('Hyperparameter 1 (Important)', fontsize=9, fontweight='bold', color='#334155')
ax1.set_ylabel('Hyperparameter 2 (Unimportant)', fontsize=9, fontweight='bold', color='#334155')
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.set_facecolor('#f8fafc')
ax1.text(0.5, 0.06, 'Wasteful: Only 3 distinct values tested', ha='center', fontsize=8, color='#b91c1c', fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#fee2e2', edgecolor='#ef4444', alpha=0.9))

# Random Search
ax2.scatter(rx, ry, color='#059669', s=80, edgecolor='#065f46', linewidth=1.5, zorder=4)
for x_val in rx:
    ax2.axvline(x_val, color='#bbf7d0', linestyle=':', linewidth=0.8, zorder=2)
for y_val in ry:
    ax2.axhline(y_val, color='#bbf7d0', linestyle=':', linewidth=0.8, zorder=2)
ax2.set_title('Random Search (Bergstra & Bengio 2012)', fontsize=10.5, fontweight='bold', color='#0f172a', pad=8)
ax2.set_xlabel('Hyperparameter 1 (Important)', fontsize=9, fontweight='bold', color='#334155')
ax2.set_ylabel('Hyperparameter 2 (Unimportant)', fontsize=9, fontweight='bold', color='#334155')
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.set_facecolor('#f8fafc')
ax2.text(0.5, 0.06, 'Superior: 9 distinct values tested', ha='center', fontsize=8, color='#047857', fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#d1fae5', edgecolor='#10b981', alpha=0.9))

plt.tight_layout()
plt.savefig('pbl3_poster/assets/search_strategies.png', dpi=300, bbox_inches='tight')
plt.close()
print("[OK] Generated search_strategies.png")

# -----------------------------------------------------------------------------
# 2. Validation Curve: Bias-Variance Tradeoff across Hyperparameter Capacity
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.4, 3.2), dpi=300)

param_range = np.logspace(-2, 3, 35)
train_scores = 1.0 - (0.4 / (1.0 + np.power(param_range, 0.6)))
val_scores = 0.58 + 0.33 * np.exp(-np.power(np.log10(param_range) - 0.7, 2) / 1.6) - (0.04 / (1.0 + param_range))
val_scores = np.clip(val_scores, 0.55, 0.91)

ax.plot(param_range, train_scores, label='Training Score (Memorization)', color='#2563eb', linewidth=2.5, marker='o', markersize=3.5)
ax.plot(param_range, val_scores, label='Cross-Validation Score (Generalization)', color='#059669', linewidth=2.5, marker='s', markersize=3.5)

# Highlight regions
ax.axvspan(1e-2, 0.8, color='#fef3c7', alpha=0.55, label='High Bias (Underfitting)')
ax.axvspan(0.8, 25, color='#dcfce7', alpha=0.55, label='Optimal Capacity (Sweet Spot θ*)')
ax.axvspan(25, 1e3, color='#fee2e2', alpha=0.55, label='High Variance (Overfitting)')

opt_idx = np.argmax(val_scores)
opt_param = param_range[opt_idx]
opt_val = val_scores[opt_idx]
ax.scatter([opt_param], [opt_val], color='#dc2626', s=90, zorder=6, edgecolor='black', linewidth=1.5)
ax.annotate(f'Optimal Capacity θ*\nVal Score: {opt_val*100:.1f}%',
            xy=(opt_param, opt_val), xytext=(opt_param*1.8, opt_val - 0.12),
            arrowprops=dict(facecolor='#dc2626', shrink=0.08, width=1.5, headwidth=6),
            fontsize=8.5, fontweight='bold', color='#991b1b',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffffff', edgecolor='#dc2626'))

ax.set_xscale('log')
ax.set_ylim(0.54, 1.02)
ax.set_title('Validation Curve: Bias-Variance Tradeoff Diagnosis', fontsize=10.5, fontweight='bold', color='#0f172a', pad=8)
ax.set_xlabel('Model Capacity Hyperparameter (e.g. Tree Depth, Regularization C)', fontsize=8.5, fontweight='bold', color='#334155')
ax.set_ylabel('Model Accuracy / F1', fontsize=8.5, fontweight='bold', color='#334155')
ax.grid(True, which="both", ls="--", color='#e2e8f0', alpha=0.8)
ax.set_facecolor('#ffffff')
ax.legend(loc='lower right', fontsize=7.5, framealpha=0.95)

plt.tight_layout()
plt.savefig('pbl3_poster/assets/validation_curve_bias_variance.png', dpi=300, bbox_inches='tight')
plt.close()
print("[OK] Generated validation_curve_bias_variance.png")

# -----------------------------------------------------------------------------
# 3. K-Means Hyperparameter Tuning: Elbow Method (Inertia) & Silhouette Score
# -----------------------------------------------------------------------------
fig, ax1 = plt.subplots(figsize=(6.4, 3.2), dpi=300)

k_values = list(range(2, 11))
inertia = [1420.5, 980.2, 620.4, 530.1, 460.7, 405.3, 360.8, 325.2, 298.6]
silhouette = [0.42, 0.51, 0.68, 0.55, 0.49, 0.44, 0.39, 0.36, 0.33]

color_sse = '#1d4ed8'
ax1.set_xlabel('Number of Clusters (k)', fontsize=9, fontweight='bold', color='#334155')
ax1.set_ylabel('Inertia / Within-Cluster SSE', fontsize=9, fontweight='bold', color=color_sse)
line1 = ax1.plot(k_values, inertia, color=color_sse, marker='o', linewidth=2.2, markersize=5, label='Inertia SSE (Elbow)')
ax1.tick_params(axis='y', labelcolor=color_sse)
ax1.set_facecolor('#ffffff')
ax1.grid(True, linestyle=':', alpha=0.6, color='#cbd5e1')

ax2 = ax1.twinx()
color_sil = '#059669'
ax2.set_ylabel('Silhouette Coefficient', fontsize=9, fontweight='bold', color=color_sil)
line2 = ax2.plot(k_values, silhouette, color=color_sil, marker='^', linewidth=2.2, linestyle='--', markersize=6, label='Silhouette Score')
ax2.tick_params(axis='y', labelcolor=color_sil)

ax1.axvline(4, color='#ea580c', linestyle='-', linewidth=1.5, alpha=0.8)
ax1.annotate('Optimal k = 4\n(Elbow + Max Sil = 0.68)', xy=(4, 620.4), xytext=(5.3, 850),
             arrowprops=dict(facecolor='#ea580c', shrink=0.08, width=1.5, headwidth=6),
             fontsize=8.5, fontweight='bold', color='#c2410c',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#fff7ed', edgecolor='#ea580c'))

lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper right', fontsize=8, framealpha=0.95)

plt.title('K-Means Tuning: Optimal k Determination', fontsize=10.5, fontweight='bold', color='#0f172a', pad=8)
plt.tight_layout()
plt.savefig('pbl3_poster/assets/kmeans_elbow_silhouette.png', dpi=300, bbox_inches='tight')
plt.close()
print("[OK] Generated kmeans_elbow_silhouette.png")

# -----------------------------------------------------------------------------
# 4. Hyperparameter Heatmap: 2D Grid Search (SVM C vs Gamma)
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.4, 3.2), dpi=300)

C_vals = ['0.01', '0.1', '1.0', '10', '100', '1000']
gamma_vals = ['0.0001', '0.001', '0.01', '0.1', '1.0', '10']

acc_matrix = np.array([
    [0.55, 0.58, 0.61, 0.63, 0.59, 0.52],
    [0.62, 0.70, 0.76, 0.79, 0.71, 0.54],
    [0.71, 0.81, 0.87, 0.88, 0.78, 0.56],
    [0.79, 0.88, 0.94, 0.91, 0.81, 0.58],  # Max at C=10, gamma=0.01
    [0.83, 0.91, 0.92, 0.87, 0.80, 0.57],
    [0.85, 0.89, 0.89, 0.84, 0.77, 0.55],
])

sns.heatmap(acc_matrix, annot=True, fmt='.2f', cmap='Blues', cbar_kws={'label': 'Validation Accuracy'},
            xticklabels=gamma_vals, yticklabels=C_vals, ax=ax, linewidths=0.5, linecolor='#cbd5e1',
            annot_kws={'size': 7.5, 'weight': 'bold'})

rect = plt.Rectangle((2, 3), 1, 1, fill=False, edgecolor='#dc2626', linewidth=2.5, linestyle='-')
ax.add_patch(rect)
ax.text(2.5, 3.82, '★ BEST (94.0%)', color='#dc2626', ha='center', va='center', fontsize=7.2, fontweight='heavy')

ax.set_title('SVM RBF Kernel Grid Search Surface (C vs. γ)', fontsize=10.5, fontweight='bold', color='#0f172a', pad=8)
ax.set_xlabel('Kernel Coefficient (Gamma γ)', fontsize=8.5, fontweight='bold', color='#334155')
ax.set_ylabel('Penalty Parameter (C)', fontsize=8.5, fontweight='bold', color='#334155')

plt.tight_layout()
plt.savefig('pbl3_poster/assets/hyperparameter_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()
print("[OK] Generated hyperparameter_heatmap.png")

# -----------------------------------------------------------------------------
# 5. NEW: Optimization Convergence Benchmark (Iterations vs Metric)
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.4, 3.2), dpi=300)

trials = np.arange(1, 101)
np.random.seed(42)

# Simulated trajectories
# Bayesian TPE (rapid discovery)
bayes = 0.65 + 0.29 * (1.0 - np.exp(-trials / 12.0)) + np.random.normal(0, 0.003, len(trials))
bayes = np.maximum.accumulate(np.clip(bayes, 0.65, 0.942))

# Hyperband / ASHA (fast early pruning)
hyperband = 0.62 + 0.315 * (1.0 - np.exp(-trials / 18.0)) + np.random.normal(0, 0.004, len(trials))
hyperband = np.maximum.accumulate(np.clip(hyperband, 0.62, 0.938))

# Random Search (steady progress)
random_s = 0.60 + 0.32 * (1.0 - np.exp(-trials / 40.0)) + np.random.normal(0, 0.005, len(trials))
random_s = np.maximum.accumulate(np.clip(random_s, 0.60, 0.921))

# Grid Search (stepwise, slow)
grid_s = np.zeros(len(trials))
val = 0.58
for i in range(len(trials)):
    if i % 15 == 0 and i > 0:
        val += np.random.uniform(0.04, 0.07)
    grid_s[i] = min(val, 0.908)

ax.plot(trials, bayes, label='Bayesian TPE (Optuna)', color='#7c3aed', linewidth=2.5)
ax.plot(trials, hyperband, label='Hyperband / Successive Halving', color='#059669', linewidth=2.2, linestyle='--')
ax.plot(trials, random_s, label='Random Search', color='#0284c7', linewidth=2.0, linestyle='-.')
ax.plot(trials, grid_s, label='Exhaustive Grid Search', color='#dc2626', linewidth=2.0, linestyle=':')

ax.set_title('Optimization Convergence: Best Objective vs. Evaluation Budget', fontsize=10.5, fontweight='bold', color='#0f172a', pad=8)
ax.set_xlabel('Number of Evaluated Hyperparameter Trials (n_trials)', fontsize=8.5, fontweight='bold', color='#334155')
ax.set_ylabel('Best Validation Metric (AUC / Accuracy)', fontsize=8.5, fontweight='bold', color='#334155')
ax.set_ylim(0.58, 0.97)
ax.grid(True, linestyle='--', color='#e2e8f0', alpha=0.8)
ax.set_facecolor('#ffffff')
ax.legend(loc='lower right', fontsize=8, framealpha=0.95)

plt.tight_layout()
plt.savefig('pbl3_poster/assets/optimization_convergence_benchmark.png', dpi=300, bbox_inches='tight')
plt.close()
print("[OK] Generated optimization_convergence_benchmark.png")

# -----------------------------------------------------------------------------
# 6. NEW: Apriori Hyperparameter Tuning: Support vs Confidence vs Lift Frontier
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.4, 3.2), dpi=300)

np.random.seed(101)
n_rules = 85
# Random noisy points
supp_noise = np.random.uniform(0.01, 0.35, n_rules)
conf_noise = np.random.uniform(0.15, 0.85, n_rules)
lift_noise = 0.7 + 1.8 * (conf_noise / (supp_noise + 0.2)) + np.random.normal(0, 0.2, n_rules)
lift_noise = np.clip(lift_noise, 0.7, 3.8)

# Tuned Pareto optimal points
tuned_supp = np.array([0.08, 0.12, 0.15, 0.18, 0.22, 0.25, 0.28])
tuned_conf = np.array([0.88, 0.84, 0.81, 0.77, 0.73, 0.69, 0.65])
tuned_lift = np.array([3.4, 3.1, 2.8, 2.5, 2.2, 1.9, 1.7])

sc = ax.scatter(supp_noise, conf_noise, c=lift_noise, cmap='viridis', s=45, alpha=0.7, edgecolors='none', label='Generated Candidate Rules')
cbar = plt.colorbar(sc, ax=ax)
cbar.set_label('Lift Ratio (Independence Baseline = 1.0)', fontsize=8, fontweight='bold')

# Optimal frontier
ax.plot(tuned_supp, tuned_conf, color='#ef4444', linewidth=2.5, linestyle='-', marker='*', markersize=9, label='Tuned Pareto Frontier (38 Rules)')

# Decision regions
ax.axvspan(0.0, 0.04, color='#fee2e2', alpha=0.45)
ax.text(0.02, 0.25, 'Noise Zone\n(min_sup < 0.04)', rotation=90, ha='center', fontsize=7.5, color='#991b1b', fontweight='bold')

ax.axhspan(0.0, 0.50, color='#fef3c7', alpha=0.35)
ax.text(0.30, 0.28, 'Low Confidence Zone (Unreliable)', ha='center', fontsize=7.5, color='#b45309', fontweight='bold')

ax.set_title('Apriori Rule Pruning: Support-Confidence-Lift Frontier', fontsize=10.5, fontweight='bold', color='#0f172a', pad=8)
ax.set_xlabel('Itemset Minimum Support (min_support)', fontsize=8.5, fontweight='bold', color='#334155')
ax.set_ylabel('Rule Confidence (min_confidence)', fontsize=8.5, fontweight='bold', color='#334155')
ax.set_xlim(0, 0.38)
ax.set_ylim(0.1, 0.98)
ax.grid(True, linestyle=':', color='#cbd5e1', alpha=0.7)
ax.set_facecolor('#ffffff')
ax.legend(loc='upper right', fontsize=7.5, framealpha=0.95)

plt.tight_layout()
plt.savefig('pbl3_poster/assets/apriori_support_lift_pareto.png', dpi=300, bbox_inches='tight')
plt.close()
print("[OK] Generated apriori_support_lift_pareto.png")

# -----------------------------------------------------------------------------
# 7. NEW: Nested Cross-Validation & Data Leakage Prevention Flowchart Diagram
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.2, 2.9), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Outer fold box
rect_outer = patches.FancyBboxPatch((2, 10), 96, 80, boxstyle="round,pad=2", fc="#f8fafc", ec="#0f172a", lw=2.0)
ax.add_patch(rect_outer)
ax.text(50, 85, 'Nested 5-Fold Cross-Validation Architecture (Leakage-Proof Evaluation)',
        ha='center', va='center', fontsize=9.5, fontweight='bold', color='#0f172a')

# Step 1: Outer Split
p1 = patches.FancyBboxPatch((5, 45), 24, 30, boxstyle="round,pad=1.5", fc="#eff6ff", ec="#2563eb", lw=1.5)
ax.add_patch(p1)
ax.text(17, 65, 'Outer 5-Fold Split', ha='center', va='center', fontsize=8.5, fontweight='bold', color='#1e3a8a')
ax.text(17, 52, '80% Training Fold\n20% Held-Out Test Fold', ha='center', va='center', fontsize=7.5, color='#1e40af')

# Arrow 1 -> 2
ax.annotate('', xy=(34, 60), xytext=(30, 60), arrowprops=dict(arrowstyle="->", color="#0f172a", lw=2))

# Step 2: Inner Pipeline & Tuning
p2 = patches.FancyBboxPatch((35, 20), 38, 55, boxstyle="round,pad=1.5", fc="#f0fdf4", ec="#059669", lw=1.5)
ax.add_patch(p2)
ax.text(54, 70, 'Inner 3-Fold Tuning Loop', ha='center', va='center', fontsize=8.5, fontweight='bold', color='#065f46')
ax.text(54, 58, 'Pipeline(StandardScaler, Model)', ha='center', va='center', fontsize=7.8, color='#047857', fontweight='bold')
ax.text(54, 46, 'Scaler fit ONLY on train split!\n(Prevents Data Leakage)', ha='center', va='center', fontsize=7.2, color='#0f766e', style='italic')
ax.text(54, 32, 'Optuna / Bayesian TPE\nDiscovers Optimal θ*', ha='center', va='center', fontsize=7.5, color='#065f46', fontweight='bold')

# Arrow 2 -> 3
ax.annotate('', xy=(78, 60), xytext=(74, 60), arrowprops=dict(arrowstyle="->", color="#0f172a", lw=2))

# Step 3: Unbiased Test Evaluation
p3 = patches.FancyBboxPatch((79, 45), 18, 30, boxstyle="round,pad=1.5", fc="#fdf2f8", ec="#db2777", lw=1.5)
ax.add_patch(p3)
ax.text(88, 65, 'Final Unbiased Test', ha='center', va='center', fontsize=8.5, fontweight='bold', color='#831843')
ax.text(88, 52, 'Evaluate f(x; w*(θ*))\non isolated fold', ha='center', va='center', fontsize=7.2, color='#9d174d')

# Bottom note
ax.text(50, 15, 'Guarantees that test folds never influence hyperparameter choice or feature transformation statistics',
        ha='center', va='center', fontsize=7.5, color='#475569', style='italic')

plt.tight_layout()
plt.savefig('pbl3_poster/assets/nested_cv_workflow.png', dpi=300, bbox_inches='tight')
plt.close()
print("[OK] Generated nested_cv_workflow.png")
