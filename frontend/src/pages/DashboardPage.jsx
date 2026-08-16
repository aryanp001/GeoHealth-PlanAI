import React from 'react';
import StatCard from '../components/StatCard';
import MapView from '../components/MapView';
import RankedTable from '../components/RankedTable';
import ScoreBadge from '../components/ScoreBadge';
import { Building2, Users, MapPin, Activity, ShieldAlert, Sparkles, Navigation } from 'lucide-react';

export default function DashboardPage({
  sites = [],
  hospitals = [],
  stats = null,
  selectedSite = null,
  onSelectSite,
  onOpenAI
}) {
  const totalCandidates = stats?.total_candidates ?? sites.length;
  const eligibleSites = stats?.eligible_sites ?? sites.filter(s => s.scores?.is_eligible).length;
  const underservedPop = stats?.total_underserved_population_covered ?? 289000;
  const avgAccScore = stats?.average_accessibility_score ?? 85.7;
  const topSiteName = stats?.top_recommended_site_name 
    ? stats.top_recommended_site_name.split(' ')[0] 
    : (sites[0]?.name?.split(' ')[0] || "None");

  return (
    <div className="space-y-6">
      {/* KPI Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Evaluated Candidate Parcels"
          value={totalCandidates}
          subtitle={`${eligibleSites} passed statutory gates`}
          icon={Building2}
          color="blue"
        />
        <StatCard
          title="Underserved Demographic"
          value={`${(underservedPop / 1000).toFixed(0)}k`}
          subtitle="5km catchment coverage"
          icon={Users}
          color="emerald"
        />
        <StatCard
          title="Average Ingress Transit"
          value="14.2 min"
          subtitle={`Avg score: ${avgAccScore} / 100`}
          icon={Navigation}
          color="purple"
        />
        <StatCard
          title="Top Recommendation"
          value={topSiteName}
          subtitle="Rank #1 MCDA Synthesis"
          icon={Activity}
          color="amber"
        />
      </div>

      {/* Map & Inspector Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 h-[480px]">
          <MapView
            sites={sites}
            hospitals={hospitals}
            selectedSite={selectedSite}
            onSelectSite={onSelectSite}
          />
        </div>

        {/* Selected Candidate Audit Card */}
        <div className="p-5 rounded-xl bg-slate-900 border border-slate-800 flex flex-col justify-between shadow-xl">
          {selectedSite ? (
            <div className="space-y-4">
              <div className="flex items-start justify-between border-b border-slate-800 pb-3">
                <div>
                  <span className="text-[10px] uppercase font-bold tracking-wider text-brand-400">
                    Selected Candidate
                  </span>
                  <h3 className="text-base font-bold text-white mt-0.5">
                    {selectedSite.name}
                  </h3>
                  <p className="text-xs text-slate-400">
                    {selectedSite.zone}
                  </p>
                </div>
                <ScoreBadge
                  score={selectedSite.scores?.overall_score || 0}
                  isEligible={selectedSite.scores?.is_eligible}
                  size="lg"
                />
              </div>

              {selectedSite.scores?.is_eligible ? (
                <div className="p-3 rounded-lg bg-slate-850 border border-slate-800 text-xs space-y-1.5 text-slate-300">
                  <div className="font-semibold text-white flex items-center gap-1.5">
                    <Sparkles className="w-3.5 h-3.5 text-amber-400" />
                    <span>Justification Synthesis:</span>
                  </div>
                  <p className="text-[11px] leading-relaxed text-slate-300">
                    {selectedSite.scores?.explanation || "Evaluation metrics completed."}
                  </p>
                </div>
              ) : (
                <div className="p-4 rounded-lg bg-rose-950/30 border border-rose-800/50 text-xs text-rose-300 space-y-2">
                  <div className="font-bold flex items-center gap-1.5 text-rose-400">
                    <ShieldAlert className="w-4 h-4" />
                    <span>Statutory Constraint Gate Failure</span>
                  </div>
                  <ul className="list-disc pl-4 space-y-1 text-[11px]">
                    {(selectedSite.scores?.ineligibility_reasons || []).map((reason, idx) => (
                      <li key={idx}>{reason}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ) : (
            <div className="h-full flex flex-col items-center justify-center text-center p-6 text-slate-500">
              <MapPin className="w-10 h-10 mb-2 opacity-40" />
              <p className="text-xs">
                Click on any map marker or ranking row to inspect multi-factor suitability audit.
              </p>
            </div>
          )}

          <button
            type="button"
            onClick={onOpenAI}
            className="w-full mt-3 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-white flex items-center justify-center gap-2 border border-slate-700 transition-colors"
          >
            <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
            <span>Audit with AI Assistant</span>
          </button>
        </div>
      </div>

      {/* Ranked Candidate Sites Table */}
      <div className="space-y-3">
        <h2 className="text-sm font-bold text-white uppercase tracking-wider">
          Candidate Site Evaluation Rankings
        </h2>
        <RankedTable
          sites={sites}
          selectedSite={selectedSite}
          onSelectSite={onSelectSite}
        />
      </div>
    </div>
  );
}