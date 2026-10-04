import React, { useState, useEffect } from 'react';
import { movieApi, recommendationApi, miningApi } from '../services/api';
import { useUser } from '../context/UserContext';
import MovieCard from '../components/MovieCard';
import MetricCard from '../components/MetricCard';
import { 
  Sparkles, TrendingUp, Award, Search, 
  Layers, Users, Star, ArrowRight, Play
} from 'lucide-react';

const Home = ({ onSelectMovie, onRateMovie, setActiveTab }) => {
  const { currentUser } = useUser();
  const [stats, setStats] = useState(null);
  const [recommendedMovies, setRecommendedMovies] = useState([]);
  const [topRatedMovies, setTopRatedMovies] = useState([]);
  const [genres, setGenres] = useState([]);
  const [selectedGenre, setSelectedGenre] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHomeData();
  }, [currentUser]);

  const loadHomeData = async () => {
    setLoading(true);
    try {
      const [statsRes, genresRes, topMoviesRes] = await Promise.all([
        miningApi.getStatistics(),
        movieApi.getGenres(),
        movieApi.getMovies({ page: 1, per_page: 8, sort_by: 'rating' }),
      ]);

      setStats(statsRes.data);
      setGenres(genresRes.data || []);
      setTopRatedMovies(topMoviesRes.data?.movies || []);

      if (currentUser) {
        const recRes = await recommendationApi.getRecommendations(currentUser.user_id, 8);
        setRecommendedMovies(recRes.data?.hybrid || recRes.data?.content_based || []);
      }
    } catch (err) {
      console.error('Failed to load home data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      setActiveTab('movies');
    }
  };

  return (
    <div className="space-y-10 pb-16">
      {/* Hero Banner */}
      <section className="relative rounded-3xl overflow-hidden bg-gradient-to-r from-slate-900 via-indigo-950/80 to-slate-900 border border-slate-800 p-8 sm:p-12 shadow-2xl">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-indigo-500/10 via-transparent to-transparent"></div>
        <div className="relative z-10 max-w-3xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/20 border border-indigo-500/30 text-indigo-300 text-xs font-semibold uppercase tracking-wider mb-4">
            <Sparkles className="w-3.5 h-3.5" /> Data Mining Powered Recommender
          </div>
          <h1 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight leading-tight">
            Discover Movies Mined From <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-300 to-pink-400">Audience Behavior</span>
          </h1>
          <p className="mt-4 text-sm sm:text-base text-slate-300 leading-relaxed max-w-2xl">
            MovieMine merges <span className="text-white font-medium">Collaborative Filtering</span>, <span className="text-white font-medium">TF-IDF Content Similarity</span>, <span className="text-white font-medium">K-Means Audience Clustering</span>, and <span className="text-white font-medium">Apriori Association Rules</span> into a single database-driven academic system.
          </p>

          {/* Quick Search & Actions */}
          <div className="mt-8 flex flex-wrap items-center gap-3">
            <form onSubmit={handleSearchSubmit} className="relative flex-1 min-w-[260px] max-w-md">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search movies by title, actor, or genre..."
                className="w-full pl-10 pr-4 py-3 rounded-xl bg-slate-900/90 border border-slate-700 text-white placeholder-slate-400 text-sm focus:outline-none focus:border-indigo-500 shadow-inner"
              />
              <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
            </form>

            <button
              onClick={() => setActiveTab('recommendations')}
              className="px-5 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-semibold shadow-lg shadow-indigo-600/30 transition-all flex items-center gap-2"
            >
              <span>Get Recommendations</span>
              <ArrowRight className="w-4 h-4" />
            </button>

            <button
              onClick={() => setActiveTab('dashboard')}
              className="px-4 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-sm font-semibold border border-slate-700 transition-all"
            >
              Faculty Mining Dashboard
            </button>
          </div>
        </div>
      </section>

      {/* KPI Stats Overview */}
      <section className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <MetricCard
          title="Total Movies Mined"
          value={stats?.total_movies || 225}
          subtitle="Across 18 Curated Genres"
          icon={TrendingUp}
          color="indigo"
        />
        <MetricCard
          title="Active Users"
          value={stats?.total_users || 120}
          subtitle="4 Persona Segments"
          icon={Users}
          color="purple"
        />
        <MetricCard
          title="User Ratings"
          value={stats?.total_ratings || 2560}
          subtitle={`Avg: ${stats?.average_rating || 3.9} Stars`}
          icon={Star}
          color="amber"
        />
        <MetricCard
          title="Discovered Rules"
          value={stats?.association_rules_count || 13}
          subtitle="Apriori Pattern Mining"
          icon={Layers}
          color="emerald"
        />
      </section>

      {/* Genre Filter Pills */}
      <section>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <span>Explore Genres</span>
          </h2>
          <button
            onClick={() => setActiveTab('movies')}
            className="text-xs text-indigo-400 hover:text-indigo-300 font-medium"
          >
            View All Movies →
          </button>
        </div>
        <div className="flex items-center gap-2 overflow-x-auto pb-2 no-scrollbar">
          {['All', 'Action', 'Sci-Fi', 'Adventure', 'Drama', 'Comedy', 'Thriller', 'Animation', 'Crime', 'Horror', 'Romance'].map((genre) => (
            <button
              key={genre}
              onClick={() => {
                setSelectedGenre(genre);
                if (genre !== 'All') {
                  setActiveTab('movies');
                }
              }}
              className={`px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all ${
                selectedGenre === genre
                  ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                  : 'bg-slate-800/80 hover:bg-slate-700 text-slate-300 border border-slate-700/60'
              }`}
            >
              {genre}
            </button>
          ))}
        </div>
      </section>

      {/* Recommended For Active User */}
      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-indigo-400" />
              <h2 className="text-xl font-bold text-white">Recommended For You</h2>
              <span className="text-xs px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 font-semibold">
                {currentUser ? currentUser.name : 'Active Persona'}
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Hybrid prediction blending Collaborative Filtering (50%), Content Similarity (30%), and Popularity (20%)
            </p>
          </div>
          <button
            onClick={() => setActiveTab('recommendations')}
            className="text-xs font-semibold text-indigo-400 hover:text-indigo-300 flex items-center gap-1"
          >
            Deep Recommendations →
          </button>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
          {recommendedMovies.slice(0, 8).map((m) => (
            <MovieCard
              key={m.movie_id}
              movie={m}
              onSelect={onSelectMovie}
              onRate={onRateMovie}
              matchPercentage={m.match_percentage}
              methodTag={m.recommendation_method}
            />
          ))}
        </div>
      </section>

      {/* Top Rated Movies */}
      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Award className="w-5 h-5 text-amber-400" />
            <h2 className="text-xl font-bold text-white">Top Rated Masterpieces</h2>
          </div>
          <button
            onClick={() => setActiveTab('movies')}
            className="text-xs font-semibold text-indigo-400 hover:text-indigo-300"
          >
            Explore Catalog →
          </button>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
          {topRatedMovies.slice(0, 8).map((m) => (
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

export default Home;
