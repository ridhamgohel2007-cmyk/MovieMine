import React from 'react';

const MetricCard = ({ title, value, subtitle, icon: Icon, color = 'indigo' }) => {
  const colorMap = {
    indigo: 'from-indigo-600/20 to-indigo-600/5 text-indigo-400 border-indigo-500/30',
    purple: 'from-purple-600/20 to-purple-600/5 text-purple-400 border-purple-500/30',
    emerald: 'from-emerald-600/20 to-emerald-600/5 text-emerald-400 border-emerald-500/30',
    amber: 'from-amber-600/20 to-amber-600/5 text-amber-400 border-amber-500/30',
    pink: 'from-pink-600/20 to-pink-600/5 text-pink-400 border-pink-500/30',
  };

  const scheme = colorMap[color] || colorMap.indigo;

  return (
    <div className={`relative p-5 rounded-2xl bg-gradient-to-b ${scheme} border shadow-lg backdrop-blur-sm transition-all hover:scale-[1.02]`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs font-medium text-slate-400">{title}</p>
          <h3 className="text-2xl font-bold text-white mt-1">{value}</h3>
          {subtitle && <p className="text-[11px] text-slate-400 mt-1">{subtitle}</p>}
        </div>
        {Icon && (
          <div className="p-3 rounded-xl bg-slate-800/80 border border-slate-700/60 shadow-inner">
            <Icon className="w-6 h-6" />
          </div>
        )}
      </div>
    </div>
  );
};

export default MetricCard;
