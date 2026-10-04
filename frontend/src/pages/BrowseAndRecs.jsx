import React, { useState, useEffect } from 'react';
import { recommendationApi, movieApi } from '../services/api';
import { useUser } from '../context/UserContext';
import MovieCard from '../components/MovieCard';
import { Sparkles, Search, Star, RefreshCw, Film } from 'lucide-react';

const BrowseAndRecs = ({ onSelectMovie, onRateMovie }) => {
  const { currentUser } = useUser();
  const [data, setData] = useState({
    hybrid: [],
    collaborative: [],
    content_based: [],
  });
  const [activeModel, setActiveModel] = useState('hybrid');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedGenre, setSelectedGenre] = useState('All');
  const [allMovies, setAllMovies] = useState([]);
  const [loadingRecs, setLoadingRecs] = useState(false);
  const [loadingMovies, setLoadingMovies] = useState(false);

  useEffect(() => {
    loadMovies();
  }, [selectedGenre, searchQuery]);

  useEffect(() => {
    if (currentUser?.user_id) {
      loadRecommendations(currentUser.user_id);
    }
  }, [currentUser?.user_id]);

  const loadRecommendations = async (userId) => {
    setLoadingRecs(true);
    try {
      const res = await recommendationApi.getRecommendations(userId, 8);
      setData(res.data || {});
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingRecs(false);
    }
  };

  const loadMovies = async () => {
    setLoadingMovies(true);
    try {
      const params = {
        page: 1,
        per_page: 24,
        genre: selectedGenre !== 'All' ? selectedGenre : undefined,
        search: searchQuery.trim() || undefined,
        sort_by: 'rating',
      };
      const res = await movieApi.getMovies(params);
      setAllMovies(res.data?.movies || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingMovies(false);
    }
  };

  const genres = ['All', 'Action', 'Sci-Fi', 'Adventure', 'Drama', 'Comedy', 'Crime', 'Animation', 'Thriller', 'Horror', 'Romance'];

  const recList = data[activeModel] || [];

  return (
    <div className="space-y-10 pb-16 text-left">
      {/* Top Search & Filter Bar */}
      <div className="flex flex-col md:flex-row items-center justify-between gap-4 bg-slate-900/90 p-4 sm:p-5 rounded-2xl border border-slate-800 shadow-xl">
        {/* Search Input */}
        <div className="relative w-full md:w-80">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search 220+ movies..."
            className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
          />
        </div>

        {/* Genre Filter Pills */}
        <div className="flex items-center gap-1.5 overflow-x-auto w-full md:w-auto pb-1 md:pb-0 no-scrollbar">
          {genres.map((g) => (
            <button
              key={g}
              onClick={() => setSelectedGenre(g)}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-bold whitespace-nowrap transition-all ${
                selectedGenre === g
                  ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                  : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800/80 hover:bg-slate-800'
              }`}
            >
              {g}
            </button>
          ))}
        </div>
      </div>

      {/* Recommended For You Section */}
      <section className="space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-gradient-to-tr from-indigo-500 to-pink-500 text-white shadow-md shadow-indigo-500/20">
              <Sparkles className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-xl sm:text-2xl font-black text-white tracking-tight">
                Recommended For You
              </h2>
              <p className="text-xs text-slate-400">
                Personalized for <span className="text-indigo-400 font-bold">{currentUser?.name}</span> ({currentUser?.cluster?.cluster_name || 'Active Persona'})
              </p>
            </div>
          </div>

          {/* Quick Algorithm Toggle */}
          <div className="flex items-center gap-1.5 bg-slate-900 p-1 rounded-xl border border-slate-800 self-start sm:self-auto">
            {[
              { id: 'hybrid', label: '⭐ Hybrid (Best)' },
              { id: 'collaborative', label: '👥 Collaborative' },
              { id: 'content_based', label: '🎬 Similar Content' },
            ].map((btn) => (
              <button
                key={btn.id}
                onClick={() => setActiveModel(btn.id)}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                  activeModel === btn.id
                    ? 'bg-indigo-600 text-white shadow-md'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                {btn.label}
              </button>
            ))}
          </div>
        </div>

        {/* Recommendation Cards Grid */}
        {loadingRecs ? (
          <div className="py-16 text-center text-slate-400 text-xs">Computing recommendations from database...</div>
        ) : recList.length === 0 ? (
          <div className="py-12 text-center bg-slate-900/40 rounded-2xl border border-slate-800 p-6 text-xs text-slate-400">
            No recommendations generated. Rate a movie below to provide preferences!
          </div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-4 gap-4">
            {recList.map((m) => (
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

      {/* Movie Catalog Grid */}
      <section className="space-y-4 pt-4 border-t border-slate-800/80">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Film className="w-5 h-5 text-yellow-400" />
            <h2 className="text-xl font-black text-white tracking-tight">
              Popular Catalog ({allMovies.length} Titles)
            </h2>
          </div>
          <span className="text-xs text-slate-400">Showing top rated releases</span>
        </div>

        {loadingMovies ? (
          <div className="py-16 text-center text-slate-400 text-xs">Loading movies...</div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-4 gap-4">
            {allMovies.map((m) => (
              <MovieCard
                key={m.movie_id}
                movie={m}
                onSelect={onSelectMovie}
                onRate={onRateMovie}
              />
            ))}
          </div>
        )}
      </section>
    </div>
  );
};

export default BrowseAndRecs;
