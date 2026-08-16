import React from 'react';
import ScoreBadge from './ScoreBadge';
import { ChevronRight } from 'lucide-react';

export default function RankedTable({ sites = [], selectedSite, onSelectSite }) {
  return (
    <div className="overflow-x-auto rounded-xl border border-slate-800 bg-slate-900 shadow-md">
      <table className="w-full text-left text-xs text-slate-300">
        <thead className="bg-slate-850 text-slate-400 uppercase font-semibold border-b border-slate-800">
          <tr>
            <th className="px-4 py-3">Rank</th>
            <th className="px-4 py-3">Candidate Site &amp; Zone</th>
            <th className="px-4 py-3 text-center">Score</th>
            <th className="px-4 py-3">5km Catchment</th>
            <th className="px-4 py-3">Travel Time</th>
            <th className="px-4 py-3">Nearest Hospital</th>
            <th className="px-4 py-3">Parcel Area</th>
            <th className="px-4 py-3 text-center">Action</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800">
          {sites.map((site) => {
            const isSelected = selectedSite && selectedSite.id === site.id;
            return (
              <tr
                key={site.id}
                onClick={() => onSelectSite && onSelectSite(site)}
                className={`cursor-pointer transition-colors ${
                  isSelected ? 'bg-brand-950/40 border-l-4 border-brand-500' : 'hover:bg-slate-800/50'
                }`}
              >
                <td className="px-4 py-3 font-bold text-slate-200">
                  {site.scores?.is_eligible ? `#${site.scores?.rank}` : '-'}
                </td>
                <td className="px-4 py-3">
                  <div className="font-semibold text-white">{site.name}</div>
                  <div className="text-[11px] text-slate-400">{site.zone}</div>
                </td>
                <td className="px-4 py-3 text-center">
                  <ScoreBadge
                    score={site.scores?.overall_score || 0}
                    isEligible={site.scores?.is_eligible}
                  />
                </td>
                <td className="px-4 py-3">
                  <span className="font-medium text-slate-200">
                    {site.population_5km?.toLocaleString() || '0'}
                  </span>
                  <span className="text-[10px] text-slate-400 block">
                    Underserved: {site.estimated_underserved_pop?.toLocaleString() || '0'}
                  </span>
                </td>
                <td className="px-4 py-3">
                  <span className="font-medium text-slate-200">
                    {site.travel_time_min} mins
                  </span>
                  <span className="text-[10px] text-slate-400 block">
                    {site.distance_to_major_road_km} km to road
                  </span>
                </td>
                <td className="px-4 py-3">
                  <span className="font-medium text-slate-200">
                    {site.distance_to_nearest_hospital_km} km
                  </span>
                  <span className="text-[10px] text-slate-400 block truncate max-w-[120px]">
                    {site.nearest_hospital_name}
                  </span>
                </td>
                <td className="px-4 py-3">
                  <span className="font-medium text-slate-200">
                    {site.parcel_size_acres} Acres
                  </span>
                  <span className="text-[10px] text-slate-400 block">
                    {site.slope_percent}% Slope
                  </span>
                </td>
                <td className="px-4 py-3 text-center">
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      if (onSelectSite) onSelectSite(site);
                    }}
                    className="p-1.5 rounded-lg bg-slate-800 hover:bg-brand-600 text-slate-300 hover:text-white transition-colors"
                    title="Inspect Site"
                  >
                    <ChevronRight className="w-4 h-4" />
                  </button>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}