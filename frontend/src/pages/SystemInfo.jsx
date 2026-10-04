import React, { useState } from 'react';
import { BookOpen, ChevronDown, ChevronUp, Database, ExternalLink, CheckCircle } from 'lucide-react';

const SystemInfo = () => {
  const [expandedFaq, setExpandedFaq] = useState(0);

  const topVivaQuestions = [
    {
      q: '1. What is the main objective of this project?',
      a: 'To build a database-driven Data Mining system that doesn\'t just search movies, but actually stores user viewing data in MySQL, preprocesses it, and applies multiple data mining techniques: Collaborative Filtering, Content-Based Similarity, K-Means Clustering, and Apriori Association Rules.'
    },
    {
      q: '2. How does your Recommendation System work? (Explain Hybrid Formula)',
      a: 'We combine 3 signals into a Hybrid Score: 50% Collaborative Filtering (what similar users liked) + 30% Content-Based Filtering (matching movie genres & plot synopses via TF-IDF Cosine Similarity) + 20% Global Popularity. This solves the Cold-Start problem when a user has few ratings.'
    },
    {
      q: '3. What is Collaborative Filtering vs Content-Based Filtering?',
      a: 'Collaborative Filtering looks at user behavior: "Users who agreed with you in the past will agree with you in the future." Content-Based Filtering looks at item features: "If you liked Inception, you will like Interstellar because both share Sci-Fi, Adventure genres and Nolan directing style."'
    },
    {
      q: '4. Why did you use K-Means Clustering and what do the clusters represent?',
      a: 'K-Means is an unsupervised learning algorithm. We used it to partition 120 users into 4 distinct audience segments based on their genre ratings. For example, Cluster 0 represents Action & Sci-Fi fans, while Cluster 1 represents Drama & Romance lovers.'
    },
    {
      q: '5. In Apriori, what is Support, Confidence, and Lift?',
      a: 'Support is how frequently both movies appear together across all users. Confidence is the probability that a viewer of Movie A will also like Movie B. Lift measures correlation strength over random chance; a Lift > 1 proves a real positive association.'
    },
    {
      q: '6. What Kaggle dataset did you use and what preprocessing was done?',
      a: 'We used The Movies Dataset (Kaggle) and MovieLens. We preprocessed the data by removing duplicate ratings, imputing missing runtimes, encoding genres into binary vectors, and mean-centering user ratings to remove harsh rater bias.'
    },
    {
      q: '7. What database did you use and why?',
      a: 'We designed a 10-table normalized relational schema in MySQL with primary keys, foreign keys, and indexes. It stores users, movies, ratings, watch history, clusters, and mined association rules.'
    },
    {
      q: '8. What is the Cold-Start problem and how did you solve it?',
      a: 'Cold-start happens when a new user has zero ratings, making collaborative filtering impossible. Our hybrid model solves this by falling back to content-based genre similarities and top-rated IMDb movies until the user rates their first few movies.'
    }
  ];

  return (
    <div className="space-y-8 pb-16 text-left">
      {/* Header Banner */}
      <div className="bg-slate-900/90 p-6 sm:p-8 rounded-3xl border border-slate-800 shadow-2xl">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-semibold mb-2 border border-emerald-500/30">
          <BookOpen className="w-3.5 h-3.5" /> Exam & Defense Guide
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          College Viva Cheat Sheet
        </h1>
        <p className="text-xs text-slate-300 mt-1 max-w-xl">
          The 8 most frequently asked questions by external examiners, with concise 2-sentence answers ready to speak in your viva!
        </p>
      </div>

      {/* Dataset Link Card */}
      <div className="p-4 rounded-2xl bg-indigo-950/40 border border-indigo-500/30 flex items-center justify-between text-xs">
        <div>
          <div className="font-bold text-white">Kaggle Dataset Used</div>
          <div className="text-slate-400">The Movies Dataset & MovieLens 100k Benchmark</div>
        </div>
        <a
          href="https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset"
          target="_blank"
          rel="noreferrer"
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold transition-colors"
        >
          <span>Open Kaggle Link</span>
          <ExternalLink className="w-3.5 h-3.5" />
        </a>
      </div>

      {/* Questions Accordion */}
      <div className="space-y-3">
        {topVivaQuestions.map((item, index) => {
          const isOpen = expandedFaq === index;
          return (
            <div
              key={index}
              className="rounded-2xl border border-slate-800 bg-slate-900/90 overflow-hidden transition-all shadow-lg"
            >
              <button
                onClick={() => setExpandedFaq(isOpen ? -1 : index)}
                className="w-full p-4 text-left flex items-center justify-between text-xs sm:text-sm font-bold text-white hover:bg-slate-800/80 transition-colors"
              >
                <span>{item.q}</span>
                {isOpen ? (
                  <ChevronUp className="w-4 h-4 text-indigo-400 shrink-0" />
                ) : (
                  <ChevronDown className="w-4 h-4 text-slate-400 shrink-0" />
                )}
              </button>

              {isOpen && (
                <div className="px-4 pb-4 pt-1 text-xs text-slate-300 leading-relaxed border-t border-slate-800/80 bg-slate-950/50">
                  <p className="p-3 rounded-xl bg-slate-800/50 border border-slate-700/50 text-indigo-200">
                    {item.a}
                  </p>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default SystemInfo;
