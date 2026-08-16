import React from 'react';
import { LayoutDashboard, MapPin, Trophy, GitCompare, Sliders, Database, BookOpen } from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab }) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'analysis', label: 'Site Analysis', icon: MapPin },
    { id: 'ranking', label: 'Rankings', icon: Trophy },
    { id: 'comparison', label: 'Site Comparison', icon: GitCompare },
    { id: 'scenario', label: 'Scenario Weights', icon: Sliders },
    { id: 'datasources', label: 'Data Sources', icon: Database },
    { id: 'methodology', label: 'Methodology', icon: BookOpen },
  ];

  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-900/60 p-4 flex flex-col justify-between hidden md:flex">
      <div className="space-y-1">
        <div className="px-3 py-2 text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
          Decision System
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              type="button"
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-xs font-medium transition-all ${
                isActive
                  ? 'bg-brand-600 text-white shadow-md shadow-brand-600/20'
                  : 'text-slate-300 hover:bg-slate-800/80 hover:text-white'
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400'}`} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </div>

      <div className="p-3 rounded-lg bg-slate-800/40 border border-slate-700/40 text-[11px] text-slate-400">
        <div className="font-semibold text-slate-300 mb-1">Demo Environment</div>
        <p className="leading-relaxed">Nagpur Metropolitan Regional Development Corridor (PMR/NMR).</p>
      </div>
    </aside>
  );
}