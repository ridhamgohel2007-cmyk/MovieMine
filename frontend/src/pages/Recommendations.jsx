import React, { useState, useEffect } from 'react';
import { recommendationApi, movieApi } from '../services/api';
import { useUser } from '../context/UserContext';
import MovieCard from '../components/MovieCard';
import { Sparkles, Users, Cpu, Layers, Search, Filter, RefreshCw, Star } from 'lucide-react';

const Recommendations = ({ onSelectMovie, onRateMovie }) => {
  const { currentUser } = useUser();
  const [data, setData] = useState({
    hybrid: [],
    collaborative: [],
    content_based: [],
    cluster_popular: [],
  });
  const [activeModel, setActiveModel] = useState('hybrid');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedGenre, setSelectedGenre] = useState('All');
  const [genres, setGenres] = useState([]);
  const [catalogMovies, setCatalogMovies] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadGenres();
    loadCatalog();
  }, []);

  useEffect(() => {
    if (currentUser?.user_id) {
      loadRecommendations(currentUser.user_id);
    }
  }, [currentUser?.user_id]);

  const loadGenres = async () => {
    try {
      const res = await movieApi.getGenres();
      setGenres(res.data || []);
    } catch (err) {
      console.error(err);
    }
  };

  const loadCatalog = async () => {
    try {
      const res = await movieApi.getMovies({ page: 1, per_page: 12, sort_by: 'rating' });
      setCatalogMovies(res.data?.movies || []);
    } catch (err) {
      console.error(err);
    }
  };

  const loadRecommendations = async (userId) => {
    setLoading(true);
    try {
      const res = await recommendationApi.getRecommendations(userId, 8);
      setData(res.data);
    } catch (err) {
      console.error('Failed to load recommendations:', err);
    } finally {
      setLoading(false);
    }
  };

  const modelExplanations = {
    hybrid: 'Combines 50% Collaborative Filtering + 30% Content Matching + 20% Global Popularity into a single best recommendation score.',
    collaborative: 'Finds other users who gave similar ratings to you in the past, and recommends what they loved.',
    content_based: 'Compares movie genres and plot descriptions using TF-IDF and Cosine Similarity to find movies like your favorites.',
    cluster_popular: `Recommends movies that are most popular among users in your audience segment (${currentUser?.cluster?.cluster_name || 'your cluster'}).`,
  };

  const currentList = data[activeModel] || [];

  return (
    <div className="space-y-8 pb-16 text-left">
      {/* Cool Hero Banner */}
      <div className="relative rounded-3xl overflow-hidden bg-gradient-to-r from-slate-900 via-indigo-950/70 to-slate-900 border border-slate-800 p-6 sm:p-8 shadow-2xl">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
          <div>
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-semibold mb-3 border border-indigo-500/30">
              <Sparkles className="w-3.5 h-3.5" /> Data-Mining Recommendation System
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              Recommended For <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-pink-400">{currentUser?.name}</span>
            </h1>
            <p className="text-xs text-slate-300 mt-1 max-w-xl">
              Audience Category: <span className="text-indigo-400 font-bold">{currentUser?.cluster?.cluster_name || 'Active Persona'}</span>. Switch personas anytime in the top-right corner to see how recommendations instantly adapt!
            </p>
          </div>

          <button
            onClick={() => loadRecommendations(currentUser?.user_id)}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold shadow-lg shadow-indigo-600/30 transition-all disabled:opacity-50 shrink-0"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>Re-Mine Recommendations</span>
          </button>
        </div>

        {/* Algorithm Switcher Tabs */}
        <div className="mt-6 pt-5 border-t border-slate-800/80 flex flex-wrap items-center gap-2">
          <span className="text-xs font-bold text-slate-400 mr-1">Choose Algorithm:</span>
          {[
            { id: 'hybrid', label: '⭐ Hybrid (Best)', icon: Sparkles },
            { id: 'collaborative', label: '👥 Collaborative (k-NN)', icon: Users },
            { id: 'content_based', label: '🎬 Content Similarity', icon: Cpu },
            { id: 'cluster_popular', label: '🔥 Cluster Top Picks', icon: Layers },
          ].map((btn) => (
            <button
              key={btn.id}
              onClick={() => setActiveModel(btn.id)}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 ${
                activeModel === btn.id
                  ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30 scale-105'
                  : 'bg-slate-800/80 hover:bg-slate-800 text-slate-400 hover:text-white border border-slate-700/60'
              }`}
            >
              <span>{btn.label}</span>
            </button>
          ))}
        </div>

        {/* 1-Sentence Plain English Explanation Box */}
        <div className="mt-4 p-3 rounded-xl bg-slate-950/60 border border-indigo-500/20 text-xs text-indigo-300 flex items-center gap-2">
          <span className="font-bold text-white uppercase text-[10px] bg-indigo-500/30 px-2 py-0.5 rounded">
            Viva Explanation:
          </span>
          <span>{modelExplanations[activeModel]}</span>
        </div>
      </div>

      {/* Recommended Movies Section */}
      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-indigo-400" />
            Top Mined Picks ({currentList.length} movies)
          </h2>
          <span className="text-xs text-slate-400">Click any movie to see details or rate</span>
        </div>

        {loading ? (
          <div className="py-16 text-center text-slate-400 text-xs">Computing similarity scores...</div>
        ) : currentList.length === 0 ? (
          <div className="py-16 text-center bg-slate-900/40 rounded-2xl border border-slate-800 p-8 text-xs text-slate-400">
            No recommendations generated yet. Try rating a movie below to provide seed preferences!
          </div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
            {currentList.map((m) => (
              <MovieCard
                key={m.movie_id}
                movie={m}
                onSelect={onSelectMovie}
                onRate={onRateMovie}
                matchPercentage={m.match_percentage}
                methodTag={m.recommendation_method?.split('(')[0]}
              />
            ))}
          </div>
        )}
      </section>

      {/* Popular Movie Catalog Section */}
      <section className="space-y-4 pt-4 border-t border-slate-800/80">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Star className="w-4 h-4 text-yellow-400" />
              Explore Movie Catalog ({catalogMovies.length} Popular Titles)
            </h2>
            <p className="text-xs text-slate-400">Rate any movie below to immediately update your mined recommendations!</p>
          </div>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
          {catalogMovies.map((m) => (
            <MovieCard
              key={m.movie_id}
              movie={m}
              onSelect={onSelectMovie}
              onRate={onRateMovie}
            />
          ))}
        </div>
      </section>
    </div>
  );
};

export default Recommendations;
