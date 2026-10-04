import React, { useState, useEffect } from 'react';
import { miningApi } from '../services/api';
import AlgorithmFlowDiagram from '../components/AlgorithmFlowDiagram';
import { Network, Play, ArrowUpDown, HelpCircle, ArrowRight, CheckCircle2 } from 'lucide-react';

const AssociationRules = () => {
  const [minSupport, setMinSupport] = useState(0.08);
  const [minConfidence, setMinConfidence] = useState(0.40);
  const [minLift, setMinLift] = useState(1.0);
  const [rules, setRules] = useState([]);
  const [meta, setMeta] = useState(null);
  const [running, setRunning] = useState(false);
  const [sortField, setSortField] = useState('lift');
  const [sortAsc, setSortAsc] = useState(false);

  useEffect(() => {
    handleMineRules();
  }, []);

  const handleMineRules = async () => {
    setRunning(true);
    try {
      const res = await miningApi.runAssociationRules({
        min_support: minSupport,
        min_confidence: minConfidence,
        min_lift: minLift,
      });
      setRules(res.data.rules || []);
      setMeta(res.data);
    } catch (err) {
      console.error('Failed to mine association rules:', err);
    } finally {
      setRunning(false);
    }
  };

  const handleSort = (field) => {
    if (sortField === field) {
      setSortAsc(!sortAsc);
    } else {
      setSortField(field);
      setSortAsc(false);
    }
  };

  const sortedRules = [...rules].sort((a, b) => {
    const valA = a[sortField];
    const valB = b[sortField];
    return sortAsc ? valA - valB : valB - valA;
  });

  return (
    <div className="space-y-8 pb-16 text-left">
      {/* Header & Parameter Controls */}
      <div className="bg-slate-900/90 p-6 sm:p-8 rounded-3xl border border-slate-800 shadow-2xl flex flex-col md:flex-row md:items-center md:justify-between gap-6">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-semibold mb-2 border border-emerald-500/30">
            <Network className="w-3.5 h-3.5" /> Market Basket Analysis & Frequent Patterns
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Apriori Association Rule Mining
          </h1>
          <p className="text-xs text-slate-400 mt-1 max-w-2xl">
            Uncovers hidden movie co-viewing affinities and cross-genre associations mined directly from user watch logs and highly-rated itemsets.
          </p>
        </div>

        {/* Hyperparameter Controls */}
        <div className="flex flex-wrap items-center gap-4 bg-slate-800/80 p-4 rounded-2xl border border-slate-700/80 shrink-0">
          <div>
            <label className="text-[11px] font-semibold text-slate-300 block mb-1">
              Min Support: <span className="text-emerald-400 font-mono">{(minSupport * 100).toFixed(0)}%</span>
            </label>
            <input
              type="range"
              min="0.03"
              max="0.25"
              step="0.01"
              value={minSupport}
              onChange={(e) => setMinSupport(parseFloat(e.target.value))}
              className="w-24 accent-emerald-500 cursor-pointer"
            />
          </div>

          <div>
            <label className="text-[11px] font-semibold text-slate-300 block mb-1">
              Min Confidence: <span className="text-indigo-400 font-mono">{(minConfidence * 100).toFixed(0)}%</span>
            </label>
            <input
              type="range"
              min="0.20"
              max="0.80"
              step="0.05"
              value={minConfidence}
              onChange={(e) => setMinConfidence(parseFloat(e.target.value))}
              className="w-24 accent-indigo-500 cursor-pointer"
            />
          </div>

          <div>
            <label className="text-[11px] font-semibold text-slate-300 block mb-1">
              Min Lift: <span className="text-yellow-400 font-mono">{minLift.toFixed(1)}x</span>
            </label>
            <input
              type="range"
              min="1.0"
              max="3.0"
              step="0.1"
              value={minLift}
              onChange={(e) => setMinLift(parseFloat(e.target.value))}
              className="w-20 accent-yellow-500 cursor-pointer"
            />
          </div>

          <button
            onClick={handleMineRules}
            disabled={running}
            className="flex items-center gap-1.5 px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold shadow-lg shadow-emerald-600/30 transition-all disabled:opacity-50 mt-auto"
          >
            <Play className={`w-3.5 h-3.5 fill-white ${running ? 'animate-spin' : ''}`} />
            <span>{running ? 'Mining...' : 'GENERATE RULES'}</span>
          </button>
        </div>
      </div>

      {/* Academic Algorithm Flow */}
      <AlgorithmFlowDiagram
        algorithmName="Apriori Frequent Itemset & Association Rule Extraction"
        steps={[
          { title: '1. TRANSACTIONS', desc: 'Synthesized baskets of movies rated >= 3.5 or watched per user' },
          { title: '2. ENCODING', desc: 'Applied TransactionEncoder to construct binary incidence matrix' },
          { title: '3. APRIORI PRUNING', desc: `Extracted frequent itemsets satisfying min_support >= ${(minSupport*100).toFixed(0)}%` },
          { title: '4. RULE DERIVATION', desc: `Computed Confidence >= ${(minConfidence*100).toFixed(0)}% and Lift >= ${minLift.toFixed(1)}` },
          { title: '5. OUTPUT', desc: 'Actionable co-preference rules saved to association_rules database table' },
        ]}
      />

      {/* Educational Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 text-xs">
          <div className="flex items-center gap-2 text-emerald-400 font-bold mb-1">
            <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
            <span>Support = P(A ∩ B)</span>
          </div>
          <p className="text-slate-400 leading-relaxed">
            The fraction of total user transaction baskets that contain both movie A and movie B. Measures pattern popularity.
          </p>
        </div>

        <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 text-xs">
          <div className="flex items-center gap-2 text-indigo-400 font-bold mb-1">
            <span className="w-2 h-2 rounded-full bg-indigo-400"></span>
            <span>Confidence = P(B | A)</span>
          </div>
          <p className="text-slate-400 leading-relaxed">
            Conditional probability that a user who watched movie A also watched movie B: <code className="text-slate-200">Support(A∪B) / Support(A)</code>.
          </p>
        </div>

        <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 text-xs">
          <div className="flex items-center gap-2 text-yellow-400 font-bold mb-1">
            <span className="w-2 h-2 rounded-full bg-yellow-400"></span>
            <span>Lift = Confidence / P(B)</span>
          </div>
          <p className="text-slate-400 leading-relaxed">
            Measures how much more often A and B co-occur compared to random independence. Lift &gt; 1 indicates true positive association.
          </p>
        </div>
      </div>

      {/* Rules Table */}
      <div className="bg-slate-900/90 rounded-3xl border border-slate-800 p-6 shadow-xl space-y-4">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <div>
            <h3 className="text-base font-bold text-white">
              Discovered Association Rules ({rules.length} Rules)
            </h3>
            <p className="text-xs text-slate-400">
              Evaluated across {meta?.total_transactions || 120} active user transaction baskets
            </p>
          </div>
          <span className="text-xs text-slate-400">Click column header to sort</span>
        </div>

        {running ? (
          <div className="py-20 text-center text-slate-400 text-xs">Running Apriori frequent itemsets extraction...</div>
        ) : sortedRules.length === 0 ? (
          <div className="py-20 text-center bg-slate-900/40 rounded-2xl border border-slate-800 p-8">
            <p className="text-sm font-semibold text-slate-300">No rules met the selected threshold.</p>
            <p className="text-xs text-slate-400 mt-1">Try lowering the Minimum Support or Minimum Confidence slider above.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400 font-semibold uppercase text-[10px]">
                  <th className="pb-3 px-3">#</th>
                  <th className="pb-3 px-3">Antecedent (If User Likes...)</th>
                  <th className="pb-3 px-3 text-center">Direction</th>
                  <th className="pb-3 px-3">Consequent (...Then User Likes)</th>
                  <th
                    className="pb-3 px-3 text-center cursor-pointer hover:text-white"
                    onClick={() => handleSort('support')}
                  >
                    <span className="inline-flex items-center gap-1">
                      Support <ArrowUpDown className="w-3 h-3" />
                    </span>
                  </th>
                  <th
                    className="pb-3 px-3 text-center cursor-pointer hover:text-white"
                    onClick={() => handleSort('confidence')}
                  >
                    <span className="inline-flex items-center gap-1">
                      Confidence <ArrowUpDown className="w-3 h-3" />
                    </span>
                  </th>
                  <th
                    className="pb-3 px-3 text-center cursor-pointer hover:text-white"
                    onClick={() => handleSort('lift')}
                  >
                    <span className="inline-flex items-center gap-1">
                      Lift <ArrowUpDown className="w-3 h-3" />
                    </span>
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-slate-300">
                {sortedRules.map((rule, idx) => (
                  <tr key={idx} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-3 px-3 font-mono text-slate-500">{idx + 1}</td>
                    <td className="py-3 px-3 font-semibold text-white">{rule.antecedent}</td>
                    <td className="py-3 px-3 text-center text-slate-500">
                      <ArrowRight className="w-3.5 h-3.5 mx-auto text-indigo-400" />
                    </td>
                    <td className="py-3 px-3 font-semibold text-indigo-300">{rule.consequent}</td>
                    <td className="py-3 px-3 text-center font-mono font-medium">
                      {(rule.support * 100).toFixed(1)}%
                    </td>
                    <td className="py-3 px-3 text-center font-mono font-bold text-emerald-400">
                      {(rule.confidence * 100).toFixed(1)}%
                    </td>
                    <td className="py-3 px-3 text-center font-mono font-black text-yellow-400">
                      {rule.lift.toFixed(2)}x
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default AssociationRules;
