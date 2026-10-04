import React, { useState, useEffect } from 'react';
import { recommendationApi, movieApi } from '../services/api';
import { useUser } from '../context/UserContext';
import MovieCard from '../components/MovieCard';
import { Sparkles, Search, Star, RefreshCw, Film, X, Compass, Zap } from 'lucide-react';

const POPULAR_SEARCH_SUGGESTIONS = ['Interstellar', 'The Dark Knight', 'Inception', 'Avengers', 'Dune', 'Toy Story'];

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

  // Search & Similar Recommendations States
  const [searchResults, setSearchResults] = useState([]);
  const [selectedSearchMovie, setSelectedSearchMovie] = useState(null);
  const [similarMovies, setSimilarMovies] = useState([]);
  const [loadingSearch, setLoadingSearch] = useState(false);
  const [loadingSimilar, setLoadingSimilar] = useState(false);

  useEffect(() => {
    loadMovies();
  }, [selectedGenre]);

  useEffect(() => {
    if (currentUser?.user_id) {
      loadRecommendations(currentUser.user_id);
    }
  }, [currentUser?.user_id]);

  // Live Search & Similar Recommendations Debounce Pipeline
  useEffect(() => {
    const query = searchQuery.trim();
    if (!query) {
      setSearchResults([]);
      setSelectedSearchMovie(null);
      setSimilarMovies([]);
      return;
    }

    const timer = setTimeout(async () => {
      setLoadingSearch(true);
      try {
        const res = await movieApi.searchMovies(query);
        const results = res.data || [];
        setSearchResults(results);

        if (results.length > 0) {
          const topMovie = results[0];
          setSelectedSearchMovie(topMovie);
          loadSimilarForMovie(topMovie.movie_id);
        } else {
          setSelectedSearchMovie(null);
          setSimilarMovies([]);
        }
      } catch (err) {
        console.error('Search error:', err);
      } finally {
        setLoadingSearch(false);
      }
    }, 200);

    return () => clearTimeout(timer);
  }, [searchQuery]);

  const loadSimilarForMovie = async (movieId) => {
    setLoadingSimilar(true);
    try {
      const res = await recommendationApi.getContentBased({ movie_id: movieId, top_n: 8 });
      setSimilarMovies(res.data || []);
    } catch (err) {
      console.error('Error fetching similar movies:', err);
      setSimilarMovies([]);
    } finally {
      setLoadingSimilar(false);
    }
  };

  const handleSelectSearchMovie = (movie) => {
    setSelectedSearchMovie(movie);
    loadSimilarForMovie(movie.movie_id);
  };

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
      <div className="space-y-3 bg-slate-900/90 p-4 sm:p-5 rounded-3xl border border-slate-800 shadow-xl">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          {/* Search Input with Clear Button */}
          <div className="relative w-full md:w-96">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search movie (e.g. Interstellar, Batman)..."
              className="w-full pl-10 pr-10 py-2.5 rounded-2xl bg-slate-950 border border-slate-800 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 shadow-inner"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="absolute right-3 top-3 text-slate-400 hover:text-white p-0.5 rounded-full hover:bg-slate-800 transition-colors"
                title="Clear Search"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>

          {/* Genre Filter Pills */}
          <div className="flex items-center gap-1.5 overflow-x-auto w-full md:w-auto pb-1 md:pb-0 no-scrollbar">
            {genres.map((g) => (
              <button
                key={g}
                onClick={() => {
                  setSelectedGenre(g);
                  if (searchQuery) setSearchQuery('');
                }}
                className={`px-3.5 py-1.5 rounded-xl text-xs font-bold whitespace-nowrap transition-all ${
                  selectedGenre === g && !searchQuery
                    ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                    : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800/80 hover:bg-slate-800'
                }`}
              >
                {g}
              </button>
            ))}
          </div>
        </div>

        {/* Quick Suggestion Chips */}
        <div className="flex items-center gap-2 pt-1 overflow-x-auto no-scrollbar text-xs">
          <span className="text-slate-500 font-semibold flex items-center gap-1 shrink-0">
            <Zap className="w-3.5 h-3.5 text-yellow-400" /> Quick Search:
          </span>
          {POPULAR_SEARCH_SUGGESTIONS.map((title) => (
            <button
              key={title}
              onClick={() => setSearchQuery(title)}
              className="px-2.5 py-1 rounded-lg bg-slate-950 hover:bg-slate-800 text-slate-300 hover:text-indigo-300 border border-slate-800 text-[11px] font-medium shrink-0 transition-colors"
            >
              {title}
            </button>
          ))}
        </div>
      </div>

      {/* CONDITIONAL DISPLAY: IF USER IS SEARCHING */}
      {searchQuery.trim() ? (
        <div className="space-y-12 animate-fadeIn">
          {/* 1. Direct Search Matches */}
          <section className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Search className="w-5 h-5 text-indigo-400" />
                <h2 className="text-xl sm:text-2xl font-black text-white tracking-tight">
                  Search Results for "{searchQuery}"
                </h2>
                <span className="text-xs font-bold px-2.5 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                  {searchResults.length} {searchResults.length === 1 ? 'match' : 'matches'}
                </span>
              </div>
              <button
                onClick={() => setSearchQuery('')}
                className="text-xs text-slate-400 hover:text-white px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 hover:bg-slate-800 transition-colors"
              >
                Clear Search
              </button>
            </div>

            {loadingSearch ? (
              <div className="py-12 text-center text-xs text-slate-400">Searching 220+ movies...</div>
            ) : searchResults.length === 0 ? (
              <div className="p-10 text-center bg-slate-900/50 rounded-3xl border border-slate-800 text-slate-400 space-y-2">
                <p className="text-sm font-semibold text-white">No movies found matching "{searchQuery}"</p>
                <p className="text-xs text-slate-400">Try one of the quick suggestions above like <span className="text-indigo-400 font-bold">Interstellar</span> or <span className="text-indigo-400 font-bold">The Dark Knight</span>.</p>
              </div>
            ) : (
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-4 gap-4">
                {searchResults.map((m) => {
                  const isSelected = selectedSearchMovie?.movie_id === m.movie_id;
                  return (
                    <div
                      key={m.movie_id}
                      className={`relative rounded-2xl transition-all ${
                        isSelected
                          ? 'ring-2 ring-indigo-500 ring-offset-2 ring-offset-slate-950 scale-[1.02]'
                          : 'opacity-85 hover:opacity-100'
                      }`}
                      onClick={() => handleSelectSearchMovie(m)}
                    >
                      {isSelected && (
                        <div className="absolute -top-3 left-1/2 -translate-x-1/2 z-20 px-3 py-0.5 rounded-full bg-gradient-to-r from-indigo-500 to-pink-500 text-white text-[10px] font-black uppercase tracking-wider shadow-lg whitespace-nowrap">
                          Selected for Similar Recs
                        </div>
                      )}
                      <MovieCard
                        movie={m}
                        onSelect={onSelectMovie}
                        onRate={onRateMovie}
                      />
                    </div>
                  );
                })}
              </div>
            )}
          </section>

          {/* 2. Similar Recommendations Based on the Searched Movie */}
          {selectedSearchMovie && (
            <section className="space-y-4 pt-6 border-t border-slate-800/80">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div className="flex items-center gap-2.5">
                  <div className="p-2 rounded-2xl bg-gradient-to-tr from-indigo-500 to-pink-500 text-white shadow-lg shadow-indigo-500/25">
                    <Sparkles className="w-5 h-5" />
                  </div>
                  <div>
                    <h2 className="text-xl sm:text-2xl font-black text-white tracking-tight">
                      Recommended Similar to <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-pink-400">"{selectedSearchMovie.title}"</span>
                    </h2>
                    <p className="text-xs text-slate-400">
                      Content-Based Similarity Algorithm (Cosine Similarity on Genre + Synopsis TF-IDF)
                    </p>
                  </div>
                </div>
                <span className="text-xs text-slate-500">
                  {searchResults.length > 1 ? 'Click any matching card above to change base movie' : ''}
                </span>
              </div>

              {loadingSimilar ? (
                <div className="py-12 text-center text-xs text-slate-400">Computing similar movie vectors...</div>
              ) : similarMovies.length === 0 ? (
                <div className="py-8 text-center bg-slate-900/40 rounded-2xl border border-slate-800 text-xs text-slate-400">
                  No similar movies found.
                </div>
              ) : (
                <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-4 gap-4">
                  {similarMovies.map((m) => (
                    <MovieCard
                      key={m.movie_id}
                      movie={m}
                      onSelect={onSelectMovie}
                      onRate={onRateMovie}
                      matchPercentage={m.match_percentage}
                      methodTag="Similar Content"
                    />
                  ))}
                </div>
              )}
            </section>
          )}
        </div>
      ) : (
        /* NORMAL VIEW: PERSONALIZED RECOMMENDATIONS + POPULAR CATALOG */
        <>
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
        </>
      )}
    </div>
  );
};

export default BrowseAndRecs;
