import React, { useState, useRef, useEffect } from 'react';
import { useUser } from '../context/UserContext';
import { 
  Film, Sparkles, Layers, Network, ChevronDown, Check, Zap, 
  Crown, UserCheck, ShieldCheck, Activity, Compass, Tag
} from 'lucide-react';

const Navbar = ({ activeTab, setActiveTab }) => {
  const { users, currentUser, switchUser } = useUser();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);

  // Close dropdown on outside click
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // 3 Essential Navigation Tabs with dynamic badges
  const navTabs = [
    { 
      id: 'browse', 
      label: 'Movies & For You', 
      icon: Sparkles,
      badge: 'Recs',
      badgeColor: 'bg-indigo-500/20 text-indigo-300 border-indigo-500/30'
    },
    { 
      id: 'clusters', 
      label: 'User Clusters & Roles', 
      icon: Layers,
      badge: '4 Roles',
      badgeColor: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30'
    },
    { 
      id: 'patterns', 
      label: 'Association Patterns', 
      icon: Network,
      badge: '38 Rules',
      badgeColor: 'bg-amber-500/20 text-amber-300 border-amber-500/30'
    },
  ];

  const getRoleIcon = (clusterName) => {
    if (!clusterName) return '🎬';
    if (clusterName.includes('Sci-Fi') || clusterName.includes('Action')) return '🚀';
    if (clusterName.includes('Drama') || clusterName.includes('Critic')) return '🎭';
    if (clusterName.includes('Crime') || clusterName.includes('Mystery') || clusterName.includes('Sleuth')) return '🔍';
    if (clusterName.includes('Animation') || clusterName.includes('Family')) return '🎨';
    if (clusterName.includes('Romance') || clusterName.includes('Musical')) return '💖';
    return '🎬';
  };

  const getRoleBadgeColor = (clusterName) => {
    if (!clusterName) return 'bg-slate-800 text-slate-300 border-slate-700';
    if (clusterName.includes('Sci-Fi') || clusterName.includes('Action')) 
      return 'bg-blue-500/15 text-blue-300 border-blue-500/30';
    if (clusterName.includes('Drama') || clusterName.includes('Critic')) 
      return 'bg-purple-500/15 text-purple-300 border-purple-500/30';
    if (clusterName.includes('Crime') || clusterName.includes('Mystery')) 
      return 'bg-rose-500/15 text-rose-300 border-rose-500/30';
    if (clusterName.includes('Animation') || clusterName.includes('Family')) 
      return 'bg-amber-500/15 text-amber-300 border-amber-500/30';
    return 'bg-indigo-500/15 text-indigo-300 border-indigo-500/30';
  };

  return (
    <header className="sticky top-0 z-50 backdrop-blur-xl bg-slate-950/85 border-b border-slate-800/80 shadow-[0_8px_32px_rgba(0,0,0,0.55)] transition-all">
      {/* Top Luminous Ambient Accent Strip */}
      <div className="h-[2px] w-full bg-gradient-to-r from-transparent via-indigo-500 via-purple-500 to-transparent opacity-80" />


      {/* Main Navigation Bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="flex items-center justify-between h-17">
          
          {/* Brand Logo & Title */}
          <div 
            className="flex items-center gap-3.5 cursor-pointer group select-none"
            onClick={() => setActiveTab('browse')}
          >
            {/* Luminous 3D Glass Emblem */}
            <div className="relative">
              <div className="absolute -inset-1 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 rounded-2xl blur-sm opacity-60 group-hover:opacity-100 transition duration-300"></div>
              <div className="relative w-10.5 h-10.5 rounded-2xl bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-600 flex items-center justify-center shadow-xl shadow-indigo-600/30 group-hover:scale-105 transition-transform duration-300 border border-white/25">
                <Film className="w-5 h-5 text-white drop-shadow-md group-hover:rotate-6 transition-transform" />
              </div>
            </div>

            <div>
              <div className="flex items-center gap-2">
                <span className="text-2xl font-black tracking-tight text-white font-sans">
                  Movie<span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-300 to-pink-400">Mine</span>
                </span>
                <span className="hidden lg:inline-flex items-center gap-1 text-[10px] uppercase font-black px-2 py-0.5 rounded-full bg-indigo-500/15 text-indigo-300 border border-indigo-500/30 shadow-sm">
                  <Activity className="w-3 h-3 text-emerald-400 animate-pulse" />
                  Engine v2.4
                </span>
              </div>
              <p className="text-[10px] font-semibold text-slate-400 tracking-wider uppercase hidden sm:block">
                Predictive Analytics &amp; User Segmentation
              </p>
            </div>
          </div>

          {/* Central Floating Navigation Island */}
          <nav className="hidden md:flex items-center bg-slate-900/90 p-1.5 rounded-full border border-slate-800 shadow-inner backdrop-blur-md">
            {navTabs.map((tab) => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-4.5 py-2 rounded-full text-xs font-bold transition-all duration-300 ${
                    isActive
                      ? 'bg-gradient-to-r from-indigo-600 via-indigo-500 to-purple-600 text-white shadow-lg shadow-indigo-600/35 scale-[1.03] border border-indigo-400/40'
                      : 'text-slate-400 hover:text-white hover:bg-slate-800/60'
                  }`}
                >
                  <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                  <span>{tab.label}</span>
                  <span className={`text-[10px] px-1.5 py-0.2 rounded-full font-extrabold border ${
                    isActive 
                      ? 'bg-white/20 text-white border-white/30' 
                      : tab.badgeColor
                  }`}>
                    {tab.badge}
                  </span>
                </button>
              );
            })}
          </nav>

          {/* User Persona Profile Pill & Switcher */}
          <div className="relative" ref={dropdownRef}>
            <button
              onClick={() => setDropdownOpen(!dropdownOpen)}
              className="flex items-center gap-3 p-1.5 pr-3 rounded-full bg-slate-900/90 border border-slate-800 hover:border-indigo-500/60 transition-all duration-200 shadow-md group hover:bg-slate-800/80"
            >
              {/* Avatar with dynamic role gradient ring */}
              <div className="w-8 h-8 rounded-full p-0.5 bg-gradient-to-tr from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center shrink-0 shadow-sm">
                <div className="w-full h-full rounded-full bg-slate-950 flex items-center justify-center text-xs font-black text-white">
                  {currentUser?.name?.charAt(0) || 'U'}
                </div>
              </div>

              <div className="text-left hidden xs:block">
                <div className="text-xs font-bold text-white flex items-center gap-1.5 leading-tight group-hover:text-indigo-300 transition-colors">
                  <span className="truncate max-w-[110px]">{currentUser?.name || 'User Profile'}</span>
                  <Crown className="w-3 h-3 text-amber-400 shrink-0" />
                </div>
                <div className="text-[10px] font-semibold text-slate-400 flex items-center gap-1 mt-0.5">
                  <span>{getRoleIcon(currentUser?.cluster?.cluster_name)}</span>
                  <span className="truncate max-w-[110px] text-indigo-300">
                    {currentUser?.cluster?.cluster_name?.split(' ')[0] || 'Audience'} Persona
                  </span>
                </div>
              </div>

              <ChevronDown className={`w-3.5 h-3.5 text-slate-400 transition-transform duration-200 ${dropdownOpen ? 'rotate-180 text-indigo-400' : ''}`} />
            </button>

            {/* Persona Switcher Dropdown */}
            {dropdownOpen && (
              <div className="absolute right-0 mt-3 w-80 rounded-3xl bg-slate-900/95 border border-slate-700/80 shadow-[0_20px_60px_rgba(0,0,0,0.8)] p-3 z-50 backdrop-blur-2xl animate-in fade-in zoom-in-95 duration-150">
                <div className="flex items-center justify-between pb-2 mb-2 border-b border-slate-800 px-2">
                  <div className="flex items-center gap-1.5">
                    <UserCheck className="w-4 h-4 text-indigo-400" />
                    <span className="text-xs font-bold text-white">Switch Persona Profile</span>
                  </div>
                  <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                    {users.length} Users Pool
                  </span>
                </div>

                <div className="text-[11px] text-slate-400 px-2 mb-2 leading-relaxed">
                  Switching personas dynamically updates personalized Hybrid &amp; Collaborative filtering recommendations in real-time.
                </div>

                <div className="space-y-1.5 max-h-72 overflow-y-auto pr-1">
                  {users.slice(0, 15).map((u) => {
                    const isSelected = currentUser?.user_id === u.user_id;
                    const uRole = u.cluster?.cluster_name || `Persona #${u.user_id}`;
                    const uIcon = getRoleIcon(u.cluster?.cluster_name);
                    const badgeClass = getRoleBadgeColor(u.cluster?.cluster_name);

                    return (
                      <button
                        key={u.user_id}
                        onClick={() => {
                          switchUser(u);
                          setDropdownOpen(false);
                        }}
                        className={`w-full px-3 py-2.5 rounded-2xl text-left text-xs flex items-center justify-between transition-all ${
                          isSelected
                            ? 'bg-indigo-600/25 text-white font-bold border border-indigo-500/40 shadow-md'
                            : 'text-slate-300 hover:bg-slate-800/80 hover:text-white border border-transparent'
                        }`}
                      >
                        <div className="flex items-center gap-2.5 min-w-0">
                          <span className="text-lg shrink-0 p-1.5 rounded-xl bg-slate-950 border border-slate-800">
                            {uIcon}
                          </span>
                          <div className="truncate">
                            <div className="text-white font-semibold flex items-center gap-1.5 truncate">
                              <span>{u.name}</span>
                              {isSelected && <span className="text-[9px] bg-indigo-500 text-white px-1.5 rounded font-black">Active</span>}
                            </div>
                            <div className="flex items-center gap-1 mt-0.5">
                              <span className={`text-[10px] px-1.5 py-0.2 rounded-md font-semibold border ${badgeClass} truncate max-w-[150px]`}>
                                {uRole}
                              </span>
                            </div>
                          </div>
                        </div>

                        {isSelected ? (
                          <Check className="w-4 h-4 text-emerald-400 shrink-0 ml-2" />
                        ) : (
                          <span className="text-[10px] text-slate-500 font-mono">#{u.user_id}</span>
                        )}
                      </button>
                    );
                  })}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Mobile Navigation Island Bar */}
        <div className="flex md:hidden items-center justify-around py-2.5 border-t border-slate-800/80">
          {navTabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold transition-all ${
                  isActive 
                    ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-md' 
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{tab.label.split(' ')[0]}</span>
              </button>
            );
          })}
        </div>
      </div>
    </header>
  );
};

export default Navbar;
