import React, { useState } from 'react';
import { Star, Film, Sparkles } from 'lucide-react';

const GENRE_GRADIENTS = {
  'Action': 'from-blue-600 via-indigo-900 to-slate-950',
  'Sci-Fi': 'from-cyan-600 via-blue-900 to-slate-950',
  'Drama': 'from-purple-800 via-slate-900 to-slate-950',
  'Comedy': 'from-amber-600 via-orange-950 to-slate-950',
  'Horror': 'from-rose-800 via-zinc-950 to-black',
  'Animation': 'from-pink-600 via-purple-950 to-slate-950',
  'Adventure': 'from-emerald-700 via-teal-950 to-slate-950',
  'Crime': 'from-red-900 via-neutral-950 to-black',
  'Thriller': 'from-violet-900 via-slate-950 to-black',
  'Default': 'from-indigo-700 via-slate-900 to-slate-950',
};

const MovieCard = ({ movie, onSelect, onRate, matchPercentage, methodTag }) => {
  const [imgError, setImgError] = useState(false);

  const primaryGenre = movie.genres?.[0] || 'Default';
  const gradient = GENRE_GRADIENTS[primaryGenre] || GENRE_GRADIENTS['Default'];

  return (
    <div 
      className="group relative bg-slate-900 rounded-2xl overflow-hidden border border-slate-800 hover:border-indigo-500/80 hover:shadow-2xl hover:shadow-indigo-500/25 transition-all duration-300 flex flex-col justify-between cursor-pointer"
      onClick={() => onSelect(movie)}
    >
      <div>
        {/* Bold Large Poster Image */}
        <div className="relative aspect-[2/3] w-full overflow-hidden bg-slate-950 flex items-center justify-center">
          {!imgError && movie.poster_url ? (
            <img
              src={movie.poster_url}
              alt={movie.title}
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              loading="lazy"
              onError={() => setImgError(true)}
            />
          ) : (
            /* Clean Aesthetic Stylized Poster Banner - No duplicate text */
            <div className={`w-full h-full p-4 bg-gradient-to-b ${gradient} flex flex-col items-center justify-center text-center relative overflow-hidden`}>
              <div className="w-14 h-14 rounded-2xl bg-white/10 backdrop-blur-md flex items-center justify-center text-white/90 shadow-xl mb-2">
                <Film className="w-7 h-7" />
              </div>
              <span className="text-xs font-black uppercase tracking-wider text-indigo-300">
                {primaryGenre}
              </span>
              <span className="text-[11px] font-semibold text-slate-400 mt-0.5">
                {movie.release_year}
              </span>
            </div>
          )}

          {/* Top Rating Badge */}
          <div className="absolute top-2.5 right-2.5 flex items-center gap-1 px-2.5 py-1 rounded-xl bg-slate-950/90 backdrop-blur-md border border-yellow-500/40 text-yellow-400 text-xs font-black shadow-lg">
            <Star className="w-3.5 h-3.5 fill-yellow-400" />
            <span>{movie.imdb_rating ? movie.imdb_rating.toFixed(1) : '8.0'}</span>
          </div>

          {/* Match % Badge (for recommendations) */}
          {matchPercentage !== undefined && (
            <div className="absolute top-2.5 left-2.5 px-2.5 py-1 rounded-xl bg-gradient-to-r from-indigo-500 to-pink-500 text-white text-xs font-black shadow-lg shadow-indigo-600/40">
              {matchPercentage}% Match
            </div>
          )}
        </div>

        {/* Card Body: Title, Metadata & Tags (Single place, NO OVERLAPPING) */}
        <div className="p-3.5 text-left space-y-2">
          <div>
            <h3 
              className="text-sm font-bold text-white group-hover:text-indigo-300 transition-colors line-clamp-1"
              title={movie.title}
            >
              {movie.title}
            </h3>
            <div className="flex items-center gap-2 text-[11px] text-slate-400 mt-1 font-medium">
              <span>{movie.release_year}</span>
              {movie.duration && <span>• {movie.duration}m</span>}
              <span className="text-indigo-400">• {primaryGenre}</span>
            </div>
          </div>

          {/* Genre Badges */}
          <div className="flex flex-wrap gap-1">
            {(movie.genres || []).slice(0, 3).map((g) => (
              <span
                key={g}
                className="text-[10px] font-semibold px-2 py-0.5 rounded-md bg-slate-800/80 text-slate-300 border border-slate-700/50"
              >
                {g}
              </span>
            ))}
          </div>

          {methodTag && (
            <div className="text-[10px] font-bold text-indigo-300 bg-indigo-500/10 px-2 py-0.5 rounded-md border border-indigo-500/20 truncate">
              {methodTag}
            </div>
          )}
        </div>
      </div>

      {/* Action Buttons */}
      <div 
        className="px-3.5 pb-3.5 pt-0 flex items-center gap-2"
        onClick={(e) => e.stopPropagation()}
      >
        <button
          onClick={() => onSelect(movie)}
          className="flex-1 py-1.5 px-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-bold text-slate-200 transition-colors text-center"
        >
          Details
        </button>
        {onRate && (
          <button
            onClick={() => onRate(movie)}
            className="py-1.5 px-3 rounded-xl bg-indigo-600/20 hover:bg-indigo-600 text-indigo-300 hover:text-white text-xs font-bold border border-indigo-500/30 transition-colors flex items-center gap-1"
          >
            <Star className="w-3 h-3" /> Rate
          </button>
        )}
      </div>
    </div>
  );
};

export default MovieCard;
