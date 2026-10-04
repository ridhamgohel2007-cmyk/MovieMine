import React, { useState, useEffect } from 'react';
import { movieApi, recommendationApi } from '../services/api';
import MovieCard from '../components/MovieCard';
import { Star, Clock, Calendar, ArrowLeft, Sparkles } from 'lucide-react';

const MovieDetail = ({ movie, onBack, onSelectMovie, onRateMovie }) => {
  const [details, setDetails] = useState(movie);
  const [similarMovies, setSimilarMovies] = useState([]);
  const [loadingSimilar, setLoadingSimilar] = useState(false);

  useEffect(() => {
    if (movie?.movie_id) {
      loadMovieDetails(movie.movie_id);
      loadSimilarMovies(movie.movie_id);
    }
  }, [movie?.movie_id]);

  const loadMovieDetails = async (id) => {
    try {
      const res = await movieApi.getMovieById(id);
      setDetails(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const loadSimilarMovies = async (id) => {
    setLoadingSimilar(true);
    try {
      const res = await recommendationApi.getContentBased({ movie_id: id, top_n: 6 });
      setSimilarMovies(res.data || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingSimilar(false);
    }
  };

  if (!details) return null;

  return (
    <div className="space-y-8 pb-16 text-left">
      {/* Back Button */}
      <button
        onClick={onBack}
        className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-xs font-bold text-slate-300 border border-slate-800 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" /> Back to Movies
      </button>

      {/* Main Details Banner */}
      <div className="relative rounded-3xl overflow-hidden bg-slate-900 border border-slate-800 shadow-2xl p-6 sm:p-10 flex flex-col md:flex-row gap-8 items-start">
        {/* Bold Large Poster */}
        <div className="w-52 sm:w-64 shrink-0 aspect-[2/3] rounded-2xl overflow-hidden shadow-2xl border border-slate-700 bg-slate-950">
          <img
            src={details.poster_url || 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=600&q=80'}
            alt={details.title}
            className="w-full h-full object-cover"
          />
        </div>

        {/* Content */}
        <div className="flex-1 space-y-4">
          <div>
            <h1 className="text-3xl sm:text-4xl font-black text-white tracking-tight">
              {details.title}
            </h1>
            <div className="flex flex-wrap items-center gap-3 text-xs text-slate-400 mt-2">
              <span className="flex items-center gap-1 font-semibold text-slate-300">
                <Calendar className="w-3.5 h-3.5 text-indigo-400" /> {details.release_year}
              </span>
              <span>•</span>
              <span className="flex items-center gap-1 font-semibold text-slate-300">
                <Clock className="w-3.5 h-3.5 text-indigo-400" /> {details.duration} mins
              </span>
              <span>•</span>
              <span className="flex items-center gap-1 px-2.5 py-0.5 rounded-lg bg-yellow-500/10 border border-yellow-500/30 text-yellow-400 font-black">
                <Star className="w-3.5 h-3.5 fill-yellow-400" /> IMDb {details.imdb_rating} / 10
              </span>
            </div>
          </div>

          {/* Genre Badges */}
          <div className="flex flex-wrap gap-1.5 pt-1">
            {(details.genres || []).map((g) => (
              <span
                key={g}
                className="text-xs font-semibold px-3 py-1 rounded-xl bg-slate-800 text-slate-200 border border-slate-700"
              >
                {g}
              </span>
            ))}
          </div>

          {/* Synopsis */}
          <div className="pt-2">
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Overview</h3>
            <p className="text-sm text-slate-300 leading-relaxed max-w-3xl">
              {details.description || 'No overview available for this title.'}
            </p>
          </div>

          {/* Action Button */}
          <div className="pt-4">
            <button
              onClick={() => onRateMovie(details)}
              className="px-6 py-3 rounded-2xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-black shadow-xl shadow-indigo-600/30 transition-all flex items-center gap-2"
            >
              <Star className="w-4 h-4 fill-white" /> Rate This Movie
            </button>
          </div>
        </div>
      </div>

      {/* Similar Movies Section */}
      <section className="space-y-4">
        <h2 className="text-xl font-black text-white flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-indigo-400" />
          Similar Movies
        </h2>

        {loadingSimilar ? (
          <div className="py-12 text-center text-slate-400 text-xs">Loading similar titles...</div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-4">
            {similarMovies.map((m) => (
              <MovieCard
                key={m.movie_id}
                movie={m}
                onSelect={onSelectMovie}
                onRate={onRateMovie}
                matchPercentage={m.match_percentage}
              />
            ))}
          </div>
        )}
      </section>
    </div>
  );
};

export default MovieDetail;
