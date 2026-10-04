import React, { useState } from 'react';
import { useUser } from '../context/UserContext';
import { Film, Sparkles, Layers, Network, ChevronDown, Check } from 'lucide-react';

const Navbar = ({ activeTab, setActiveTab }) => {
  const { users, currentUser, switchUser } = useUser();
  const [dropdownOpen, setDropdownOpen] = useState(false);

  // 3 Essential, Clean Tabs
  const navTabs = [
    { id: 'browse', label: 'Movies & For You', icon: Sparkles },
    { id: 'clusters', label: 'User Clusters', icon: Layers },
    { id: 'patterns', label: 'Movie Patterns', icon: Network },
  ];

  return (
    <header className="sticky top-0 z-50 bg-slate-950/95 backdrop-blur-md border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div 
            className="flex items-center gap-3 cursor-pointer group"
            onClick={() => setActiveTab('browse')}
          >
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center shadow-lg shadow-indigo-500/25 group-hover:scale-105 transition-transform">
              <Film className="w-5 h-5 text-white" />
            </div>
            <div>
              <span className="text-xl font-black tracking-tight text-white">Movie<span className="text-indigo-400">Mine</span></span>
              <span className="hidden sm:inline-block ml-2 text-[10px] uppercase font-black px-2 py-0.5 rounded-md bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                Data Mining
              </span>
            </div>
          </div>

          {/* 3 Clean Center Tabs */}
          <nav className="hidden sm:flex items-center gap-1 bg-slate-900/90 p-1.5 rounded-2xl border border-slate-800">
            {navTabs.map((tab) => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                    isActive
                      ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/30 scale-102'
                      : 'text-slate-400 hover:text-white hover:bg-slate-800/60'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </nav>

          {/* Active User Persona Pill */}
          <div className="relative">
            <button
              onClick={() => setDropdownOpen(!dropdownOpen)}
              className="flex items-center gap-2.5 px-3 py-1.5 rounded-2xl bg-slate-900 border border-slate-800 hover:border-indigo-500/60 transition-colors shadow-md"
            >
              <div className="w-7 h-7 rounded-xl bg-gradient-to-tr from-indigo-500 to-pink-500 flex items-center justify-center text-xs font-black text-white">
                {currentUser?.name?.charAt(0) || 'U'}
              </div>
              <div className="text-left hidden xs:block">
                <div className="text-xs font-bold text-white leading-tight">
                  {currentUser?.name || 'User'}
                </div>
                <div className="text-[10px] font-semibold text-indigo-400">
                  {currentUser?.cluster?.cluster_name || 'Audience Member'}
                </div>
              </div>
              <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
            </button>

            {dropdownOpen && (
              <div className="absolute right-0 mt-2 w-64 rounded-2xl bg-slate-900 border border-slate-800 shadow-2xl p-2 z-50">
                <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider px-3 py-1.5 mb-1">
                  Switch Active Persona
                </div>
                <div className="space-y-1 max-h-60 overflow-y-auto">
                  {users.slice(0, 8).map((u) => {
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
                            : 'text-slate-300 hover:bg-slate-800'
                        }`}
                      >
                        <div>
                          <div className="text-white font-medium">{u.name}</div>
                          <div className="text-[10px] text-slate-400">{u.cluster?.cluster_name || `User #${u.user_id}`}</div>
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
        <div className="flex sm:hidden items-center justify-around py-2 border-t border-slate-800">
          {navTabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold ${
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
