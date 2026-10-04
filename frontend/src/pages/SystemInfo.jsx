import React, { useState } from 'react';
import { 
  BookOpen, Database, Cpu, Layers, Network, 
  ExternalLink, ChevronDown, ChevronUp, CheckCircle, Shield
} from 'lucide-react';

const SystemInfo = () => {
  const [expandedFaq, setExpandedFaq] = useState(0);

  const vivaQuestions = [
    {
      q: 'What is Data Mining?',
      a: 'Data Mining is the computational process of discovering non-trivial, previously unknown, implicit, and potentially useful patterns, correlations, and anomalies within large datasets using techniques at the intersection of artificial intelligence, machine learning, statistics, and database systems.'
    },
    {
      q: 'What is KDD and how does it relate to Data Mining?',
      a: 'KDD stands for Knowledge Discovery in Databases. Data Mining is the central algorithmic step within the broader iterative KDD process. The 5 KDD stages are: 1. Selection (extracting relevant data from tables), 2. Preprocessing (handling missing values and noise), 3. Transformation (normalizing ratings and pivoting into user-movie matrices), 4. Data Mining (applying algorithms like K-Means, Apriori, Collaborative Filtering), and 5. Evaluation & Interpretation (analyzing clusters, rules, and recommendation metrics).'
    },
    {
      q: 'Why did you choose a Relational Database (MySQL) instead of static files?',
      a: 'Real-world data mining applications operate over normalized transaction logs that evolve over time. Using MySQL relational tables (with primary keys, foreign keys, and indexes) ensures ACID compliance, prevents data redundancy via 3NF normalization, supports relational joins between users, ratings, and movies, and enables real-time extraction for dynamic data mining.'
    },
    {
      q: 'Explain Collaborative Filtering vs Content-Based Filtering.',
      a: 'Collaborative Filtering relies solely on past user interactions (ratings/views). It identifies peer users who agreed in the past (User-User k-NN) to recommend items they liked. Content-Based Filtering relies on item attributes (genres, keywords, synopses) vectorized using TF-IDF and computes pairwise Cosine Similarity. Collaborative filtering can discover surprising cross-genre items, while Content-based filtering is immune to cold-start for new items that have metadata but no user ratings.'
    },
    {
      q: 'What is the Cold-Start Problem and how does MovieMine solve it?',
      a: 'Cold-start occurs when a new user has zero ratings (cannot compute user similarities) or a new movie has zero views. MovieMine solves this via a Hybrid Recommendation Model: Hybrid Score = 0.5 * Collab + 0.3 * Content + 0.2 * Popularity. If collaborative signals are missing, the system gracefully falls back to content-based similarity and global IMDb popularity.'
    },
    {
      q: 'Explain the mathematical foundation of K-Means Clustering.',
      a: 'K-Means is an unsupervised partitioning algorithm that clusters N data points into K clusters. It iteratively optimizes the Within-Cluster Sum of Squares (Inertia/WCSS): J = Σ Σ ||x_i - μ_j||^2. It alternates between 1. Assignment step (assigning each user vector to the nearest centroid μ_j via Euclidean distance) and 2. Update step (recalculating μ_j as the mathematical mean of all assigned vectors) until convergence.'
    },
    {
      q: 'In Association Rule Mining, explain Support, Confidence, and Lift.',
      a: 'For a rule A -> B: 1. Support = P(A ∩ B) is the proportion of total transactions containing both items. 2. Confidence = P(B | A) = Support(A∪B) / Support(A) is the conditional probability that a user who watched A also watched B. 3. Lift = Confidence / Support(B) measures how much more frequently A and B occur together than if they were statistically independent. Lift > 1 indicates a genuine positive correlation.'
    },
    {
      q: 'What is Cosine Similarity and why is it preferred over Euclidean distance for text vectors?',
      a: 'Cosine Similarity computes the cosine of the angle between two multi-dimensional vectors: sim(A, B) = (A · B) / (||A|| * ||B||). It evaluates directional orientation rather than vector magnitude. In text mining (TF-IDF), document lengths vary widely; Euclidean distance would penalize long synopses, whereas Cosine Similarity normalizes for length.'
    },
    {
      q: 'Which Kaggle dataset did you use and how was it preprocessed?',
      a: 'We utilized metadata and interactions from The Movies Dataset (by Rounak Banik on Kaggle) and MovieLens Small Latest Dataset. The raw files were parsed through a KDD pipeline: extracting 225 high-density movies across 18 genres, cleaning missing durations and rating anomalies, generating normalized relational tables, and creating sparse User-Movie rating pivot tables.'
    },
    {
      q: 'What is mean-centering in User-Based Collaborative Filtering?',
      a: 'Different users exhibit different rating biases—some are harsh raters (average 2.5) while others are generous (average 4.5). Subtracting each user\'s mean rating: s(u, i) = r(u, i) - mean(r_u) normalizes rating scales so that similarity measures reflect genuine preference deviations rather than baseline rating tendencies.'
    }
  ];

  return (
    <div className="space-y-8 pb-16 text-left">
      {/* Header */}
      <div className="bg-slate-900/90 p-6 sm:p-8 rounded-3xl border border-slate-800 shadow-2xl">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-semibold mb-2 border border-emerald-500/30">
          <BookOpen className="w-3.5 h-3.5" /> Academic Viva & System Documentation
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          System Architecture & Viva Examination Guide
        </h1>
        <p className="text-xs text-slate-400 mt-1 max-w-3xl">
          Comprehensive reference explaining the 5-stage KDD process, relational database schema, data mining mathematical formulations, and anticipated faculty viva questions.
        </p>
      </div>

      {/* Kaggle Provenance Banner */}
      <div className="p-6 rounded-2xl bg-indigo-950/30 border border-indigo-500/20 shadow-xl space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Database className="w-5 h-5 text-indigo-400" />
            <h3 className="text-sm font-bold text-white">Kaggle Dataset Provenance & Attribution</h3>
          </div>
          <span className="text-[10px] font-bold text-indigo-300 bg-indigo-500/20 px-2 py-0.5 rounded border border-indigo-500/30">
            Open Data Attribution
          </span>
        </div>

        <p className="text-xs text-slate-300 leading-relaxed">
          The underlying data for MovieMine is sourced and synthesized from official open-source academic datasets:
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-1">
          <a
            href="https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset"
            target="_blank"
            rel="noreferrer"
            className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-700/60 hover:border-indigo-500 transition-colors flex items-center justify-between text-xs"
          >
            <div>
              <div className="font-semibold text-white">The Movies Dataset (Kaggle)</div>
              <div className="text-[11px] text-slate-400">By Rounak Banik • TMDB & MovieLens Metadata</div>
            </div>
            <ExternalLink className="w-4 h-4 text-indigo-400" />
          </a>

          <a
            href="https://www.kaggle.com/datasets/shubhammehta21/movie-lens-small-latest-dataset"
            target="_blank"
            rel="noreferrer"
            className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-700/60 hover:border-indigo-500 transition-colors flex items-center justify-between text-xs"
          >
            <div>
              <div className="font-semibold text-white">MovieLens Small Latest Dataset (Kaggle)</div>
              <div className="text-[11px] text-slate-400">GroupLens Research • 100k Benchmark Ratings</div>
            </div>
            <ExternalLink className="w-4 h-4 text-indigo-400" />
          </a>
        </div>
      </div>

      {/* Relational Schema Breakdown */}
      <div className="bg-slate-900/90 rounded-3xl border border-slate-800 p-6 shadow-xl space-y-4">
        <h3 className="text-base font-bold text-white flex items-center gap-2">
          <Database className="w-4 h-4 text-indigo-400" /> Relational Database Schema (MySQL 3NF Tables)
        </h3>
        <p className="text-xs text-slate-400">
          Normalized tables enforcing entity integrity, foreign keys, and indexes for data mining queries
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 text-xs">
          {[
            { name: 'users', role: 'Demographic profiles (age, gender, email, created_at)' },
            { name: 'movies', role: 'Catalog metadata (title, release_year, duration, imdb_rating)' },
            { name: 'genres', role: 'Unique genres dictionary (18 distinct genres)' },
            { name: 'movie_genres', role: 'M:N Junction mapping movies to multiple genres' },
            { name: 'ratings', role: 'User-Movie interaction core (0.5 to 5.0 stars with timestamps)' },
            { name: 'watch_history', role: 'Transaction baskets used for Apriori frequent itemsets' },
            { name: 'clusters', role: 'K-Means segment profiles & centroid characteristics' },
            { name: 'user_clusters', role: 'Foreign key mappings linking users to mined clusters' },
            { name: 'association_rules', role: 'Apriori discoveries with Support, Confidence, Lift' },
          ].map((t) => (
            <div key={t.name} className="p-3 rounded-xl bg-slate-800/60 border border-slate-700/60">
              <span className="font-mono font-bold text-indigo-400">{t.name}</span>
              <p className="text-[11px] text-slate-300 mt-1">{t.role}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Data Mining Mathematical Reference Table */}
      <div className="bg-slate-900/90 rounded-3xl border border-slate-800 p-6 shadow-xl space-y-4">
        <h3 className="text-base font-bold text-white flex items-center gap-2">
          <Cpu className="w-4 h-4 text-indigo-400" /> Data Mining Techniques Mathematical Reference
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 font-semibold uppercase text-[10px]">
                <th className="pb-3 px-3">Mining Technique</th>
                <th className="pb-3 px-3">Mathematical Formulation</th>
                <th className="pb-3 px-3">Primary Role in MovieMine</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-300">
              <tr>
                <td className="py-3 px-3 font-bold text-white">Collaborative Filtering</td>
                <td className="py-3 px-3 font-mono text-indigo-300 text-[11px]">Pearson / Mean-Centered Cosine Sim + k-NN</td>
                <td className="py-3 px-3">Predicts unrated movies from similar users</td>
              </tr>
              <tr>
                <td className="py-3 px-3 font-bold text-white">Content-Based Filtering</td>
                <td className="py-3 px-3 font-mono text-indigo-300 text-[11px]">TF-IDF Vector Space + Cosine Similarity</td>
                <td className="py-3 px-3">Matches plot and genre similarity across items</td>
              </tr>
              <tr>
                <td className="py-3 px-3 font-bold text-white">K-Means Clustering</td>
                <td className="py-3 px-3 font-mono text-indigo-300 text-[11px]">Minimizes WCSS J = Σ Σ ||x_i - μ_j||²</td>
                <td className="py-3 px-3">Unsupervised audience preference segmentation</td>
              </tr>
              <tr>
                <td className="py-3 px-3 font-bold text-white">Association Rule Mining</td>
                <td className="py-3 px-3 font-mono text-indigo-300 text-[11px]">Apriori Property: Lift = Conf / P(B)</td>
                <td className="py-3 px-3">Discovers frequent co-viewing patterns</td>
              </tr>
              <tr>
                <td className="py-3 px-3 font-bold text-white">Supervised Classification</td>
                <td className="py-3 px-3 font-mono text-indigo-300 text-[11px]">Random Forest & Decision Tree (Gini Impurity)</td>
                <td className="py-3 px-3">Predicts binary user preference (Like vs Dislike)</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Interactive Viva Questions Accordion */}
      <div className="bg-slate-900/90 rounded-3xl border border-slate-800 p-6 shadow-xl space-y-4">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <div>
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <BookOpen className="w-4 h-4 text-emerald-400" /> College Viva Q&A Cheat Sheet
            </h3>
            <p className="text-xs text-slate-400">Master explanations tailored for academic examination</p>
          </div>
          <span className="text-xs text-emerald-400 font-semibold bg-emerald-500/10 px-2.5 py-1 rounded-lg border border-emerald-500/20">
            {vivaQuestions.length} Core Questions
          </span>
        </div>

        <div className="space-y-3">
          {vivaQuestions.map((item, index) => {
            const isOpen = expandedFaq === index;
            return (
              <div
                key={index}
                className="rounded-2xl border border-slate-800 bg-slate-800/40 overflow-hidden transition-all"
              >
                <button
                  onClick={() => setExpandedFaq(isOpen ? -1 : index)}
                  className="w-full p-4 text-left flex items-center justify-between text-xs sm:text-sm font-semibold text-white hover:bg-slate-800/80 transition-colors"
                >
                  <span className="flex items-center gap-2">
                    <span className="text-indigo-400 font-mono font-bold">Q{index + 1}.</span>
                    <span>{item.q}</span>
                  </span>
                  {isOpen ? (
                    <ChevronUp className="w-4 h-4 text-slate-400 shrink-0" />
                  ) : (
                    <ChevronDown className="w-4 h-4 text-slate-400 shrink-0" />
                  )}
                </button>

                {isOpen && (
                  <div className="px-4 pb-4 pt-1 text-xs text-slate-300 leading-relaxed border-t border-slate-800/80 bg-slate-900/60">
                    <p className="p-3 rounded-xl bg-slate-800/60 border border-slate-700/50">
                      {item.a}
                    </p>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default SystemInfo;
