import React from 'react';
import { Star, Clock, Eye, Sparkles } from 'lucide-react';

const MovieCard = ({ movie, onSelect, onRate, matchPercentage, methodTag }) => {
  return (
    <div className="group relative bg-slate-800/90 rounded-xl overflow-hidden border border-slate-700/60 hover:border-indigo-500/60 shadow-lg hover:shadow-indigo-500/10 transition-all duration-300 flex flex-col justify-between">
      <div>
        {/* Poster Container */}
        <div className="relative aspect-[2/3] overflow-hidden bg-slate-900 cursor-pointer" onClick={() => onSelect(movie)}>
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
          <div className="absolute inset-0 bg-gradient-to-t from-slate-900 via-transparent to-transparent opacity-70 group-hover:opacity-40 transition-opacity"></div>

          {/* Rating Badge */}
          <div className="absolute top-2.5 right-2.5 flex items-center gap-1 px-2 py-1 rounded-md bg-slate-900/80 backdrop-blur border border-yellow-500/30 text-yellow-400 text-xs font-bold shadow-md">
            <Star className="w-3.5 h-3.5 fill-yellow-400" />
            <span>{movie.imdb_rating ? movie.imdb_rating.toFixed(1) : 'N/A'}</span>
          </div>

          {/* Match Percentage Badge (if provided) */}
          {matchPercentage !== undefined && (
            <div className="absolute top-2.5 left-2.5 flex items-center gap-1 px-2 py-1 rounded-md bg-indigo-600/90 backdrop-blur text-white text-xs font-bold shadow-lg shadow-indigo-600/40">
              <Sparkles className="w-3 h-3" />
              <span>{matchPercentage}% Match</span>
            </div>
          )}

          {/* Quick Overlay Action */}
          <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity bg-black/40 backdrop-blur-[2px]">
            <span className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-indigo-600 text-white text-xs font-semibold shadow-lg">
              <Eye className="w-4 h-4" /> Quick View
            </span>
          </div>
        </div>

        {/* Content Details */}
        <div className="p-3.5">
          <div className="flex items-center justify-between text-[11px] text-slate-400 mb-1">
            <span>{movie.release_year}</span>
            {movie.duration && (
              <span className="flex items-center gap-1">
                <Clock className="w-3 h-3" /> {movie.duration}m
              </span>
            )}
          </div>

          <h3 
            className="text-sm font-semibold text-white line-clamp-1 group-hover:text-indigo-400 transition-colors cursor-pointer"
            onClick={() => onSelect(movie)}
            title={movie.title}
          >
            {movie.title}
          </h3>

          {/* Genres */}
          <div className="flex flex-wrap gap-1 mt-2">
            {(movie.genres || []).slice(0, 3).map((g) => (
              <span
                key={g}
                className="text-[10px] px-2 py-0.5 rounded bg-slate-700/60 text-slate-300 border border-slate-600/40"
              >
                {g}
              </span>
            ))}
          </div>

          {/* Mining Method Tag */}
          {methodTag && (
            <div className="mt-2 text-[10px] text-indigo-400 font-medium truncate">
              {methodTag}
            </div>
          )}
        </div>
      </div>

      {/* Card Action Buttons */}
      <div className="px-3.5 pb-3.5 pt-1 flex items-center gap-2 border-t border-slate-700/40">
        <button
          onClick={() => onSelect(movie)}
          className="flex-1 py-1.5 px-2 rounded-lg bg-slate-700/50 hover:bg-slate-700 text-xs font-medium text-slate-200 transition-colors text-center"
        >
          Details
        </button>
        {onRate && (
          <button
            onClick={() => onRate(movie)}
            className="py-1.5 px-2.5 rounded-lg bg-indigo-600/20 hover:bg-indigo-600 text-indigo-300 hover:text-white text-xs font-medium border border-indigo-500/30 transition-colors flex items-center gap-1"
          >
            <Star className="w-3 h-3" /> Rate
          </button>
        )}
      </div>
    </div>
  );
};

export default MovieCard;
