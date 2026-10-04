import React, { useState, useEffect } from 'react';
import { recommendationApi } from '../services/api';
import { useUser } from '../context/UserContext';
import MovieCard from '../components/MovieCard';
import AlgorithmFlowDiagram from '../components/AlgorithmFlowDiagram';
import { Sparkles, Users, Cpu, Layers, HelpCircle, RefreshCw } from 'lucide-react';

const Recommendations = ({ onSelectMovie, onRateMovie }) => {
  const { currentUser } = useUser();
  const [data, setData] = useState({
    hybrid: [],
    collaborative: [],
    content_based: [],
    cluster_popular: [],
  });
  const [activeSubTab, setActiveSubTab] = useState('hybrid');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (currentUser?.user_id) {
      loadRecommendations(currentUser.user_id);
    }
  }, [currentUser?.user_id]);

  const loadRecommendations = async (userId) => {
    setLoading(true);
    try {
      const res = await recommendationApi.getRecommendations(userId, 8);
      setData(res.data);
    } catch (err) {
      console.error('Failed to load recommendations:', err);
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { id: 'hybrid', label: 'Hybrid Model', count: data.hybrid?.length || 0, icon: Sparkles, color: 'text-indigo-400' },
    { id: 'collaborative', label: 'Collaborative Filtering', count: data.collaborative?.length || 0, icon: Users, color: 'text-purple-400' },
    { id: 'content', label: 'Content-Based', count: data.content_based?.length || 0, icon: Cpu, color: 'text-amber-400' },
    { id: 'cluster', label: 'Cluster Popular', count: data.cluster_popular?.length || 0, icon: Layers, color: 'text-emerald-400' },
  ];

  return (
    <div className="space-y-8 pb-16 text-left">
      {/* Header Banner */}
      <div className="bg-slate-900/90 p-6 sm:p-8 rounded-3xl border border-slate-800 shadow-2xl flex flex-col md:flex-row md:items-center md:justify-between gap-6">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-semibold mb-3 border border-indigo-500/30">
            <Sparkles className="w-3.5 h-3.5" /> Recommendation Engine
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Personalized Movie Recommendations
          </h1>
          <p className="text-xs text-slate-400 mt-1 max-w-2xl">
            Currently analyzing preferences for <span className="text-indigo-300 font-semibold">{currentUser?.name}</span> (Age {currentUser?.age}, {currentUser?.gender}).
            {currentUser?.cluster?.cluster_name && (
              <span className="ml-1 text-slate-300">
                Belongs to segment: <span className="text-indigo-400 font-medium">{currentUser.cluster.cluster_name}</span>.
              </span>
            )}
          </p>
        </div>

        <button
          onClick={() => loadRecommendations(currentUser?.user_id)}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-white border border-slate-700 transition-colors shadow-md shrink-0"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Re-compute Models</span>
        </button>
      </div>

      {/* Academic Algorithm Flow */}
      <AlgorithmFlowDiagram
        algorithmName="Multi-Model Hybrid Recommendation Architecture"
        steps={[
          { title: '1. INPUT', desc: 'User ratings, watch logs, movie metadata, and cluster segment' },
          { title: '2. COLLABORATIVE', desc: 'User-User Pearson correlation on mean-centered rating matrix' },
          { title: '3. CONTENT-BASED', desc: 'TF-IDF genre/synopsis vectors compared via Cosine Similarity' },
          { title: '4. HYBRID FUSION', desc: 'Final Score = 0.5*(Collab) + 0.3*(Content) + 0.2*(Popularity)' },
          { title: '5. OUTPUT', desc: 'Ranked candidate list with transparent algorithm attribution' },
        ]}
      />

      {/* Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-3 overflow-x-auto no-scrollbar">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeSubTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveSubTab(tab.id)}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-semibold whitespace-nowrap transition-all ${
                isActive
                  ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/30'
                  : 'bg-slate-800/60 hover:bg-slate-800 text-slate-400 hover:text-white border border-slate-700/50'
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? 'text-white' : tab.color}`} />
              <span>{tab.label}</span>
              <span className={`px-1.5 py-0.5 rounded-full text-[10px] ${
                isActive ? 'bg-white/20 text-white' : 'bg-slate-700 text-slate-300'
              }`}>
                {tab.count}
              </span>
            </button>
          );
        })}
      </div>

      {/* Tab Content Display */}
      {loading ? (
        <div className="py-20 text-center text-slate-400 text-sm">Computing real-time recommendations...</div>
      ) : (
        <div>
          {/* Hybrid Section */}
          {activeSubTab === 'hybrid' && (
            <div className="space-y-4">
              <div className="p-4 rounded-2xl bg-indigo-950/30 border border-indigo-500/20 text-xs text-indigo-300 flex items-start gap-3">
                <HelpCircle className="w-5 h-5 text-indigo-400 shrink-0 mt-0.5" />
                <div>
                  <span className="font-bold">Hybrid Formulation: </span>
                  <code className="text-white font-mono bg-slate-900/60 px-2 py-0.5 rounded ml-1">
                    Score = 0.5 × CollabScore + 0.3 × ContentScore + 0.2 × PopularityScore
                  </code>
                  <p className="mt-1 text-slate-300">
                    Provides maximum recommendation coverage while overcoming the individual cold-start and sparsity limitations of collaborative filtering.
                  </p>
                </div>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
                {data.hybrid.map((m) => (
                  <div key={m.movie_id} className="relative">
                    <MovieCard
                      movie={m}
                      onSelect={onSelectMovie}
                      onRate={onRateMovie}
                      matchPercentage={m.match_percentage}
                      methodTag="Hybrid Filtering"
                    />
                    {m.collab_component !== undefined && (
                      <div className="mt-1 px-2 py-1 rounded bg-slate-900 border border-slate-800 text-[10px] text-slate-400 flex justify-between">
                        <span>Collab: {Math.round(m.collab_component * 100)}%</span>
                        <span>Content: {Math.round(m.content_component * 100)}%</span>
                        <span>Pop: {Math.round(m.popularity_component * 100)}%</span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Collaborative Section */}
          {activeSubTab === 'collaborative' && (
            <div className="space-y-4">
              <div className="p-4 rounded-2xl bg-purple-950/30 border border-purple-500/20 text-xs text-purple-300 flex items-start gap-3">
                <Users className="w-5 h-5 text-purple-400 shrink-0 mt-0.5" />
                <div>
                  <span className="font-bold">Collaborative Filtering (User-Based k-NN): </span>
                  <p className="mt-1 text-slate-300">
                    Recommends movies highly rated by peer users whose historical rating vectors exhibit high Pearson correlation with your preferences.
                  </p>
                </div>
              </div>

              {data.collaborative.length === 0 ? (
                <div className="py-16 text-center text-slate-400 text-xs bg-slate-900/40 rounded-2xl border border-slate-800">
                  No collaborative ratings match yet. Try rating more movies in the catalog to expand your neighbor overlaps.
                </div>
              ) : (
                <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
                  {data.collaborative.map((m) => (
                    <MovieCard
                      key={m.movie_id}
                      movie={m}
                      onSelect={onSelectMovie}
                      onRate={onRateMovie}
                      matchPercentage={m.match_percentage}
                      methodTag={m.predicted_rating ? `Pred. Rating: ${m.predicted_rating} ★` : 'Collaborative'}
                    />
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Content-Based Section */}
          {activeSubTab === 'content' && (
            <div className="space-y-4">
              <div className="p-4 rounded-2xl bg-amber-950/30 border border-amber-500/20 text-xs text-amber-300 flex items-start gap-3">
                <Cpu className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
                <div>
                  <span className="font-bold">Content-Based Vector Space Model: </span>
                  <p className="mt-1 text-slate-300">
                    Calculates TF-IDF cosine similarity against movies you previously rated 3.5+ stars, matching genres, plot themes, and keywords.
                  </p>
                </div>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
                {data.content_based.map((m) => (
                  <MovieCard
                    key={m.movie_id}
                    movie={m}
                    onSelect={onSelectMovie}
                    onRate={onRateMovie}
                    matchPercentage={m.match_percentage}
                    methodTag="TF-IDF Cosine Match"
                  />
                ))}
              </div>
            </div>
          )}

          {/* Cluster-Popular Section */}
          {activeSubTab === 'cluster' && (
            <div className="space-y-4">
              <div className="p-4 rounded-2xl bg-emerald-950/30 border border-emerald-500/20 text-xs text-emerald-300 flex items-start gap-3">
                <Layers className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
                <div>
                  <span className="font-bold">Cluster Persona Popularity: </span>
                  <p className="mt-1 text-slate-300">
                    Highest rated movies within your designated K-Means audience cluster segment.
                  </p>
                </div>
              </div>

              {data.cluster_popular.length === 0 ? (
                <div className="py-16 text-center text-slate-400 text-xs bg-slate-900/40 rounded-2xl border border-slate-800">
                  Run K-Means clustering in the Mining Dashboard to establish audience clusters.
                </div>
              ) : (
                <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
                  {data.cluster_popular.map((m) => (
                    <MovieCard
                      key={m.movie_id}
                      movie={m}
                      onSelect={onSelectMovie}
                      onRate={onRateMovie}
                      matchPercentage={m.match_percentage}
                      methodTag="Cluster Top Pick"
                    />
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Recommendations;
