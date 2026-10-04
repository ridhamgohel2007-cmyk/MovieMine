import React, { useState, useEffect } from 'react';
import { miningApi } from '../services/api';
import { Network, Play, ArrowRight, Sparkles, TrendingUp } from 'lucide-react';

const AssociationRules = () => {
  const [minSupport, setMinSupport] = useState(0.08);
  const [minConfidence, setMinConfidence] = useState(0.40);
  const [rules, setRules] = useState([]);
  const [running, setRunning] = useState(false);

  useEffect(() => {
    handleMineRules();
  }, []);

  const handleMineRules = async () => {
    setRunning(true);
    try {
      const res = await miningApi.runAssociationRules({
        min_support: minSupport,
        min_confidence: minConfidence,
        min_lift: 1.0,
      });
      setRules(res.data.rules || []);
    } catch (err) {
      console.error('Failed to mine rules:', err);
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="space-y-8 pb-16 text-left">
      {/* Header Banner */}
      <div className="bg-slate-900/90 p-6 sm:p-8 rounded-3xl border border-slate-800 shadow-2xl flex flex-col md:flex-row md:items-center md:justify-between gap-6">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-semibold mb-3 border border-emerald-500/30">
            <Network className="w-3.5 h-3.5" /> Market Basket Pattern Mining
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Movie Co-Viewing Patterns (Apriori)
          </h1>
          <p className="text-xs text-slate-300 mt-1 max-w-xl">
            Discovers movies that users frequently watch together: "If a user liked Movie A, they also liked Movie B".
          </p>
        </div>

        {/* Simple One-Click Run Button */}
        <button
          onClick={handleMineRules}
          disabled={running}
          className="flex items-center gap-2 px-5 py-3 rounded-2xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold shadow-lg shadow-emerald-600/30 transition-all disabled:opacity-50 shrink-0"
        >
          <Play className={`w-4 h-4 fill-white ${running ? 'animate-spin' : ''}`} />
          <span>{running ? 'Mining Patterns...' : 'Mine Movie Patterns'}</span>
        </button>
      </div>

      {/* 30-Second Viva Explanation */}
      <div className="p-4 rounded-2xl bg-emerald-950/40 border border-emerald-500/30 text-xs text-emerald-200 space-y-1">
        <span className="font-bold text-white uppercase text-[10px] bg-emerald-500/30 px-2 py-0.5 rounded mr-2">
          How to explain this in Viva in 30 seconds:
        </span>
        <p className="pt-1">
          "Sir/Ma'am, we applied the Apriori algorithm on user watch histories. Just like supermarket market-basket analysis finds bread + butter, our system discovers which movies co-occur frequently. We measure Support (popularity), Confidence (predictive probability), and Lift (strength over random chance)."
        </p>
      </div>

      {/* 3 Metric Explanations */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 text-xs space-y-1">
          <div className="font-bold text-emerald-400">1. Support (Popularity)</div>
          <p className="text-slate-400">Percentage of all users who watched BOTH movies.</p>
        </div>
        <div className="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 text-xs space-y-1">
          <div className="font-bold text-indigo-400">2. Confidence (Accuracy)</div>
          <p className="text-slate-400">Chance that a viewer of Movie A will also like Movie B.</p>
        </div>
        <div className="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 text-xs space-y-1">
          <div className="font-bold text-yellow-400">3. Lift (Strength)</div>
          <p className="text-slate-400">Lift &gt; 1 means genuine correlation, not just coincidence!</p>
        </div>
      </div>

      {/* Beautiful Rule Cards */}
      <div className="space-y-4">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-emerald-400" />
          Top Discovered Rules ({rules.length} Patterns Found)
        </h3>

        {running ? (
          <div className="py-16 text-center text-slate-400 text-xs">Mining frequent itemsets...</div>
        ) : rules.length === 0 ? (
          <div className="py-16 text-center text-slate-400 text-xs bg-slate-900/40 rounded-2xl border border-slate-800">
            No patterns found at this threshold.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {rules.map((rule, idx) => (
              <div
                key={idx}
                className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-xl space-y-3 hover:border-emerald-500/40 transition-colors"
              >
                {/* Visual Rule Flow */}
                <div className="flex items-center gap-2 text-xs font-bold">
                  <span className="px-3 py-1.5 rounded-xl bg-slate-800 text-white border border-slate-700 truncate max-w-[45%]">
                    {rule.antecedent}
                  </span>
                  <ArrowRight className="w-4 h-4 text-emerald-400 shrink-0" />
                  <span className="px-3 py-1.5 rounded-xl bg-indigo-950/60 text-indigo-300 border border-indigo-500/30 truncate max-w-[45%]">
                    {rule.consequent}
                  </span>
                </div>

                {/* Plain English Meaning */}
                <p className="text-xs text-slate-300 italic leading-relaxed">
                  "{rule.explanation}"
                </p>

                {/* Metric Badges */}
                <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between text-xs font-mono">
                  <span className="text-slate-400">
                    Support: <strong className="text-white">{(rule.support * 100).toFixed(0)}%</strong>
                  </span>
                  <span className="text-slate-400">
                    Confidence: <strong className="text-emerald-400">{(rule.confidence * 100).toFixed(0)}%</strong>
                  </span>
                  <span className="text-slate-400">
                    Lift: <strong className="text-yellow-400">{rule.lift.toFixed(2)}x</strong>
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default AssociationRules;
