import React, { useState, useEffect } from 'react';
import { userApi } from '../services/api';
import { useUser } from '../context/UserContext';
import { Star, Clock, Film, Plus } from 'lucide-react';

const MyRatings = ({ onSelectMovie, onRateMovie, setActiveTab }) => {
  const { currentUser } = useUser();
  const [ratings, setRatings] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (currentUser?.user_id) {
      loadRatings(currentUser.user_id);
    }
  }, [currentUser?.user_id]);

  const loadRatings = async (userId) => {
    setLoading(true);
    try {
      const res = await userApi.getUserRatings(userId);
      setRatings(res.data || []);
    } catch (err) {
      console.error('Failed to load user ratings:', err);
    } finally {
      setLoading(false);
    }
  };

  const avgRating = ratings.length > 0
    ? (ratings.reduce((acc, curr) => acc + curr.rating, 0) / ratings.length).toFixed(2)
    : '0.0';

  return (
    <div className="space-y-6 pb-16 text-left">
      {/* Header */}
      <div className="bg-slate-900/90 p-6 rounded-3xl border border-slate-800 shadow-xl flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">My Rating History</h1>
          <p className="text-xs text-slate-400 mt-1">
            Ratings entered for <span className="text-indigo-400 font-semibold">{currentUser?.name}</span> (User #{currentUser?.user_id})
          </p>
        </div>

        <div className="flex items-center gap-4">
          <div className="text-right">
            <span className="text-xs text-slate-400">Total Rated</span>
            <div className="text-xl font-bold text-white">{ratings.length}</div>
          </div>
          <div className="h-8 w-px bg-slate-800"></div>
          <div className="text-right">
            <span className="text-xs text-slate-400">Average Given</span>
            <div className="text-xl font-bold text-yellow-400 flex items-center gap-1 justify-end">
              <Star className="w-4 h-4 fill-yellow-400" /> {avgRating}
            </div>
          </div>
        </div>
      </div>

      {/* Ratings List */}
      {loading ? (
        <div className="py-20 text-center text-slate-400 text-xs">Loading ratings history...</div>
      ) : ratings.length === 0 ? (
        <div className="py-20 text-center bg-slate-900/40 rounded-2xl border border-slate-800 p-8">
          <Film className="w-12 h-12 text-slate-600 mx-auto mb-3" />
          <p className="text-sm font-semibold text-slate-300">No ratings recorded for this user yet.</p>
          <p className="text-xs text-slate-400 mt-1 mb-4">Rate movies in the catalog to build your preference vector.</p>
          <button
            onClick={() => setActiveTab('movies')}
            className="px-4 py-2 rounded-xl bg-indigo-600 text-white text-xs font-semibold shadow-lg shadow-indigo-600/30"
          >
            Browse Movies to Rate
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          {ratings.map((r) => (
            <div
              key={r.rating_id}
              className="p-4 rounded-2xl bg-slate-800/80 border border-slate-700/60 shadow-lg flex items-center justify-between gap-3 hover:border-slate-600 transition-colors"
            >
              <div className="flex items-center gap-3 overflow-hidden">
                <img
                  src={r.movie_poster || 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=600&q=80'}
                  alt={r.movie_title}
                  className="w-12 h-16 object-cover rounded-lg shrink-0 bg-slate-900"
                />
                <div className="overflow-hidden">
                  <h4 className="text-xs font-semibold text-white truncate" title={r.movie_title}>
                    {r.movie_title}
                  </h4>
                  <p className="text-[11px] text-slate-400 mt-0.5">
                    {r.rating_date ? new Date(r.rating_date).toLocaleDateString() : 'Recent'}
                  </p>
                </div>
              </div>

              <div className="text-right shrink-0">
                <span className="flex items-center gap-1 text-sm font-bold text-yellow-400 bg-yellow-500/10 border border-yellow-500/20 px-2.5 py-1 rounded-lg">
                  <Star className="w-3.5 h-3.5 fill-yellow-400" />
                  {r.rating.toFixed(1)}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MyRatings;
