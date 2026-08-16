import React, { useState } from 'react';
import { GitCompare } from 'lucide-react';

export default function SiteComparisonPage({ sites = [] }) {
  const [siteAId, setSiteAId] = useState(sites[0]?.id || '');
  const [siteBId, setSiteBId] = useState(sites[1]?.id || '');

  const siteA = sites.find(s => s.id === siteAId) || sites[0];
  const siteB = sites.find(s => s.id === siteBId) || sites[1];

  const compareRows = [
    {
      label: 'Overall Suitability Score',
      valA: `${siteA?.scores?.overall_score || 0} / 100`,
      valB: `${siteB?.scores?.overall_score || 0} / 100`,
      highlightA: (siteA?.scores?.overall_score || 0) > (siteB?.scores?.overall_score || 0)
    },
    {
      label: 'Healthcare Need Score',
      valA: `${siteA?.scores?.healthcare_need_score || 0} / 100`,
      valB: `${siteB?.scores?.healthcare_need_score || 0} / 100`,
      highlightA: (siteA?.scores?.healthcare_need_score || 0) > (siteB?.scores?.healthcare_need_score || 0)
    },
    {
      label: 'Accessibility Score',
      valA: `${siteA?.scores?.accessibility_score || 0} / 100`,
      valB: `${siteB?.scores?.accessibility_score || 0} / 100`,
      highlightA: (siteA?.scores?.accessibility_score || 0) > (siteB?.scores?.accessibility_score || 0)
    },
    {
      label: '5km Catchment Population',
      valA: siteA?.population_5km?.toLocaleString() || '0',
      valB: siteB?.population_5km?.toLocaleString() || '0',
      highlightA: (siteA?.population_5km || 0) > (siteB?.population_5km || 0)
    },
    {
      label: 'Estimated Underserved Population',
      valA: siteA?.estimated_underserved_pop?.toLocaleString() || '0',
      valB: siteB?.estimated_underserved_pop?.toLocaleString() || '0',
      highlightA: (siteA?.estimated_underserved_pop || 0) > (siteB?.estimated_underserved_pop || 0)
    },
    {
      label: 'Emergency Response Transit Time',
      valA: `${siteA?.travel_time_min || 0} mins`,
      valB: `${siteB?.travel_time_min || 0} mins`,
      highlightA: (siteA?.travel_time_min || 0) < (siteB?.travel_time_min || 0)
    },
    {
      label: 'Distance to Nearest Tertiary Hospital',
      valA: `${siteA?.distance_to_nearest_hospital_km || 0} km`,
      valB: `${siteB?.distance_to_nearest_hospital_km || 0} km`,
      highlightA: (siteA?.distance_to_nearest_hospital_km || 0) > (siteB?.distance_to_nearest_hospital_km || 0)
    },
    {
      label: 'Parcel Size',
      valA: `${siteA?.parcel_size_acres || 0} Acres`,
      valB: `${siteB?.parcel_size_acres || 0} Acres`,
      highlightA: (siteA?.parcel_size_acres || 0) > (siteB?.parcel_size_acres || 0)
    },
    {
      label: 'Slope Grade',
      valA: `${siteA?.slope_percent || 0}%`,
      valB: `${siteB?.slope_percent || 0}%`,
      highlightA: (siteA?.slope_percent || 0) < (siteB?.slope_percent || 0)
    },
    {
      label: 'Statutory Eligibility',
      valA: siteA?.scores?.is_eligible ? 'Eligible' : 'Ineligible',
      valB: siteB?.scores?.is_eligible ? 'Eligible' : 'Ineligible',
      highlightA: siteA?.scores?.is_eligible && !siteB?.scores?.is_eligible
    }
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-base font-bold text-white flex items-center gap-2">
          <GitCompare className="w-5 h-5 text-brand-400" />
          <span>Side-by-Side Siting Alternative Comparison</span>
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Compare two candidate locations across all spatial and demographic vectors.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
          <label className="text-xs font-semibold text-slate-400">Select Site Option A:</label>
          <select
            value={siteAId || siteA?.id || ''}
            onChange={(e) => setSiteAId(e.target.value)}
            className="w-full p-2.5 rounded-lg bg-slate-800 border border-slate-700 text-xs text-white"
          >
            {sites.map(s => (
              <option key={s.id} value={s.id}>
                {s.name} ({s.zone})
              </option>
            ))}
          </select>
        </div>

        <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
          <label className="text-xs font-semibold text-slate-400">Select Site Option B:</label>
          <select
            value={siteBId || siteB?.id || ''}
            onChange={(e) => setSiteBId(e.target.value)}
            className="w-full p-2.5 rounded-lg bg-slate-800 border border-slate-700 text-xs text-white"
          >
            {sites.map(s => (
              <option key={s.id} value={s.id}>
                {s.name} ({s.zone})
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="rounded-xl border border-slate-800 bg-slate-900 overflow-hidden shadow-lg">
        <table className="w-full text-left text-xs text-slate-300">
          <thead className="bg-slate-850 text-slate-400 uppercase font-semibold border-b border-slate-800">
            <tr>
              <th className="px-6 py-4">Evaluation Criterion</th>
              <th className="px-6 py-4 text-brand-400">{siteA?.name || 'Site A'}</th>
              <th className="px-6 py-4 text-indigo-400">{siteB?.name || 'Site B'}</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {compareRows.map((row, idx) => (
              <tr key={idx} className="hover:bg-slate-800/40">
                <td className="px-6 py-3.5 font-medium text-slate-200">{row.label}</td>
                <td className={`px-6 py-3.5 font-semibold ${row.highlightA ? 'text-emerald-400 bg-emerald-950/20' : 'text-slate-300'}`}>
                  {row.valA}
                </td>
                <td className={`px-6 py-3.5 font-semibold ${!row.highlightA && row.valA !== row.valB ? 'text-emerald-400 bg-emerald-950/20' : 'text-slate-300'}`}>
                  {row.valB}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}