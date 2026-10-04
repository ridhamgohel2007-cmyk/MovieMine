import React, { useState, useEffect } from 'react';
import { movieApi, miningApi } from '../services/api';
import { useUser } from '../context/UserContext';
import AlgorithmFlowDiagram from '../components/AlgorithmFlowDiagram';
import { Sparkles, Play, CheckCircle, XCircle, BarChart3, HelpCircle } from 'lucide-react';

const ClassificationDemo = () => {
  const { users, currentUser } = useUser();
  const [movies, setMovies] = useState([]);
  const [selectedUserId, setSelectedUserId] = useState(currentUser?.user_id || 1);
  const [selectedMovieId, setSelectedMovieId] = useState(1);
  const [result, setResult] = useState(null);
  const [running, setRunning] = useState(false);

  useEffect(() => {
    loadMovies();
  }, []);

  useEffect(() => {
    if (currentUser?.user_id) {
      setSelectedUserId(currentUser.user_id);
    }
  }, [currentUser?.user_id]);

  const loadMovies = async () => {
    try {
      const res = await movieApi.getMovies({ page: 1, per_page: 100 });
      const mList = res.data.movies || [];
      setMovies(mList);
      if (mList.length > 0) {
        setSelectedMovieId(mList[0].movie_id);
      }
    } catch (err) {
      console.error('Failed to load movies:', err);
    }
  };

  const handlePredict = async () => {
    setRunning(true);
    try {
      const res = await miningApi.classifyPreference(selectedUserId, selectedMovieId);
      setResult(res.data);
    } catch (err) {
      console.error('Failed to classify preference:', err);
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="space-y-8 pb-16 text-left">
      {/* Header */}
      <div className="bg-slate-900/90 p-6 sm:p-8 rounded-3xl border border-slate-800 shadow-2xl flex flex-col md:flex-row md:items-center md:justify-between gap-6">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-semibold mb-2 border border-indigo-500/30">
            <Sparkles className="w-3.5 h-3.5" /> Supervised Machine Learning
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Supervised Preference Classification
          </h1>
          <p className="text-xs text-slate-400 mt-1 max-w-2xl">
            Uses Decision Tree and Random Forest classifiers to predict whether a specific user is likely to rate a candidate movie favorably (≥ 3.5 stars) before recommending it.
          </p>
        </div>

        <button
          onClick={handlePredict}
          disabled={running}
          className="flex items-center gap-2 px-6 py-3 rounded-2xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold shadow-xl shadow-indigo-600/30 transition-all disabled:opacity-50 shrink-0"
        >
          <Play className={`w-4 h-4 fill-white ${running ? 'animate-spin' : ''}`} />
          <span>{running ? 'Predicting...' : 'PREDICT PREFERENCE'}</span>
        </button>
      </div>

      {/* Academic Flow Diagram */}
      <AlgorithmFlowDiagram
        algorithmName="Supervised Classification (Decision Tree & Random Forest Ensemble)"
        steps={[
          { title: '1. INPUT', desc: 'Target User Profile (Affinity, Avg Rating) + Candidate Movie Metadata' },
          { title: '2. FEATURE VECTOR', desc: '[user_avg, ratings_count, genre_affinity, imdb_score, duration, year]' },
          { title: '3. CLASSIFIER', desc: 'Trained Random Forest (30 estimators) & Decision Tree (max_depth=4)' },
          { title: '4. PROBABILITY', desc: 'Computes class posterior P(Like >= 3.5 | Features)' },
          { title: '5. VERDICT', desc: 'Binary classification: "LIKED" or "UNLIKELY TO PREFER"' },
        ]}
      />

      {/* Interactive Selector Controls */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 bg-slate-900/90 p-6 rounded-3xl border border-slate-800 shadow-xl">
        {/* User Selection */}
        <div>
          <label className="text-xs font-bold text-slate-300 block mb-2">1. Select Target User</label>
          <select
            value={selectedUserId}
            onChange={(e) => setSelectedUserId(parseInt(e.target.value, 10))}
            className="w-full p-3 rounded-xl bg-slate-800 border border-slate-700 text-xs text-white focus:outline-none focus:border-indigo-500"
          >
            {users.map((u) => (
              <option key={u.user_id} value={u.user_id}>
                User #{u.user_id}: {u.name} ({u.gender}, {u.age}y)
              </option>
            ))}
          </select>
        </div>

        {/* Movie Selection */}
        <div>
          <label className="text-xs font-bold text-slate-300 block mb-2">2. Select Candidate Movie</label>
          <select
            value={selectedMovieId}
            onChange={(e) => setSelectedMovieId(parseInt(e.target.value, 10))}
            className="w-full p-3 rounded-xl bg-slate-800 border border-slate-700 text-xs text-white focus:outline-none focus:border-indigo-500"
          >
            {movies.map((m) => (
              <option key={m.movie_id} value={m.movie_id}>
                {m.title} ({m.release_year}) - IMDb {m.imdb_rating} ★
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Result Display */}
      {result && (
        <div className="bg-slate-900/90 rounded-3xl border border-slate-800 p-6 sm:p-8 shadow-2xl space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-800 pb-4">
            <div>
              <span className="text-[10px] uppercase font-bold text-indigo-400 tracking-wider">
                Classification Result
              </span>
              <h3 className="text-xl font-bold text-white mt-1">
                Preference Prediction for {result.user_name} on "{result.movie_title}"
              </h3>
            </div>

            <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold ${
              result.like_percentage >= 50
                ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                : 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
            }`}>
              {result.like_percentage >= 50 ? <CheckCircle className="w-4 h-4" /> : <XCircle className="w-4 h-4" />}
              <span>{result.prediction}</span>
            </div>
          </div>

          {/* Probability Gauge Bar */}
          <div>
            <div className="flex justify-between text-xs font-semibold mb-2">
              <span className="text-slate-400">Model Confidence Probability</span>
              <span className="text-white font-mono">{result.like_percentage}% Likelihood to Like</span>
            </div>
            <div className="w-full h-3 rounded-full bg-slate-800 overflow-hidden">
              <div
                className={`h-full transition-all duration-700 rounded-full ${
                  result.like_percentage >= 50
                    ? 'bg-gradient-to-r from-indigo-500 to-emerald-400'
                    : 'bg-gradient-to-r from-amber-500 to-rose-500'
                }`}
                style={{ width: `${result.like_percentage}%` }}
              ></div>
            </div>
          </div>

          {/* Feature Breakdown Table */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-2">
            <div className="p-3.5 rounded-xl bg-slate-800/60 border border-slate-700/60">
              <span className="text-[10px] text-slate-400 uppercase font-semibold">User Genre Affinity</span>
              <div className="text-sm font-bold text-indigo-400 mt-1">
                {result.features_analyzed?.user_genre_affinity}
              </div>
            </div>
            <div className="p-3.5 rounded-xl bg-slate-800/60 border border-slate-700/60">
              <span className="text-[10px] text-slate-400 uppercase font-semibold">User Avg Rating</span>
              <div className="text-sm font-bold text-yellow-400 mt-1">
                {result.features_analyzed?.user_avg_rating} ★
              </div>
            </div>
            <div className="p-3.5 rounded-xl bg-slate-800/60 border border-slate-700/60">
              <span className="text-[10px] text-slate-400 uppercase font-semibold">Movie IMDb Rating</span>
              <div className="text-sm font-bold text-white mt-1">
                {result.features_analyzed?.movie_imdb_rating} / 10
              </div>
            </div>
            <div className="p-3.5 rounded-xl bg-slate-800/60 border border-slate-700/60">
              <span className="text-[10px] text-slate-400 uppercase font-semibold">Movie Genres</span>
              <div className="text-xs font-semibold text-slate-300 mt-1 truncate">
                {result.features_analyzed?.movie_genres?.join(', ')}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ClassificationDemo;
