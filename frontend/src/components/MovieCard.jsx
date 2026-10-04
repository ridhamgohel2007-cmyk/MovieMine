import React from 'react';
import { Star } from 'lucide-react';

const MovieCard = ({ movie, onSelect, onRate, matchPercentage, methodTag }) => {
  return (
    <div 
      className="group relative bg-slate-900 rounded-2xl overflow-hidden border border-slate-800/80 hover:border-indigo-500/80 hover:shadow-2xl hover:shadow-indigo-500/20 transition-all duration-300 flex flex-col justify-between cursor-pointer"
      onClick={() => onSelect(movie)}
    >
      <div>
        {/* Bold Large Poster */}
        <div className="relative aspect-[2/3] overflow-hidden bg-slate-950">
          <img
            src={movie.poster_url || 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=600&q=80'}
            alt={movie.title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
            loading="lazy"
            onError={(e) => {
              e.target.onerror = null;
              e.target.src = 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=600&q=80';
            }}
          />
          <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/20 to-transparent opacity-80 group-hover:opacity-60 transition-opacity"></div>

          {/* Top Rating Badge */}
          <div className="absolute top-3 right-3 flex items-center gap-1 px-2.5 py-1 rounded-xl bg-slate-950/80 backdrop-blur-md border border-yellow-500/40 text-yellow-400 text-xs font-black shadow-lg">
            <Star className="w-3.5 h-3.5 fill-yellow-400" />
            <span>{movie.imdb_rating ? movie.imdb_rating.toFixed(1) : '7.5'}</span>
          </div>

          {/* Bold Match % Badge */}
          {matchPercentage !== undefined && (
            <div className="absolute top-3 left-3 px-2.5 py-1 rounded-xl bg-gradient-to-r from-indigo-600 to-pink-600 text-white text-xs font-black shadow-lg shadow-indigo-600/40">
              {matchPercentage}% Match
            </div>
          )}

          {/* Bottom Title Overlay inside poster */}
          <div className="absolute bottom-3 left-3 right-3">
            <h3 className="text-sm sm:text-base font-bold text-white line-clamp-1 group-hover:text-indigo-300 transition-colors drop-shadow-md">
              {movie.title}
            </h3>
            <div className="flex items-center gap-2 text-xs text-slate-300 mt-0.5">
              <span>{movie.release_year}</span>
              {movie.duration && <span>• {movie.duration}m</span>}
            </div>
          </div>
        </div>

        {/* Tags & Actions */}
        <div className="p-3.5 space-y-3">
          {/* Genre Badges */}
          <div className="flex flex-wrap gap-1.5">
            {(movie.genres || []).slice(0, 3).map((g) => (
              <span
                key={g}
                className="text-[10px] font-semibold px-2 py-0.5 rounded-lg bg-slate-800 text-slate-300 border border-slate-700/60"
              >
                {g}
              </span>
            ))}
          </div>

          {/* Recommendation Method Badge */}
          {methodTag && (
            <div className="text-[11px] font-bold text-indigo-400 bg-indigo-500/10 px-2 py-1 rounded-lg border border-indigo-500/20 truncate">
              {methodTag}
            </div>
          )}
        </div>
      </div>

      {/* Action Bar */}
      <div 
        className="px-3.5 pb-3.5 pt-1 flex items-center gap-2"
        onClick={(e) => e.stopPropagation()}
      >
        <button
          onClick={() => onSelect(movie)}
          className="flex-1 py-2 px-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-bold text-slate-200 transition-colors"
        >
          View
        </button>
        {onRate && (
          <button
            onClick={() => onRate(movie)}
            className="py-2 px-3.5 rounded-xl bg-indigo-600/20 hover:bg-indigo-600 text-indigo-300 hover:text-white text-xs font-bold border border-indigo-500/30 transition-colors flex items-center gap-1.5"
          >
            <Star className="w-3.5 h-3.5" /> Rate
          </button>
        )}
      </div>
    </div>
  );
};

export default MovieCard;
