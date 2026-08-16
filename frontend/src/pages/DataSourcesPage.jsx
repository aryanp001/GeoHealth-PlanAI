import React, { useEffect, useState } from 'react';
import { Database, Layers, CheckCircle2, Link2 } from 'lucide-react';
import { apiService } from '../services/api';

const DEFAULT_SOURCES = [
  {
    category: "Roads & Transportation",
    source_name: "OpenStreetMap (OSM) / Overpass API",
    integration_status: "Mock Spatial Data Active",
    production_connector: "overpass-api.de / OSRM Routing Engine",
    attributes: ["Highway classification", "Lane counts", "Speed profiles", "Access restrictions"],
    data_tier: "Verified Open Source Specification"
  },
  {
    category: "Routing & Isochrones",
    source_name: "openrouteservice / HeiGIT Isochrones",
    integration_status: "Adapter Ready",
    production_connector: "api.openrouteservice.org/v2/isochrones",
    attributes: ["Emergency response isochrones", "15-min catchment", "Congestion weights"],
    data_tier: "API Access to be Configured"
  },
  {
    category: "Demographics & Census",
    source_name: "Census of India Projections (Nagpur 2026)",
    integration_status: "Calibrated Benchmark Data",
    production_connector: "censusindia.gov.in / Smart City Open Data Portal",
    attributes: ["Ward-level population", "Vulnerable demographics", "Underserved ratio"],
    data_tier: "Calibrated Hackathon Benchmark"
  },
  {
    category: "Healthcare Infrastructure",
    source_name: "Ayushman Bharat Digital Mission (ABDM) - HFR",
    integration_status: "Schema Ready",
    production_connector: "hfr.abdm.gov.in/api/v1/facilities",
    attributes: ["Bed capacity", "Specialties offered", "Public/Private ownership", "Emergency units"],
    data_tier: "National Health Stack Interface"
  },
  {
    category: "Land Records & Cadastral Parcels",
    source_name: "Mahabhunaksha / State Cadastral GIS",
    integration_status: "GeoJSON Parcel Fallback Active",
    production_connector: "mahabhunaksha.mahabhumi.gov.in / WFS Service",
    attributes: ["Parcel boundaries", "Ownership classification", "Non-Agriculture (NA) status"],
    data_tier: "Demo Cadastral Polygon Layer"
  },
  {
    category: "Environmental & LULC Layers",
    source_name: "ISRO Bhuvan / NRSC LULC 50K & FSI",
    integration_status: "Mock Spatial Buffers Active",
    production_connector: "bhuvan.nrsc.gov.in/bhuvan_wms.php",
    attributes: ["Eco-sensitive reserves", "Water bodies", "Forest canopy density", "Flood plains"],
    data_tier: "Calibrated Environmental Benchmark"
  }
];

export default function DataSourcesPage() {
  const [sources, setSources] = useState(DEFAULT_SOURCES);

  useEffect(() => {
    apiService.getDataSources()
      .then((data) => {
        if (data && data.length > 0) {
          setSources(data);
        }
      })
      .catch((err) => {
        console.warn('Using default data source catalog:', err.message);
      });
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-base font-bold text-white flex items-center gap-2">
          <Database className="w-5 h-5 text-brand-400" />
          <span>Data Sources &amp; API Integration Readiness</span>
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Transparency registry distinguishing verified open data, production API endpoints, and hackathon calibrated demo datasets.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {sources.map((src, idx) => (
          <div key={idx} className="p-5 rounded-xl bg-slate-900 border border-slate-800 space-y-3 shadow-md">
            <div className="flex items-start justify-between">
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider text-brand-400">
                  {src.category}
                </span>
                <h3 className="text-sm font-bold text-white mt-0.5">{src.source_name}</h3>
              </div>
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-slate-800 text-slate-300 border border-slate-700">
                {src.data_tier}
              </span>
            </div>

            <div className="p-2.5 rounded-lg bg-slate-850 border border-slate-800 text-xs font-mono text-slate-300">
              <span className="text-slate-500 block text-[10px] flex items-center gap-1">
                <Link2 className="w-3 h-3" /> Target Connector:
              </span>
              <span className="text-brand-300 break-all">{src.production_connector}</span>
            </div>

            {src.attributes && (
              <div className="space-y-1.5">
                <span className="text-[11px] font-semibold text-slate-400 flex items-center gap-1">
                  <Layers className="w-3 h-3 text-slate-500" /> Ingested Layer Attributes:
                </span>
                <div className="flex flex-wrap gap-1.5">
                  {src.attributes.map((attr, aIdx) => (
                    <span
                      key={aIdx}
                      className="px-2 py-0.5 rounded bg-slate-800/80 text-[10px] text-slate-300 border border-slate-700/50"
                    >
                      {attr}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}