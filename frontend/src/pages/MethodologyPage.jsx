import React from 'react';
import { BookOpen } from 'lucide-react';

export default function MethodologyPage() {
  const steps = [
    {
      title: "1. Spatial Ingestion & Cadastral Sieve",
      desc: "Parcels and spatial coordinates are indexed into spatial memory using geodesic Haversine matrices and bounding boxes."
    },
    {
      title: "2. Statutory Hard Constraint Gating",
      desc: "Critical exclusions (Water body buffer less than 150m, Eco-sensitive zones less than 500m, floodplains, and parcels under 3 Acres) are audited. Violating sites receive an immediate ineligibility flag."
    },
    {
      title: "3. Multi-Factor Metric Normalization",
      desc: "Raw GIS metrics (catchment population within 2/5/10 km, distance to major arterial roads, slope grade, travel times) are scaled to continuous [0, 100] domain values."
    },
    {
      title: "4. Multi-Criteria Decision Analysis (AHP Weighted Sum)",
      desc: "Normalized scores combine linearly with user-configured policy weights (Need 30%, Accessibility 25%, Land Suitability 20%, Gap Deficit 15%, Environmental Safety 10%)."
    },
    {
      title: "5. Grounded Explainable Recommendation",
      desc: "A deterministic natural language synthesis engine generates transparent audit trails explaining exactly why a site was prioritized."
    }
  ];

  return (
    <div className="space-y-6 max-w-4xl">
      <div>
        <h2 className="text-base font-bold text-white flex items-center gap-2">
          <BookOpen className="w-5 h-5 text-brand-400" />
          <span>Scientific Methodology &amp; Decision Flow</span>
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Mathematical formulation of the Multi-Criteria Decision Analysis (MCDA) framework.
        </p>
      </div>

      <div className="space-y-4">
        {steps.map((s, idx) => (
          <div
            key={idx}
            className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-1.5 shadow-md"
          >
            <h3 className="text-sm font-bold text-brand-400">{s.title}</h3>
            <p className="text-xs text-slate-300 leading-relaxed">{s.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}