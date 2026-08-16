import React from 'react';

export default function ScoreBadge({ score = 0, isEligible = true, size = "md" }) {
  if (!isEligible) {
    return (
      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-900/40 text-rose-300 border border-rose-700/50">
        Ineligible
      </span>
    );
  }

  let colorClasses = "bg-emerald-900/40 text-emerald-300 border-emerald-700/50";
  if (score < 60) {
    colorClasses = "bg-amber-900/40 text-amber-300 border-amber-700/50";
  } else if (score < 40) {
    colorClasses = "bg-slate-800 text-slate-300 border-slate-700";
  }

  const sizeClass = size === "lg" 
    ? "text-base px-3 py-1 font-bold" 
    : "text-xs px-2.5 py-0.5 font-semibold";

  return (
    <span className={`inline-flex items-center rounded-full border ${colorClasses}${sizeClass}`}>
      {Number(score).toFixed(1)} / 100
    </span>
  );
}