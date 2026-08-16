import React from 'react';

export default function StatCard({ title, value, subtitle, icon: Icon, color = "blue" }) {
  const colorMap = {
    blue: "from-blue-500/10 to-transparent border-blue-500/30 text-blue-400",
    emerald: "from-emerald-500/10 to-transparent border-emerald-500/30 text-emerald-400",
    purple: "from-purple-500/10 to-transparent border-purple-500/30 text-purple-400",
    amber: "from-amber-500/10 to-transparent border-amber-500/30 text-amber-400"
  };

  return (
    <div className={`p-4 rounded-xl bg-slate-900 border bg-gradient-to-b ${colorMap[color] || colorMap.blue} flex flex-col justify-between shadow-sm`}>
      <div className="flex items-center justify-between">
        <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">
          {title}
        </span>
        {Icon && <Icon className="w-5 h-5 opacity-80" />}
      </div>
      <div className="mt-2">
        <div className="text-2xl font-bold text-white tracking-tight">
          {value}
        </div>
        {subtitle && (
          <p className="text-xs text-slate-400 mt-1">
            {subtitle}
          </p>
        )}
      </div>
    </div>
  );
}