import React, { useState } from 'react';
import { ChevronRight, Database, Cpu, CheckCircle2, FileText, ArrowRight } from 'lucide-react';

const AlgorithmFlowDiagram = ({ algorithmName, steps }) => {
  const [activeStep, setActiveStep] = useState(0);

  const defaultSteps = [
    { title: '1. INPUT', icon: Database, desc: 'Raw relational database tables (Users, Movies, Ratings, Watch History)' },
    { title: '2. PREPROCESSING', icon: Cpu, desc: 'Deduplication, TF-IDF vectorization, rating normalization, pivot matrix generation' },
    { title: '3. ALGORITHM', icon: Cpu, desc: 'Mathematical modeling (Cosine Sim, K-Means centroids, Apriori frequent itemsets)' },
    { title: '4. OUTPUT', icon: FileText, desc: 'Scored recommendations, user clusters, association rules with support/confidence/lift' },
    { title: '5. INTERPRETATION', icon: CheckCircle2, desc: 'Actionable behavioral insights and personalized recommendation rankings' },
  ];

  const currentSteps = steps || defaultSteps;

  return (
    <div className="bg-slate-900/90 rounded-2xl border border-slate-800 p-5 shadow-xl mb-6">
      <div className="flex items-center justify-between mb-4 border-b border-slate-800 pb-3">
        <div>
          <span className="text-[10px] uppercase font-bold tracking-wider text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded border border-indigo-500/20">
            Academic Data Mining Architecture
          </span>
          <h4 className="text-base font-bold text-white mt-1">
            {algorithmName || 'Knowledge Discovery in Databases (KDD) Pipeline'}
          </h4>
        </div>
        <span className="text-xs text-slate-400">Click any stage to inspect</span>
      </div>

      {/* Pipeline Step Badges */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-2">
        {currentSteps.map((step, idx) => {
          const isSelected = activeStep === idx;
          const Icon = step.icon || Cpu;
          return (
            <button
              key={idx}
              onClick={() => setActiveStep(idx)}
              className={`p-3 rounded-xl border text-left transition-all ${
                isSelected
                  ? 'bg-indigo-600/20 border-indigo-500 text-white shadow-lg shadow-indigo-500/10 scale-[1.02]'
                  : 'bg-slate-800/60 border-slate-700/60 text-slate-400 hover:bg-slate-800 hover:text-slate-200'
              }`}
            >
              <div className="flex items-center justify-between text-xs font-bold mb-1">
                <span>{step.title}</span>
                <Icon className={`w-3.5 h-3.5 ${isSelected ? 'text-indigo-400' : 'text-slate-500'}`} />
              </div>
              <p className="text-[11px] line-clamp-2 leading-relaxed opacity-90">{step.desc}</p>
            </button>
          );
        })}
      </div>

      {/* Selected Step Deep Dive */}
      <div className="mt-4 p-4 rounded-xl bg-slate-800/40 border border-slate-700/50 flex items-start gap-3">
        <div className="w-8 h-8 rounded-lg bg-indigo-500/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400 shrink-0 mt-0.5">
          <ArrowRight className="w-4 h-4" />
        </div>
        <div>
          <h5 className="text-xs font-semibold text-indigo-300 uppercase tracking-wide">
            {currentSteps[activeStep].title} Details & Mathematical Role
          </h5>
          <p className="text-xs text-slate-300 mt-1 leading-relaxed">
            {currentSteps[activeStep].details || currentSteps[activeStep].desc}
          </p>
        </div>
      </div>
    </div>
  );
};

export default AlgorithmFlowDiagram;
