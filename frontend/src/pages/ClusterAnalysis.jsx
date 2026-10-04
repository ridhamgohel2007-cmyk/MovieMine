import React, { useState, useEffect } from 'react';
import { miningApi } from '../services/api';
import { Layers, Play, Users, Star, Sparkles, CheckCircle2 } from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell 
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
    } finally {
      setRunning(false);
    }
  };

  const CLUSTER_COLORS = ['#6366f1', '#ec4899', '#f59e0b', '#10b981', '#8b5cf6'];

  return (
    <div className="space-y-8 pb-16 text-left">
      {/* Header Banner */}
      <div className="bg-slate-900/90 p-6 sm:p-8 rounded-3xl border border-slate-800 shadow-2xl flex flex-col md:flex-row md:items-center md:justify-between gap-6">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-semibold mb-3 border border-indigo-500/30">
            <Layers className="w-3.5 h-3.5" /> Unsupervised Learning
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            K-Means User Segmentation
          </h1>
          <p className="text-xs text-slate-300 mt-1 max-w-xl">
            Groups all 120 users into {k} natural audience segments based on their rating history across movie genres.
          </p>
        </div>

        {/* Simple Controls */}
        <div className="flex items-center gap-3 bg-slate-800/80 p-2.5 rounded-2xl border border-slate-700/80 shrink-0">
          <span className="text-xs font-semibold text-slate-300 pl-2">Number of Groups (K):</span>
          <select
            value={k}
            onChange={(e) => setK(parseInt(e.target.value, 10))}
            disabled={running}
            className="bg-slate-900 border border-slate-700 rounded-xl px-3 py-1.5 text-xs font-bold text-white focus:outline-none"
          >
            <option value={3}>3 Clusters</option>
            <option value={4}>4 Clusters (Best)</option>
            <option value={5}>5 Clusters</option>
          </select>

          <button
            onClick={() => handleRunClustering(k)}
            disabled={running}
            className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold shadow-lg shadow-indigo-600/30 transition-all disabled:opacity-50"
          >
            <Play className={`w-3.5 h-3.5 fill-white ${running ? 'animate-spin' : ''}`} />
            <span>{running ? 'Running...' : 'Run K-Means'}</span>
          </button>
        </div>
      </div>

      {/* 4 Big Cool Cluster Persona Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {(result?.clusters || []).map((c, idx) => (
          <div
            key={c.cluster_id}
            className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-xl relative overflow-hidden flex flex-col justify-between"
          >
            <div
              className="absolute top-0 left-0 w-2 h-full"
              style={{ backgroundColor: CLUSTER_COLORS[idx % CLUSTER_COLORS.length] }}
            ></div>

            <div>
              <div className="flex items-center justify-between pl-2 mb-2">
                <span className="text-[10px] uppercase font-bold text-slate-400">
                  Cluster #{c.cluster_id}
                </span>
                <span className="text-xs font-bold text-indigo-300 bg-indigo-500/10 px-2.5 py-0.5 rounded-full border border-indigo-500/20">
                  {c.user_count} Users ({c.percentage}%)
                </span>
              </div>

              <h3 className="text-base font-bold text-white pl-2">{c.cluster_name}</h3>
              <p className="text-xs text-slate-300 pl-2 mt-1.5 leading-relaxed">{c.description}</p>
            </div>

            <div className="pl-2 pt-4 mt-4 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-400">
              <span className="flex items-center gap-1 text-yellow-400 font-semibold">
                <Star className="w-3.5 h-3.5 fill-yellow-400" /> Avg: {c.avg_rating} ★
              </span>
              <span className="text-indigo-400 font-medium">
                {c.dominant_genres?.slice(0, 2).join(' • ')}
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Cluster Distribution Bar Chart */}
      <div className="bg-slate-900/90 p-6 rounded-3xl border border-slate-800 shadow-xl space-y-4">
        <h3 className="text-sm font-bold text-white flex items-center gap-2">
          <Users className="w-4 h-4 text-indigo-400" /> User Distribution Across Clusters
        </h3>
        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={result?.clusters || []} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="cluster_name" stroke="#94a3b8" fontSize={11} interval={0} />
              <YAxis stroke="#94a3b8" fontSize={11} unit=" users" />
              <Tooltip
                contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '12px' }}
                formatter={(val) => [`${val} Users`, 'Audience Size']}
              />
              <Bar dataKey="user_count" radius={[6, 6, 0, 0]}>
                {(result?.clusters || []).map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={CLUSTER_COLORS[index % CLUSTER_COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default ClusterAnalysis;
