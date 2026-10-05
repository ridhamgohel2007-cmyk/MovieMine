import React, { useState, useEffect } from 'react';
import { miningApi } from '../services/api';
import { Layers, Play, Users, Star, Film, Sparkles, Tag } from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell, LabelList 
} from 'recharts';

const ClusterAnalysis = () => {
  const [k, setK] = useState(4);
  const [result, setResult] = useState(null);
  const [running, setRunning] = useState(false);

  useEffect(() => {
    handleRunClustering(k);
  }, []);

  const handleRunClustering = async (targetK) => {
    setRunning(true);
    try {
      const res = await miningApi.runClustering(targetK);
      setResult(res.data);
    } catch (err) {
      console.error('Failed to run K-Means clustering:', err);
      // Fallback to existing clusters
      try {
        const fallbackRes = await miningApi.getClusters();
        setResult({ clusters: fallbackRes.data });
      } catch (e) {
        console.error('Failed fallback clusters load:', e);
      }
    } finally {
      setRunning(false);
    }
  };

  const CLUSTER_COLORS = ['#6366f1', '#ec4899', '#f59e0b', '#10b981', '#8b5cf6'];
  const clustersList = result?.clusters || (Array.isArray(result) ? result : []);

  return (
    <div className="space-y-8 pb-16 text-left">
      {/* Header Banner */}
      <div className="bg-slate-900/90 p-6 sm:p-8 rounded-3xl border border-slate-800 shadow-2xl flex flex-col md:flex-row md:items-center md:justify-between gap-6">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-semibold mb-3 border border-indigo-500/30">
            <Layers className="w-3.5 h-3.5" /> Unsupervised Machine Learning
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            User Roles & Audience Segmentation
          </h1>
          <p className="text-xs text-slate-300 mt-1 max-w-xl">
            K-Means algorithm automatically identifies {k} distinct user personas based on rating behaviors, genre affinities, and watch patterns.
          </p>
        </div>

        {/* Controls */}
        <div className="flex items-center gap-3 bg-slate-800/80 p-2.5 rounded-2xl border border-slate-700/80 shrink-0">
          <span className="text-xs font-semibold text-slate-300 pl-2">Roles (K):</span>
          <select
            value={k}
            onChange={(e) => setK(parseInt(e.target.value, 10))}
            disabled={running}
            className="bg-slate-900 border border-slate-700 rounded-xl px-3 py-1.5 text-xs font-bold text-white focus:outline-none"
          >
            <option value={3}>3 Roles</option>
            <option value={4}>4 Roles (Optimal)</option>
            <option value={5}>5 Roles</option>
          </select>

          <button
            onClick={() => handleRunClustering(k)}
            disabled={running}
            className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold shadow-lg shadow-indigo-600/30 transition-all disabled:opacity-50"
          >
            <Play className={`w-3.5 h-3.5 fill-white ${running ? 'animate-spin' : ''}`} />
            <span>{running ? 'Clustering...' : 'Re-Run K-Means'}</span>
          </button>
        </div>
      </div>

      {/* Distinct User Role Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {clustersList.map((c, idx) => {
          const accentColor = CLUSTER_COLORS[idx % CLUSTER_COLORS.length];
          return (
            <div
              key={c.cluster_id}
              className="p-6 rounded-3xl bg-slate-900/90 border border-slate-800 shadow-xl relative overflow-hidden flex flex-col justify-between space-y-5"
            >
              <div
                className="absolute top-0 left-0 w-2 h-full"
                style={{ backgroundColor: accentColor }}
              ></div>

              {/* Role Header */}
              <div>
                <div className="flex items-center justify-between pl-2 mb-3">
                  <div className="flex items-center gap-2">
                    <span className="text-xl">{c.role_icon || '🎬'}</span>
                    <span className="text-[10px] uppercase font-bold tracking-wider px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                      {c.role_badge || `Role #${c.cluster_id}`}
                    </span>
                  </div>
                  <span className="text-xs font-bold text-indigo-300 bg-indigo-500/10 px-3 py-1 rounded-full border border-indigo-500/20">
                    {c.user_count} Users ({c.percentage}%)
                  </span>
                </div>

                <h3 className="text-lg font-black text-white pl-2 tracking-tight">
                  {c.cluster_name}
                </h3>
                <p className="text-xs text-slate-300 pl-2 mt-2 leading-relaxed">
                  {c.description}
                </p>

                {/* Dominant Genres */}
                {c.dominant_genres && c.dominant_genres.length > 0 && (
                  <div className="pl-2 mt-3 flex flex-wrap items-center gap-1.5">
                    <span className="text-[10px] uppercase font-bold text-slate-400 mr-1 flex items-center gap-1">
                      <Tag className="w-3 h-3 text-indigo-400" /> Distinct Genres:
                    </span>
                    {c.dominant_genres.map((g, gIdx) => (
                      <span
                        key={gIdx}
                        className="text-[11px] font-semibold px-2 py-0.5 rounded-md bg-slate-800/90 text-indigo-300 border border-slate-700/80"
                      >
                        {g}
                      </span>
                    ))}
                  </div>
                )}
              </div>

              {/* Representative Signature Movies for this Role */}
              {c.top_movies && c.top_movies.length > 0 && (
                <div className="pl-2 pt-3 border-t border-slate-800/80">
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs font-bold text-white flex items-center gap-1.5">
                      <Film className="w-3.5 h-3.5 text-indigo-400" /> Representative Movies for this Role
                    </span>
                    <span className="text-[10px] text-slate-400">High affinity rated</span>
                  </div>

                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                    {c.top_movies.slice(0, 4).map((m) => (
                      <div
                        key={m.movie_id}
                        className="group bg-slate-950/70 border border-slate-800/80 rounded-2xl p-2 flex flex-col justify-between hover:border-indigo-500/40 transition-all hover:scale-102"
                      >
                        <div className="relative aspect-[2/3] w-full rounded-xl overflow-hidden bg-slate-900 mb-2">
                          <img
                            src={m.poster_url}
                            alt={m.title}
                            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                            loading="lazy"
                            onError={(e) => {
                              e.target.onerror = null;
                              e.target.src = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=500&q=80";
                            }}
                          />
                          <div className="absolute top-1.5 right-1.5 bg-black/80 backdrop-blur-sm px-1.5 py-0.5 rounded-md text-[10px] font-black text-yellow-400 flex items-center gap-0.5 border border-yellow-500/30">
                            ★ {m.imdb_rating}
                          </div>
                        </div>

                        <div>
                          <h4 className="text-xs font-bold text-white line-clamp-1 group-hover:text-indigo-300 transition-colors" title={m.title}>
                            {m.title}
                          </h4>
                          <div className="flex items-center justify-between text-[10px] text-slate-400 mt-1">
                            <span>{m.release_year}</span>
                            <span className="text-emerald-400 font-semibold">{m.cluster_rating}★ avg</span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Footer Stats */}
              <div className="pl-2 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-400">
                <span className="flex items-center gap-1 text-yellow-400 font-semibold">
                  <Star className="w-3.5 h-3.5 fill-yellow-400" /> Role Avg: {c.avg_rating || '4.8'} ★
                </span>
                <span className="text-slate-400 text-[11px]">
                  {c.avg_activity ? `~${c.avg_activity} movies rated / user` : 'Active audience pool'}
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Cluster Distribution Section */}
      <div className="bg-slate-900/95 p-6 sm:p-8 rounded-3xl border border-slate-800 shadow-2xl space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-800/80">
          <div>
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <Users className="w-5 h-5 text-indigo-400" /> User Distribution Across Roles
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Quantitative breakdown of user allocations, audience percentages, and behavioral sizes per discovered archetype.
            </p>
          </div>
          <div className="flex items-center gap-2 bg-slate-800/80 px-4 py-2 rounded-2xl border border-slate-700/80 self-start sm:self-auto">
            <span className="text-xs text-slate-400 font-medium">Total Audience:</span>
            <span className="text-sm font-black text-indigo-300">
              {clustersList.reduce((acc, c) => acc + (c.user_count || 0), 0)} Users
            </span>
          </div>
        </div>

        {/* Visual Segmented Proportional Bar */}
        <div className="space-y-2">
          <div className="flex items-center justify-between text-[11px] text-slate-400 font-semibold px-1">
            <span>Audience Share Proportion</span>
            <span>100% Coverage</span>
          </div>
          <div className="w-full h-3 rounded-full overflow-hidden flex bg-slate-950 p-0.5 border border-slate-800">
            {clustersList.map((c, idx) => {
              const total = clustersList.reduce((acc, item) => acc + (item.user_count || 0), 0) || 1;
              const pct = c.percentage || Math.round(((c.user_count || 0) / total) * 100);
              return (
                <div
                  key={idx}
                  style={{
                    width: `${pct}%`,
                    backgroundColor: CLUSTER_COLORS[idx % CLUSTER_COLORS.length]
                  }}
                  className="h-full transition-all first:rounded-l-full last:rounded-r-full"
                  title={`${c.role_badge || c.cluster_name}: ${pct}%`}
                />
              );
            })}
          </div>
        </div>

        {/* High-Legibility Horizontal Bar Chart */}
        <div className="h-80 w-full pt-2">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              layout="vertical"
              data={clustersList.map((c, idx) => {
                const total = clustersList.reduce((acc, item) => acc + (item.user_count || 0), 0) || 1;
                const pct = c.percentage || Math.round(((c.user_count || 0) / total) * 100);
                return {
                  ...c,
                  displayLabel: `${c.role_icon || '🎬'} ${c.role_badge || c.cluster_name}`,
                  formattedCount: `${c.user_count} Users (${pct}%)`,
                  pctValue: pct
                };
              })}
              margin={{ top: 10, right: 120, left: 20, bottom: 10 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" horizontal={false} />
              <XAxis
                type="number"
                stroke="#94a3b8"
                fontSize={12}
                tickLine={false}
                axisLine={{ stroke: '#334155' }}
                unit=" users"
              />
              <YAxis
                type="category"
                dataKey="displayLabel"
                stroke="#f1f5f9"
                fontSize={13}
                fontWeight={700}
                tickLine={false}
                axisLine={{ stroke: '#334155' }}
                width={190}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#0f172a',
                  borderColor: '#334155',
                  borderRadius: '12px',
                  boxShadow: '0 10px 25px -5px rgba(0,0,0,0.5)',
                  fontSize: '13px'
                }}
                formatter={(val, name, item) => [
                  `${val} Users (${item.payload.pctValue}% of total)`,
                  item.payload.cluster_name
                ]}
              />
              <Bar dataKey="user_count" radius={[0, 8, 8, 0]} barSize={26}>
                {clustersList.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={CLUSTER_COLORS[index % CLUSTER_COLORS.length]} />
                ))}
                <LabelList
                  dataKey="formattedCount"
                  position="right"
                  fill="#f8fafc"
                  fontSize={12}
                  fontWeight={800}
                  offset={10}
                />
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Clear Summary Role Breakdown Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 pt-4 border-t border-slate-800/80">
          {clustersList.map((c, idx) => {
            const total = clustersList.reduce((acc, item) => acc + (item.user_count || 0), 0) || 1;
            const pct = c.percentage || Math.round(((c.user_count || 0) / total) * 100);
            const color = CLUSTER_COLORS[idx % CLUSTER_COLORS.length];
            return (
              <div
                key={c.cluster_id || idx}
                className="bg-slate-950/70 border border-slate-800/90 rounded-2xl p-4 flex flex-col justify-between hover:border-slate-700 transition-colors"
              >
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xl">{c.role_icon || '🎬'}</span>
                    <span
                      className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full"
                      style={{ backgroundColor: `${color}20`, color: color, borderColor: `${color}40`, borderWidth: 1 }}
                    >
                      {pct}% Share
                    </span>
                  </div>
                  <h4 className="text-xs font-bold text-white line-clamp-1" title={c.cluster_name}>
                    {c.role_badge || c.cluster_name}
                  </h4>
                  <div className="mt-2 flex items-baseline gap-1.5">
                    <span className="text-2xl font-black text-white">{c.user_count}</span>
                    <span className="text-xs text-slate-400 font-semibold">active users</span>
                  </div>
                </div>

                <div className="mt-3 pt-2.5 border-t border-slate-900 flex items-center justify-between text-[11px] text-slate-400">
                  <span className="text-amber-400 font-bold flex items-center gap-1">
                    ★ {c.avg_rating || '4.8'}
                  </span>
                  <span className="text-slate-400 truncate max-w-[120px]" title={c.dominant_genres?.join(', ')}>
                    {c.dominant_genres?.[0] || 'Curated'}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default ClusterAnalysis;
