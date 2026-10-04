import React, { useState, useEffect } from 'react';
import { movieApi, recommendationApi, ratingApi } from '../services/api';
import { useUser } from '../context/UserContext';
import MovieCard from '../components/MovieCard';
import AlgorithmFlowDiagram from '../components/AlgorithmFlowDiagram';
import { 
  Star, Clock, Globe, Calendar, ArrowLeft, 
  Sparkles, CheckCircle, Plus, Eye
} from 'lucide-react';

const MovieDetail = ({ movie, onBack, onSelectMovie, onRateMovie }) => {
  const { currentUser } = useUser();
  const [details, setDetails] = useState(movie);
  const [similarMovies, setSimilarMovies] = useState([]);
  const [loadingSimilar, setLoadingSimilar] = useState(false);
  const [historyAdded, setHistoryAdded] = useState(false);

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
      console.error('Failed to load movie details:', err);
    }
  };

  const loadSimilarMovies = async (id) => {
    setLoadingSimilar(true);
    try {
      const res = await recommendationApi.getContentBased({ movie_id: id, top_n: 6 });
      setSimilarMovies(res.data || []);
    } catch (err) {
      console.error('Failed to load similar movies:', err);
    } finally {
      setLoadingSimilar(false);
    }
  };

  const handleAddWatchHistory = async () => {
    if (!currentUser || !details) return;
    try {
      await ratingApi.addWatchHistory({
        user_id: currentUser.user_id,
        movie_id: details.movie_id,
      });
      setHistoryAdded(true);
      setTimeout(() => setHistoryAdded(false), 2500);
    } catch (err) {
      console.error('Failed to add watch history:', err);
    }
  };

  if (!details) return null;

  return (
    <div className="space-y-8 pb-16">
      {/* Back Button */}
      <button
        onClick={onBack}
        className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-300 border border-slate-700 transition-colors"
      >
        <ArrowLeft className="w-3.5 h-3.5" /> Back
      </button>

      {/* Hero Movie Details Banner */}
      <div className="relative rounded-3xl overflow-hidden bg-slate-900 border border-slate-800 shadow-2xl">
        <div className="p-6 sm:p-10 flex flex-col md:flex-row gap-8 items-start">
          {/* Movie Poster */}
          <div className="w-48 sm:w-60 shrink-0 aspect-[2/3] rounded-2xl overflow-hidden shadow-2xl border border-slate-700 bg-slate-950">
            <img
              src={details.poster_url || 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=600&q=80'}
              alt={details.title}
              className="w-full h-full object-cover"
            />
          </div>

          {/* Details Content */}
          <div className="flex-1 space-y-4 text-left">
            <div>
              <div className="flex flex-wrap items-center gap-2 mb-2">
                <span className="px-2.5 py-0.5 rounded-md bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 text-xs font-semibold">
                  Movie #{details.movie_id}
                </span>
                <span className="text-xs text-slate-400">•</span>
                <span className="text-xs text-slate-300">{details.language || 'English'}</span>
              </div>
              <h1 className="text-3xl sm:text-4xl font-black text-white tracking-tight">
                {details.title}
              </h1>
            </div>

            {/* Quick Metadata Badges */}
            <div className="flex flex-wrap items-center gap-4 text-xs text-slate-300 pt-1">
              <span className="flex items-center gap-1.5 bg-slate-800/80 px-3 py-1.5 rounded-xl border border-slate-700">
                <Calendar className="w-3.5 h-3.5 text-indigo-400" /> {details.release_year}
              </span>
              <span className="flex items-center gap-1.5 bg-slate-800/80 px-3 py-1.5 rounded-xl border border-slate-700">
                <Clock className="w-3.5 h-3.5 text-indigo-400" /> {details.duration} mins
              </span>
              <span className="flex items-center gap-1.5 bg-yellow-500/10 px-3 py-1.5 rounded-xl border border-yellow-500/30 text-yellow-400 font-bold">
                <Star className="w-3.5 h-3.5 fill-yellow-400" /> IMDb {details.imdb_rating} / 10
              </span>
              {details.user_avg_rating !== undefined && (
                <span className="flex items-center gap-1.5 bg-indigo-500/10 px-3 py-1.5 rounded-xl border border-indigo-500/30 text-indigo-300 font-semibold">
                  Mined Avg: {details.user_avg_rating} ★ ({details.user_ratings_count} votes)
                </span>
              )}
            </div>

            {/* Genres */}
            <div className="flex flex-wrap gap-2 pt-1">
              {(details.genres || []).map((g) => (
                <span
                  key={g}
                  className="px-3 py-1 rounded-lg bg-slate-800 text-slate-200 text-xs font-medium border border-slate-700"
                >
                  {g}
                </span>
              ))}
            </div>

            {/* Synopsis */}
            <div className="pt-2">
              <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Overview / Synopsis</h3>
              <p className="text-sm text-slate-300 leading-relaxed max-w-3xl">
                {details.description || 'No overview available for this title in the database.'}
              </p>
            </div>

            {/* Action Buttons */}
            <div className="pt-4 flex flex-wrap items-center gap-3">
              <button
                onClick={() => onRateMovie(details)}
                className="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold shadow-lg shadow-indigo-600/30 transition-all flex items-center gap-2"
              >
                <Star className="w-4 h-4" /> Rate This Movie
              </button>

              <button
                onClick={handleAddWatchHistory}
                disabled={historyAdded}
                className={`px-4 py-2.5 rounded-xl border text-xs font-semibold transition-all flex items-center gap-2 ${
                  historyAdded
                    ? 'bg-emerald-500/20 border-emerald-500/40 text-emerald-300'
                    : 'bg-slate-800 hover:bg-slate-700 border-slate-700 text-slate-200'
                }`}
              >
                {historyAdded ? (
                  <>
                    <CheckCircle className="w-4 h-4 text-emerald-400" /> Added to Watch History
                  </>
                ) : (
                  <>
                    <Plus className="w-4 h-4" /> Add to Watch History
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Data Mining Academic Flow Breakdown */}
      <AlgorithmFlowDiagram
        algorithmName="Content-Based Filtering & Cosine Vector Space Model"
        steps={[
          { title: '1. INPUT', desc: `Target: "${details.title}", Genres: ${details.genres?.join(', ')}` },
          { title: '2. PREPROCESSING', desc: 'Constructed text soup, applied TF-IDF unigram & bigram matrix' },
          { title: '3. ALGORITHM', desc: 'Calculated Cosine Similarity matrix between TF-IDF document vectors' },
          { title: '4. OUTPUT', desc: 'Ranked top-6 closest geometric vector neighbors' },
          { title: '5. INTERPRETATION', desc: 'High cosine scores indicate high thematic & genre correspondence' },
        ]}
      />

      {/* Similar Movies Section (Content-Based) */}
      <div className="space-y-4 text-left">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-indigo-400" /> Content-Based Similar Movies
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Ranked by Cosine Similarity using TF-IDF genre and synopsis vector space
            </p>
          </div>
        </div>

        {loadingSimilar ? (
          <div className="py-12 text-center text-slate-400 text-xs">Computing cosine similarity vectors...</div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-4">
            {similarMovies.map((m) => (
              <MovieCard
                key={m.movie_id}
                movie={m}
                onSelect={onSelectMovie}
                onRate={onRateMovie}
                matchPercentage={m.match_percentage}
                methodTag={`${m.match_percentage}% Similarity`}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default MovieDetail;
