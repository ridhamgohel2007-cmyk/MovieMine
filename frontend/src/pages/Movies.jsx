import React, { useState, useEffect } from 'react';
import { movieApi } from '../services/api';
import MovieCard from '../components/MovieCard';
import { Search, Filter, ArrowUpDown, ChevronLeft, ChevronRight } from 'lucide-react';

const Movies = ({ onSelectMovie, onRateMovie }) => {
  const [movies, setMovies] = useState([]);
  const [genres, setGenres] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const [selectedGenre, setSelectedGenre] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState('rating');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadGenres();
  }, []);

  useEffect(() => {
    loadMovies();
  }, [page, selectedGenre, sortBy]);

  const loadGenres = async () => {
    try {
      const res = await movieApi.getGenres();
      setGenres(res.data || []);
    } catch (err) {
      console.error('Failed to load genres:', err);
    }
  };

  const loadMovies = async () => {
    setLoading(true);
    try {
      const params = {
        page,
        per_page: 16,
        genre: selectedGenre !== 'All' ? selectedGenre : undefined,
        search: searchQuery.trim() || undefined,
        sort_by: sortBy,
      };
      const res = await movieApi.getMovies(params);
      setMovies(res.data.movies || []);
      setTotalPages(res.data.total_pages || 1);
      setTotalCount(res.data.total || 0);
    } catch (err) {
      console.error('Failed to load movies:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    setPage(1);
    loadMovies();
  };

  return (
    <div className="space-y-6 pb-16">
      {/* Header & Filter Bar */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 bg-slate-900/80 p-5 rounded-2xl border border-slate-800 shadow-xl">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Movie Catalog</h1>
          <p className="text-xs text-slate-400 mt-1">
            Displaying {totalCount} movies mined and stored in the relational database
          </p>
        </div>

        {/* Filter Controls */}
        <div className="flex flex-wrap items-center gap-3">
          {/* Search Box */}
          <form onSubmit={handleSearch} className="relative min-w-[200px]">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search title..."
              className="w-full pl-9 pr-3 py-2 rounded-xl bg-slate-800 border border-slate-700 text-xs text-white placeholder-slate-400 focus:outline-none focus:border-indigo-500"
            />
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-2.5" />
          </form>

          {/* Genre Dropdown */}
          <div className="flex items-center gap-1.5 bg-slate-800 border border-slate-700 px-3 py-1.5 rounded-xl">
            <Filter className="w-3.5 h-3.5 text-indigo-400" />
            <select
              value={selectedGenre}
              onChange={(e) => {
                setSelectedGenre(e.target.value);
                setPage(1);
              }}
              className="bg-transparent text-xs text-white focus:outline-none cursor-pointer"
            >
              <option value="All" className="bg-slate-900">All Genres</option>
              {genres.map((g) => (
                <option key={g.genre_id} value={g.genre_name} className="bg-slate-900">
                  {g.genre_name}
                </option>
              ))}
            </select>
          </div>

          {/* Sort By Dropdown */}
          <div className="flex items-center gap-1.5 bg-slate-800 border border-slate-700 px-3 py-1.5 rounded-xl">
            <ArrowUpDown className="w-3.5 h-3.5 text-indigo-400" />
            <select
              value={sortBy}
              onChange={(e) => {
                setSortBy(e.target.value);
                setPage(1);
              }}
              className="bg-transparent text-xs text-white focus:outline-none cursor-pointer"
            >
              <option value="rating" className="bg-slate-900">Highest Rated</option>
              <option value="year" className="bg-slate-900">Latest Release</option>
              <option value="title" className="bg-slate-900">Title A-Z</option>
            </select>
          </div>
        </div>
      </div>

      {/* Movies Grid */}
      {loading ? (
        <div className="py-20 text-center text-slate-400 text-sm">
          Loading movies from database...
        </div>
      ) : movies.length === 0 ? (
        <div className="py-20 text-center bg-slate-900/50 rounded-2xl border border-slate-800 p-8">
          <p className="text-slate-300 text-sm font-medium">No movies found matching your filters.</p>
          <button
            onClick={() => {
              setSelectedGenre('All');
              setSearchQuery('');
              setPage(1);
            }}
            className="mt-3 px-4 py-1.5 rounded-lg bg-indigo-600 text-white text-xs font-semibold"
          >
            Reset Filters
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
          {movies.map((m) => (
            <MovieCard
              key={m.movie_id}
              movie={m}
              onSelect={onSelectMovie}
              onRate={onRateMovie}
            />
          ))}
        </div>
      )}

      {/* Pagination Footer */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between bg-slate-900/60 p-4 rounded-xl border border-slate-800">
          <p className="text-xs text-slate-400">
            Page <span className="font-semibold text-white">{page}</span> of{' '}
            <span className="font-semibold text-white">{totalPages}</span>
          </p>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page <= 1}
              className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 disabled:opacity-40 text-xs text-white border border-slate-700 transition-colors"
            >
              <ChevronLeft className="w-3.5 h-3.5" /> Previous
            </button>
            <button
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page >= totalPages}
              className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 disabled:opacity-40 text-xs text-white border border-slate-700 transition-colors"
            >
              Next <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Movies;
