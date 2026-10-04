import React, { useState } from 'react';
import { useUser } from '../context/UserContext';
import { Film, Sparkles, Layers, Network, BookOpen, ChevronDown, Check } from 'lucide-react';

const Navbar = ({ activeTab, setActiveTab }) => {
  const { users, currentUser, switchUser } = useUser();
  const [dropdownOpen, setDropdownOpen] = useState(false);

  // 4 Clean, Essential Tabs
  const navTabs = [
    { id: 'recommendations', label: 'Recommendations', icon: Sparkles },
    { id: 'clusters', label: 'Audience Clusters', icon: Layers },
    { id: 'rules', label: 'Movie Patterns', icon: Network },
    { id: 'viva', label: 'Viva Cheat Sheet', icon: BookOpen },
  ];

  // 4 Clear Demo Personas for easy viva demonstration
  const quickPersonas = users.slice(0, 4);

  return (
    <header className="sticky top-0 z-50 bg-slate-950/90 backdrop-blur-md border-b border-slate-800/80">
      <div className="max-w-6xl mx-auto px-4 sm:px-6">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div 
            className="flex items-center gap-2.5 cursor-pointer group"
            onClick={() => setActiveTab('recommendations')}
          >
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-500 to-pink-500 flex items-center justify-center shadow-lg shadow-indigo-500/20 group-hover:scale-105 transition-transform">
              <Film className="w-5 h-5 text-white" />
            </div>
            <div>
              <span className="text-lg font-black tracking-tight text-white">Movie<span className="text-indigo-400">Mine</span></span>
              <span className="hidden sm:inline-block ml-2 text-[10px] uppercase font-bold px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                Data Mining
              </span>
            </div>
          </div>

          {/* Clean 4-Tab Center Navigation */}
          <nav className="hidden md:flex items-center gap-1 bg-slate-900/80 p-1 rounded-xl border border-slate-800">
            {navTabs.map((tab) => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                    isActive
                      ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                      : 'text-slate-400 hover:text-white hover:bg-slate-800/60'
                  }`}
                >
                  <Icon className="w-3.5 h-3.5" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </nav>

          {/* Quick Demo Persona Switcher */}
          <div className="relative">
            <button
              onClick={() => setDropdownOpen(!dropdownOpen)}
              className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 text-left transition-colors"
            >
              <div className="w-6 h-6 rounded-full bg-gradient-to-tr from-indigo-500 to-pink-500 flex items-center justify-center text-[11px] font-bold text-white">
                {currentUser?.name?.charAt(0) || 'U'}
              </div>
              <div className="text-left">
                <div className="text-xs font-bold text-white leading-tight">
                  {currentUser?.name || 'Select User'}
                </div>
                <div className="text-[10px] text-indigo-400">
                  {currentUser?.cluster?.cluster_name?.split(' ')[0] || 'User'} Persona
                </div>
              </div>
              <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
            </button>

            {dropdownOpen && (
              <div className="absolute right-0 mt-2 w-64 rounded-2xl bg-slate-900 border border-slate-800 shadow-2xl p-2 z-50">
                <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider px-2 py-1 mb-1">
                  Switch Persona (For Viva)
                </div>
                <div className="space-y-1">
                  {quickPersonas.map((u) => {
                    const isSelected = currentUser?.user_id === u.user_id;
                    return (
                      <button
                        key={u.user_id}
                        onClick={() => {
                          switchUser(u);
                          setDropdownOpen(false);
                        }}
                        className={`w-full px-3 py-2 rounded-xl text-left text-xs flex items-center justify-between transition-colors ${
                          isSelected
                            ? 'bg-indigo-600/20 text-indigo-300 font-bold border border-indigo-500/30'
                            : 'text-slate-300 hover:bg-slate-800/70'
                        }`}
                      >
                        <div>
                          <div className="text-white">{u.name}</div>
                          <div className="text-[10px] text-slate-400">{u.cluster?.cluster_name || `Cluster Member`}</div>
                        </div>
                        {isSelected && <Check className="w-3.5 h-3.5 text-indigo-400" />}
                      </button>
                    );
                  })}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Mobile Navigation Row */}
        <div className="flex md:hidden items-center justify-around py-2 border-t border-slate-800/80">
          {navTabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-semibold ${
                  isActive ? 'bg-indigo-600 text-white' : 'text-slate-400'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>
      </div>
    </header>
  );
};

export default Navbar;
