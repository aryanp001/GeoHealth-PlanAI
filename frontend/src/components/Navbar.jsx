import React from 'react';
import { Building2, Sparkles, Layers, ShieldCheck } from 'lucide-react';

export default function Navbar({ onOpenAI, activeRegion = "Nagpur Metropolitan Region, MH" }) {
  return (
    <header className="h-16 border-b border-slate-800 bg-slate-900/90 backdrop-blur px-6 flex items-center justify-between sticky top-0 z-40">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-lg bg-gradient-to-tr from-brand-600 to-emerald-500 flex items-center justify-center shadow-lg shadow-brand-600/20">
          <Building2 className="w-6 h-6 text-white" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-base font-bold text-white tracking-tight">
              GeoHealth PlanAI
            </h1>
            <span className="px-2 py-0.5 text-[10px] font-bold uppercase rounded bg-brand-500/20 text-brand-400 border border-brand-500/30">
              SIH 2026 MVP
            </span>
          </div>
          <p className="text-xs text-slate-400 flex items-center gap-1 mt-0.5">
            <Layers className="w-3 h-3 text-slate-400" />
            <span>Active Region:</span>
            <span className="text-slate-300 font-medium">{activeRegion}</span>
          </p>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <div className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-800/80 border border-slate-700/60 text-xs text-slate-300">
          <ShieldCheck className="w-4 h-4 text-emerald-400" />
          <span>Spatial MCDA Engine Active</span>
        </div>
        <button
          type="button"
          onClick={onOpenAI}
          className="flex items-center gap-2 px-4 py-2 rounded-lg bg-gradient-to-r from-brand-600 to-indigo-600 hover:from-brand-500 hover:to-indigo-500 text-white text-xs font-semibold shadow-md shadow-brand-600/25 transition-all"
        >
          <Sparkles className="w-4 h-4 text-amber-300 animate-pulse" />
          <span>AI Planning Assistant</span>
        </button>
      </div>
    </header>
  );
}