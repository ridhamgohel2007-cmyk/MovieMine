import React, { useState, useEffect } from 'react';
import { miningApi } from '../services/api';
import AlgorithmFlowDiagram from '../components/AlgorithmFlowDiagram';
import { 
  Layers, Play, RefreshCw, Users, Star, 
  Award, TrendingUp, Info, HelpCircle
} from 'lucide-react';
import { 
  ScatterChart, Scatter, XAxis, YAxis, Tooltip, 
  ResponsiveContainer, CartesianGrid, Cell, Legend,
  BarChart, Bar
} from 'recharts';

const ClusterAnalysis = () => {
  const [k, setK] = useState(4);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
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

  const CLUSTER_COLORS = ['#6366f1', '#ec4899', '#f59e0b', '#10b981', '#8b5cf6', '#06b6d4', '#f43f5e'];

  return (
    <div className="space-y-8 pb-16 text-left">
      {/* Header & Controls */}
      <div className="bg-slate-900/90 p-6 sm:p-8 rounded-3xl border border-slate-800 shadow-2xl flex flex-col md:flex-row md:items-center md:justify-between gap-6">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-semibold mb-2 border border-indigo-500/30">
            <Layers className="w-3.5 h-3.5" /> Unsupervised Machine Learning
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            K-Means User Preference Clustering
          </h1>
          <p className="text-xs text-slate-400 mt-1 max-w-2xl">
            Partitions the active user base into homogeneous audience segments based on normalized multi-genre rating vectors, activity frequency, and mean rating behaviors.
          </p>
        </div>

        {/* Interactive K Selector and Runner */}
        <div className="flex items-center gap-3 bg-slate-800/80 p-3 rounded-2xl border border-slate-700/80 shrink-0">
          <div className="flex items-center gap-2">
            <label className="text-xs font-semibold text-slate-300 whitespace-nowrap">Clusters (K):</label>
            <select
              value={k}
              onChange={(e) => setK(parseInt(e.target.value, 10))}
              disabled={running}
              className="bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs font-bold text-white focus:outline-none"
            >
              {[2, 3, 4, 5, 6].map((num) => (
                <option key={num} value={num}>K = {num}</option>
              ))}
            </select>
          </div>

          <button
            onClick={() => handleRunClustering(k)}
            disabled={running}
            className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold shadow-lg shadow-indigo-600/30 transition-all disabled:opacity-50"
          >
            <Play className={`w-3.5 h-3.5 fill-white ${running ? 'animate-spin' : ''}`} />
            <span>{running ? 'Clustering...' : 'RUN K-MEANS'}</span>
          </button>
        </div>
      </div>

      {/* Academic Flow Diagram */}
      <AlgorithmFlowDiagram
        algorithmName="K-Means Clustering & Principal Component Analysis (PCA)"
        steps={[
          { title: '1. INPUT', desc: '120 user rating profiles spanning 18 movie genres' },
          { title: '2. PREPROCESSING', desc: 'Aggregated user-genre ratings, L1 normalized, applied StandardScaler' },
          { title: '3. K-MEANS', desc: `Iteratively optimized ${k} centroids minimizing within-cluster sum of squares (WCSS)` },
          { title: '4. 2D PROJECTION', desc: 'Fitted 2-Component PCA to project high-dimensional clusters onto 2D plane' },
          { title: '5. INTERPRETATION', desc: 'Discovered distinct personas: Action & Sci-Fi fans, Drama buffs, etc.' },
        ]}
      />

      {/* Execution Stats Banner */}
      {result && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800">
            <span className="text-[11px] text-slate-400">Total Users Segmented</span>
            <div className="text-xl font-bold text-white mt-0.5">{result.total_users} Users</div>
          </div>
          <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800">
            <span className="text-[11px] text-slate-400">Chosen K</span>
            <div className="text-xl font-bold text-indigo-400 mt-0.5">K = {result.k}</div>
          </div>
          <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800">
            <span className="text-[11px] text-slate-400">Cluster Inertia (WCSS)</span>
            <div className="text-xl font-bold text-pink-400 mt-0.5">{result.inertia}</div>
          </div>
          <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800">
            <span className="text-[11px] text-slate-400">Algorithmic State</span>
            <div className="text-xl font-bold text-emerald-400 mt-0.5">Converged (10 Inits)</div>
          </div>
        </div>
      )}

      {/* 2D PCA Scatter Plot */}
      <div className="bg-slate-900/90 rounded-3xl border border-slate-800 p-6 shadow-xl space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 border-b border-slate-800 pb-3">
          <div>
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-indigo-400" />
              2D Principal Component Projection (PCA)
            </h3>
            <p className="text-xs text-slate-400">
              Dimensionality reduction mapping high-dimensional user vectors into 2D coordinates for visual verification
            </p>
          </div>
          <span className="text-[10px] uppercase font-bold text-indigo-300 bg-indigo-500/10 px-2.5 py-1 rounded border border-indigo-500/20">
            Live Recharts Scatter
          </span>
        </div>

        {running ? (
          <div className="py-24 text-center text-slate-400 text-xs">Computing K-Means centroids and PCA projection...</div>
        ) : (
          <div className="h-80 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: -10 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis type="number" dataKey="x" name="PCA Component 1" stroke="#94a3b8" fontSize={11} />
                <YAxis type="number" dataKey="y" name="PCA Component 2" stroke="#94a3b8" fontSize={11} />
                <Tooltip
                  cursor={{ strokeDasharray: '3 3' }}
                  content={({ payload }) => {
                    if (payload && payload.length) {
                      const data = payload[0].payload;
                      return (
                        <div className="bg-slate-900 border border-slate-700 p-3 rounded-xl shadow-xl text-xs text-white">
                          <p className="font-bold text-indigo-400">{data.name} (User #{data.user_id})</p>
                          <p className="text-slate-300 mt-1">Cluster: <span className="font-semibold">{data.cluster_id}</span></p>
                          <p className="text-slate-400">Avg Rating: {data.avg_rating} ★</p>
                          <p className="text-slate-400">Rated Movies: {data.num_ratings}</p>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Scatter name="Users" data={result?.scatter_points || []}>
                  {(result?.scatter_points || []).map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={CLUSTER_COLORS[entry.cluster_id % CLUSTER_COLORS.length]}
                    />
                  ))}
                </Scatter>
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* Cluster Persona Cards */}
      <div className="space-y-4">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <Users className="w-5 h-5 text-indigo-400" />
          Mined Audience Cluster Characteristics
        </h3>
        <p className="text-xs text-slate-400">
          Characteristics calculated dynamically from actual cluster centroids in the database
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {(result?.clusters || []).map((c, idx) => (
            <div
              key={c.cluster_id}
              className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-xl space-y-3 relative overflow-hidden"
            >
              <div
                className="absolute top-0 left-0 w-2 h-full"
                style={{ backgroundColor: CLUSTER_COLORS[idx % CLUSTER_COLORS.length] }}
              ></div>

              <div className="flex items-center justify-between pl-2">
                <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">
                  Cluster ID #{c.cluster_id}
                </span>
                <span className="text-xs font-bold text-indigo-300 bg-indigo-500/10 px-2 py-0.5 rounded border border-indigo-500/20">
                  {c.user_count} Users ({c.percentage}%)
                </span>
              </div>

              <h4 className="text-base font-bold text-white pl-2">{c.cluster_name}</h4>

              <p className="text-xs text-slate-300 pl-2 leading-relaxed">{c.description}</p>

              <div className="pl-2 pt-2 border-t border-slate-800 flex flex-wrap items-center gap-4 text-xs text-slate-400">
                <span className="flex items-center gap-1 text-yellow-400 font-semibold">
                  <Star className="w-3.5 h-3.5 fill-yellow-400" /> Avg: {c.avg_rating} ★
                </span>
                <span>•</span>
                <span>Avg {c.avg_activity} movies rated</span>
                <span>•</span>
                <span className="text-indigo-400 font-medium">Top: {c.dominant_genres?.slice(0, 2).join(', ')}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ClusterAnalysis;
