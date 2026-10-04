import React, { useState } from 'react';
import { Star, X, CheckCircle2 } from 'lucide-react';
import { ratingApi } from '../services/api';
import { useUser } from '../context/UserContext';

const RatingModal = ({ movie, isOpen, onClose, onRatingSubmitted }) => {
  const { currentUser } = useUser();
  const [rating, setRating] = useState(4.0);
  const [hoverRating, setHoverRating] = useState(0);
  const [submitting, setSubmitting] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  if (!isOpen || !movie) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!currentUser) {
      setErrorMsg('Please select a user first');
      return;
    }

    setSubmitting(true);
    setErrorMsg('');
    try {
      await ratingApi.addRating({
        user_id: currentUser.user_id,
        movie_id: movie.movie_id,
        rating: rating,
      });
      setSuccessMsg(`Rating of ${rating} stars recorded successfully!`);
      setTimeout(() => {
        setSuccessMsg('');
        if (onRatingSubmitted) onRatingSubmitted();
        onClose();
      }, 1200);
    } catch (err) {
      setErrorMsg(err.response?.data?.error || 'Failed to submit rating.');
    } finally {
      setSubmitting(false);
    }
  };

  const stars = [1, 2, 3, 4, 5];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="relative w-full max-w-md bg-slate-900 border border-slate-700/80 rounded-2xl shadow-2xl p-6 text-left">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        <h3 className="text-lg font-bold text-white mb-1">Rate Movie</h3>
        <p className="text-xs text-slate-400 mb-4">
          Rating as <span className="text-indigo-400 font-semibold">{currentUser?.name}</span> (User #{currentUser?.user_id})
        </p>

        {/* Movie Info Snippet */}
        <div className="flex items-center gap-3 p-3 rounded-xl bg-slate-800/60 border border-slate-700/50 mb-5">
          <img
            src={movie.poster_url || 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=600&q=80'}
            alt={movie.title}
            className="w-12 h-16 object-cover rounded-lg"
          />
          <div>
            <h4 className="text-sm font-semibold text-white line-clamp-1">{movie.title}</h4>
            <p className="text-xs text-slate-400">{movie.release_year} • {movie.genres?.join(', ')}</p>
            <p className="text-xs text-yellow-400 font-medium mt-0.5">IMDb: {movie.imdb_rating} ★</p>
          </div>
        </div>

        {/* Interactive Star Picker */}
        <div className="flex flex-col items-center py-4 bg-slate-800/30 rounded-xl border border-slate-800 mb-4">
          <div className="flex items-center gap-2">
            {stars.map((star) => {
              const active = (hoverRating || rating) >= star;
              return (
                <button
                  key={star}
                  type="button"
                  onClick={() => setRating(star)}
                  onMouseEnter={() => setHoverRating(star)}
                  onMouseLeave={() => setHoverRating(0)}
                  className="p-1 text-2xl transition-transform hover:scale-125 focus:outline-none"
                >
                  <Star
                    className={`w-8 h-8 ${
                      active ? 'text-yellow-400 fill-yellow-400 drop-shadow-[0_0_8px_rgba(250,204,21,0.5)]' : 'text-slate-600'
                    }`}
                  />
                </button>
              );
            })}
          </div>
          <span className="text-sm font-bold text-white mt-2">{rating.toFixed(1)} / 5.0 Stars</span>
        </div>

        {/* Feedback message */}
        {successMsg && (
          <div className="flex items-center gap-2 p-3 mb-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs">
            <CheckCircle2 className="w-4 h-4 shrink-0" />
            <span>{successMsg}</span>
          </div>
        )}
        {errorMsg && (
          <div className="p-3 mb-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs">
            {errorMsg}
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex items-center justify-end gap-2">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            Cancel
          </button>
          <button
            type="button"
            onClick={handleSubmit}
            disabled={submitting}
            className="px-5 py-2 rounded-xl text-xs font-semibold bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg shadow-indigo-600/30 transition-all disabled:opacity-50"
          >
            {submitting ? 'Recording...' : 'Submit Rating'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default RatingModal;
