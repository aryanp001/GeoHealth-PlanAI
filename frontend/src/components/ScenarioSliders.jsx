import React from 'react';
import { Sliders, RotateCcw, AlertTriangle } from 'lucide-react';

export default function ScenarioSliders({ weights, onChangeWeights, onReset }) {
  const criteria = [
    { key: 'healthcare_need', label: 'Healthcare Need (Population Demand)', default: 30 },
    { key: 'accessibility', label: 'Accessibility & Ingress Connectivity', default: 25 },
    { key: 'land_suitability', label: 'Land Area & Topography Suitability', default: 20 },
    { key: 'healthcare_gap', label: 'Healthcare Infrastructure Gap', default: 15 },
    { key: 'environmental_safety', label: 'Environmental Safety & Buffers', default: 10 },
  ];

  const totalWeight = Object.values(weights).reduce((acc, curr) => acc + Number(curr), 0);

  const handleSliderChange = (key, val) => {
    onChangeWeights({
      ...weights,
      [key]: parseFloat(val)
    });
  };

  return (
    <div className="p-6 rounded-xl bg-slate-900 border border-slate-800 space-y-6 shadow-md">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h2 className="text-base font-bold text-white flex items-center gap-2">
            <Sliders className="w-4 h-4 text-brand-400" />
            <span>MCDA Weight Configuration</span>
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Adjust planning priorities to test policy outcomes. Weights normalize automatically.
          </p>
        </div>
        <button
          onClick={onReset}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-300 transition-colors"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          <span>Reset Defaults</span>
        </button>
      </div>

      <div className="space-y-4">
        {criteria.map((c) => (
          <div key={c.key} className="space-y-1.5">
            <div className="flex items-center justify-between text-xs">
              <span className="font-semibold text-slate-300">{c.label}</span>
              <span className="font-bold text-brand-400">{weights[c.key]}%</span>
            </div>
            <input
              type="range"
              min="0"
              max="100"
              step="5"
              value={weights[c.key]}
              onChange={(e) => handleSliderChange(c.key, e.target.value)}
              className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-brand-500"
            />
          </div>
        ))}
      </div>

      <div className="p-3 rounded-lg bg-slate-850 border border-slate-800 flex items-center justify-between text-xs">
        <span className="text-slate-400">Total Sum:</span>
        <span className={`font-bold ${totalWeight === 100 ? 'text-emerald-400' : 'text-amber-400'}`}>
          {totalWeight}% {totalWeight !== 100 && '(Auto-Normalized on Calculation)'}
        </span>
      </div>

      <div className="flex items-start gap-2 p-3 rounded-lg bg-amber-950/20 border border-amber-800/40 text-[11px] text-amber-300/80">
        <AlertTriangle className="w-4 h-4 flex-shrink-0 mt-0.5 text-amber-400" />
        <span>
          Prototype Baseline Weights: Configured for hackathon sensitivity analysis. Modify sliders to immediately recalculate candidate rankings.
        </span>
      </div>
    </div>
  );
}