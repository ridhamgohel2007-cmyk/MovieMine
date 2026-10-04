import React, { useState } from 'react';
import { useUser } from '../context/UserContext';
import { 
  Film, Sparkles, Layers, Network, 
  BarChart2, User, Star, BookOpen, Compass, ChevronDown
} from 'lucide-react';

const Navbar = ({ activeTab, setActiveTab }) => {
  const { users, currentUser, switchUser } = useUser();
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const navItems = [
    { id: 'home', label: 'Home', icon: Film },
    { id: 'movies', label: 'Movies', icon: Compass },
    { id: 'recommendations', label: 'Recommendations', icon: Sparkles, badge: 'Mined' },
    { id: 'ratings', label: 'My Ratings', icon: Star },
    { id: 'dashboard', label: 'Mining Dashboard', icon: BarChart2, highlight: true },
    { id: 'clusters', label: 'K-Means Clusters', icon: Layers },
    { id: 'association', label: 'Association Rules', icon: Network },
    { id: 'classifier', label: 'Predict Preference', icon: Sparkles },
    { id: 'profile', label: 'Profile', icon: User },
    { id: 'viva', label: 'Viva Guide', icon: BookOpen, accent: true },
  ];

  return (
    <header className="sticky top-0 z-50 bg-slate-900/95 backdrop-blur border-b border-slate-800 shadow-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div 
            className="flex items-center gap-3 cursor-pointer group"
            onClick={() => setActiveTab('home')}
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-purple-600 to-pink-500 flex items-center justify-center shadow-lg shadow-indigo-500/25 group-hover:scale-105 transition-transform">
              <Film className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="text-xl font-bold tracking-tight text-white">Movie<span className="text-indigo-400">Mine</span></span>
                <span className="text-[10px] font-semibold uppercase px-1.5 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">Data Mining</span>
              </div>
              <p className="text-[10px] text-slate-400 -mt-0.5">Recommendation & Preference Mining</p>
            </div>
          </div>

          {/* User Persona Switcher */}
          <div className="relative">
            <button
              onClick={() => setDropdownOpen(!dropdownOpen)}
              className="flex items-center gap-2.5 px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700 text-left transition-colors"
            >
              <div className="w-7 h-7 rounded-full bg-gradient-to-br from-indigo-500 to-pink-500 flex items-center justify-center text-xs font-bold text-white uppercase">
                {currentUser ? currentUser.name.charAt(0) : 'U'}
              </div>
              <div className="hidden sm:block">
                <div className="text-xs font-semibold text-white leading-tight">
                  {currentUser ? currentUser.name : 'Loading User...'}
                </div>
                <div className="text-[10px] text-indigo-400">
                  {currentUser?.cluster?.cluster_name || `User #${currentUser?.user_id || 1}`}
                </div>
              </div>
              <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
            </button>

            {dropdownOpen && (
              <div className="absolute right-0 mt-2 w-72 rounded-xl bg-slate-800 border border-slate-700 shadow-2xl z-50 overflow-hidden">
                <div className="p-3 border-b border-slate-700 bg-slate-800/50">
                  <div className="text-xs font-semibold text-slate-200">Switch Active User Persona</div>
                  <p className="text-[11px] text-slate-400">Test different audience segments and recommendations</p>
                </div>
                <div className="max-h-60 overflow-y-auto divide-y divide-slate-700/50">
                  {users.slice(0, 25).map((u) => (
                    <button
                      key={u.user_id}
                      onClick={() => {
                        switchUser(u);
                        setDropdownOpen(false);
                      }}
                      className={`w-full px-3 py-2 text-left text-xs flex items-center justify-between hover:bg-slate-700/60 transition-colors ${
                        currentUser?.user_id === u.user_id ? 'bg-indigo-600/20 text-indigo-300 font-medium' : 'text-slate-300'
                      }`}
                    >
                      <div>
                        <div>{u.name} <span className="text-[10px] text-slate-400">({u.gender}, {u.age}y)</span></div>
                        <div className="text-[10px] text-slate-400">{u.cluster?.cluster_name || `Cluster Segment`}</div>
                      </div>
                      {currentUser?.user_id === u.user_id && (
                        <span className="w-2 h-2 rounded-full bg-indigo-400"></span>
                      )}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Secondary Navigation Bar */}
        <nav className="flex items-center gap-1 overflow-x-auto py-2 border-t border-slate-800/80 no-scrollbar">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-all ${
                  isActive
                    ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                    : item.highlight
                    ? 'text-indigo-400 hover:text-indigo-300 hover:bg-slate-800/80'
                    : item.accent
                    ? 'text-emerald-400 hover:text-emerald-300 hover:bg-slate-800/80'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`}
              >
                <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-white' : ''}`} />
                <span>{item.label}</span>
                {item.badge && (
                  <span className={`text-[9px] px-1 py-0.2 rounded font-bold uppercase ${
                    isActive ? 'bg-white/20 text-white' : 'bg-indigo-500/20 text-indigo-400'
                  }`}>
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>
      </div>
    </header>
  );
};

export default Navbar;
