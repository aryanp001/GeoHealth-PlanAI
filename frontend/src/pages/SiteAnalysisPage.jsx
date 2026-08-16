import React from 'react';
import MapView from '../components/MapView';
import ScoreBadge from '../components/ScoreBadge';
import { Users, Car, Building, Trees, CheckCircle2, XCircle } from 'lucide-react';

export default function SiteAnalysisPage({
  sites = [],
  hospitals = [],
  selectedSite = null,
  onSelectSite
}) {
  const currentSite = selectedSite || sites[0];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-base font-bold text-white">
          Comprehensive GIS Parcel Analysis
        </h2>
        <p className="text-xs text-slate-400 mt-0.5">
          Detailed metric breakdown across accessibility, demography, and constraints.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 h-[520px]">
          <MapView
            sites={sites}
            hospitals={hospitals}
            selectedSite={currentSite}
            onSelectSite={onSelectSite}
          />
        </div>

        {/* Site Metric Inspector */}
        <div className="p-6 rounded-xl bg-slate-900 border border-slate-800 space-y-5 overflow-y-auto max-h-[520px]">
          <div className="border-b border-slate-800 pb-4">
            <span className="text-xs font-semibold text-brand-400 uppercase">
              Parcel Deep-Dive
            </span>
            <h3 className="text-lg font-bold text-white mt-1">
              {currentSite?.name || "No Site Selected"}
            </h3>
            <div className="flex items-center gap-2 mt-2">
              <ScoreBadge
                score={currentSite?.scores?.overall_score || 0}
                isEligible={currentSite?.scores?.is_eligible}
                size="lg"
              />
              <span className="text-xs text-slate-400">
                Rank #{currentSite?.scores?.rank ?? '-'}
              </span>
            </div>
          </div>

          {/* Section A: Population Catchment */}
          <div className="space-y-2 text-xs">
            <div className="font-semibold text-slate-200 flex items-center gap-2">
              <Users className="w-4 h-4 text-emerald-400" />
              <span>A. Population Catchment &amp; Demand</span>
            </div>
            <div className="grid grid-cols-2 gap-2 p-3 rounded-lg bg-slate-850 border border-slate-800 text-slate-300">
              <div>
                2km Core Pop:{" "}
                <span className="text-white font-medium">
                  {currentSite?.population_2km?.toLocaleString() || "0"}
                </span>
              </div>
              <div>
                5km Catchment:{" "}
                <span className="text-white font-medium">
                  {currentSite?.population_5km?.toLocaleString() || "0"}
                </span>
              </div>
              <div className="col-span-2">
                Underserved Pop:{" "}
                <span className="text-amber-400 font-medium">
                  {currentSite?.estimated_underserved_pop?.toLocaleString() || "0"}
                </span>
              </div>
            </div>
          </div>

          {/* Section B: Road Connectivity */}
          <div className="space-y-2 text-xs">
            <div className="font-semibold text-slate-200 flex items-center gap-2">
              <Car className="w-4 h-4 text-blue-400" />
              <span>B. Road Connectivity &amp; Ingress</span>
            </div>
            <div className="grid grid-cols-2 gap-2 p-3 rounded-lg bg-slate-850 border border-slate-800 text-slate-300">
              <div>
                Major Arterial Dist:{" "}
                <span className="text-white font-medium">
                  {currentSite?.distance_to_major_road_km ?? 0} km
                </span>
              </div>
              <div>
                Transit Time:{" "}
                <span className="text-white font-medium">
                  {currentSite?.travel_time_min ?? 0} mins
                </span>
              </div>
              <div className="col-span-2">
                Road Type:{" "}
                <span className="text-white font-medium">
                  {currentSite?.road_type || "N/A"}
                </span>
              </div>
            </div>
          </div>

          {/* Section C: Land Suitability */}
          <div className="space-y-2 text-xs">
            <div className="font-semibold text-slate-200 flex items-center gap-2">
              <Building className="w-4 h-4 text-purple-400" />
              <span>C. Land &amp; Topography Suitability</span>
            </div>
            <div className="grid grid-cols-2 gap-2 p-3 rounded-lg bg-slate-850 border border-slate-800 text-slate-300">
              <div>
                Parcel Area:{" "}
                <span className="text-white font-medium">
                  {currentSite?.parcel_size_acres ?? 0} Acres
                </span>
              </div>
              <div>
                Slope Grade:{" "}
                <span className="text-white font-medium">
                  {currentSite?.slope_percent ?? 0}%
                </span>
              </div>
              <div className="col-span-2">
                Zoning Category:{" "}
                <span className="text-white font-medium">
                  {currentSite?.land_use || "N/A"}
                </span>
              </div>
            </div>
          </div>

          {/* Section D: Environmental Clearance */}
          <div className="space-y-2 text-xs">
            <div className="font-semibold text-slate-200 flex items-center gap-2">
              <Trees className="w-4 h-4 text-emerald-400" />
              <span>D. Environmental Clearance</span>
            </div>
            <div className="grid grid-cols-2 gap-2 p-3 rounded-lg bg-slate-850 border border-slate-800 text-slate-300">
              <div>
                Water Body Dist:{" "}
                <span className="text-white font-medium">
                  {currentSite?.distance_to_water_body_km ?? 0} km
                </span>
              </div>
              <div>
                Protected Zone:{" "}
                <span className="text-white font-medium">
                  {currentSite?.distance_to_protected_zone_km ?? 0} km
                </span>
              </div>
              <div className="col-span-2 flex items-center gap-1.5 mt-1">
                <span>Flood Plain Risk:</span>
                {currentSite?.is_in_flood_zone ? (
                  <span className="text-rose-400 font-semibold flex items-center gap-1">
                    <XCircle className="w-3.5 h-3.5" /> High Risk
                  </span>
                ) : (
                  <span className="text-emerald-400 font-semibold flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5" /> Clear / Safe
                  </span>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}