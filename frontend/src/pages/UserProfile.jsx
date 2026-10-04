import React, { useState, useEffect } from 'react';
import { userApi } from '../services/api';
import { useUser } from '../context/UserContext';
import { 
  User as UserIcon, Mail, Calendar, 
  Layers, BarChart2, Star, Sparkles, Check
} from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, 
  ResponsiveContainer, CartesianGrid, Cell 
} from 'recharts';

const UserProfile = () => {
  const { users, currentUser, switchUser } = useUser();
  const [profile, setProfile] = useState(currentUser);
  const [genrePrefs, setGenrePrefs] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (currentUser?.user_id) {
      loadProfileData(currentUser.user_id);
    }
  }, [currentUser?.user_id]);

  const loadProfileData = async (id) => {
    setLoading(true);
    try {
      const [userRes, prefRes] = await Promise.all([
        userApi.getUserById(id),
        userApi.getUserGenrePreferences(id),
      ]);
      setProfile(userRes.data);
      setGenrePrefs(prefRes.data || []);
    } catch (err) {
      console.error('Failed to load user profile:', err);
    } finally {
      setLoading(false);
    }
  };

  const COLORS = ['#6366f1', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#3b82f6', '#06b6d4'];

  return (
    <div className="space-y-8 pb-16 text-left">
      {/* Top Banner / User Demographics */}
      <div className="bg-slate-900/90 rounded-3xl border border-slate-800 p-6 sm:p-8 shadow-2xl flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="flex items-center gap-5">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-indigo-600 via-purple-600 to-pink-500 flex items-center justify-center text-2xl font-black text-white shadow-xl shadow-indigo-600/30">
            {profile?.name?.charAt(0) || 'U'}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-bold text-white">{profile?.name}</h1>
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 font-semibold">
                User #{profile?.user_id}
              </span>
            </div>
            <div className="flex flex-wrap items-center gap-4 text-xs text-slate-400 mt-2">
              <span className="flex items-center gap-1.5"><Mail className="w-3.5 h-3.5 text-slate-500" /> {profile?.email}</span>
              <span>•</span>
              <span>{profile?.gender}, {profile?.age} years old</span>
              <span>•</span>
              <span className="flex items-center gap-1"><Calendar className="w-3.5 h-3.5 text-slate-500" /> Registered {profile?.created_at ? new Date(profile.created_at).toLocaleDateString() : 'Active'}</span>
            </div>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="flex items-center gap-4 border-t md:border-t-0 md:border-l border-slate-800 pt-4 md:pt-0 md:pl-6 w-full md:w-auto">
          <div className="text-center md:text-right">
            <span className="text-xs text-slate-400">Total Ratings</span>
            <div className="text-xl font-bold text-white">{profile?.ratings_count ?? 0}</div>
          </div>
          <div className="h-8 w-px bg-slate-800"></div>
          <div className="text-center md:text-right">
            <span className="text-xs text-slate-400">Watch History</span>
            <div className="text-xl font-bold text-indigo-400">{profile?.watch_count ?? 0}</div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Assigned K-Means Cluster Segment */}
        <div className="space-y-6">
          <div className="bg-slate-900/90 rounded-2xl border border-slate-800 p-6 shadow-xl space-y-4">
            <div className="flex items-center gap-2 text-indigo-400">
              <Layers className="w-5 h-5" />
              <h3 className="text-base font-bold text-white">Mined Audience Segment</h3>
            </div>
            
            <div className="p-4 rounded-xl bg-indigo-950/30 border border-indigo-500/20">
              <span className="text-[10px] uppercase font-bold text-indigo-400 tracking-wider">
                K-Means Cluster Assignment
              </span>
              <h4 className="text-lg font-bold text-white mt-1">
                {profile?.cluster?.cluster_name || 'Cluster 0: General Audience'}
              </h4>
              <p className="text-xs text-slate-300 mt-2 leading-relaxed">
                {profile?.cluster?.description || 'Classified by K-Means algorithm using normalized user ratings and multi-genre affinity vectors.'}
              </p>
            </div>
          </div>

          {/* Persona Switcher Quick Panel */}
          <div className="bg-slate-900/90 rounded-2xl border border-slate-800 p-6 shadow-xl">
            <h3 className="text-sm font-bold text-white mb-2">Switch Demo Persona</h3>
            <p className="text-xs text-slate-400 mb-4">
              Select different sample users to observe how recommendations and cluster charts dynamically adjust.
            </p>

            <div className="space-y-2 max-h-64 overflow-y-auto pr-1">
              {users.slice(0, 8).map((u) => {
                const isSelected = currentUser?.user_id === u.user_id;
                return (
                  <button
                    key={u.user_id}
                    onClick={() => switchUser(u)}
                    className={`w-full p-2.5 rounded-xl text-left text-xs flex items-center justify-between border transition-all ${
                      isSelected
                        ? 'bg-indigo-600/20 border-indigo-500 text-white font-semibold'
                        : 'bg-slate-800/60 border-slate-700/50 text-slate-300 hover:bg-slate-800'
                    }`}
                  >
                    <div>
                      <div className="text-white">{u.name}</div>
                      <div className="text-[10px] text-slate-400">{u.cluster?.cluster_name || `User #${u.user_id}`}</div>
                    </div>
                    {isSelected && <Check className="w-4 h-4 text-indigo-400" />}
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* Right Column: User Genre Preference Vector Chart */}
        <div className="lg:col-span-2 bg-slate-900/90 rounded-2xl border border-slate-800 p-6 shadow-xl space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div>
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <BarChart2 className="w-5 h-5 text-indigo-400" />
                Mined Genre Preference Vector
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">
                Normalized L1 weights derived from user ratings across movie genres
              </p>
            </div>
            <span className="text-[11px] text-indigo-400 font-semibold bg-indigo-500/10 px-2.5 py-1 rounded-lg border border-indigo-500/20">
              Preference Vector
            </span>
          </div>

          {loading ? (
            <div className="py-24 text-center text-slate-400 text-xs">Computing user preference weights...</div>
          ) : genrePrefs.length === 0 ? (
            <div className="py-24 text-center text-slate-400 text-xs">No genre interactions found yet.</div>
          ) : (
            <div className="h-72 w-full pt-4">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={genrePrefs.slice(0, 10)} margin={{ top: 10, right: 10, left: -20, bottom: 25 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis
                    dataKey="genre"
                    stroke="#94a3b8"
                    fontSize={11}
                    angle={-25}
                    textAnchor="end"
                    interval={0}
                  />
                  <YAxis stroke="#94a3b8" fontSize={11} unit="%" />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '12px' }}
                    formatter={(val) => [`${val}%`, 'Genre Affinity']}
                  />
                  <Bar dataKey="affinity" radius={[6, 6, 0, 0]}>
                    {genrePrefs.slice(0, 10).map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default UserProfile;
