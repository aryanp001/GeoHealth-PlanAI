import os

files = {
    "package.json": '''{
  "name": "hospital-gis-planning-platform",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "clsx": "^2.1.0",
    "leaflet": "^1.9.4",
    "lucide-react": "^0.359.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-leaflet": "^4.2.1",
    "recharts": "^2.12.3",
    "tailwind-merge": "^2.2.2"
  },
  "devDependencies": {
    "@types/leaflet": "^1.9.8",
    "@types/react": "^18.2.66",
    "@types/react-dom": "^18.2.22",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.19",
    "postcss": "^8.4.38",
    "tailwindcss": "^3.4.1",
    "vite": "^5.1.6"
  }
}''',

    "vite.config.js": '''import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true
  }
});''',

    "tailwind.config.js": '''/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
        slate: {
          850: '#151e2e',
          900: '#0f172a',
          950: '#020617',
        }
      }
    },
  },
  plugins: [],
}''',

    "postcss.config.js": '''export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}''',

    "index.html": '''

  
    
    
    GeoHealth PlanAI - Hospital Infrastructure Siting Platform
  
  
    
    
  
''',

    "src/index.css": '''@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-slate-950 text-slate-100 antialiased font-sans selection:bg-brand-500 selection:text-white;
  }
}

.leaflet-container {
  width: 100%;
  height: 100%;
  border-radius: 0.75rem;
  background-color: #0f172a !important;
}

.leaflet-popup-content-wrapper {
  background-color: #1e293b !important;
  color: #f8fafc !important;
  border-radius: 0.5rem !important;
  border: 1px solid #334155;
}

.leaflet-popup-tip {
  background-color: #1e293b !important;
}''',

    "src/main.jsx": '''import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  
    
  ,
);''',

    "src/services/api.js": '''const API_BASE_URL = 'http://localhost:8000/api';

export const apiService = {
  async getCandidates() {
    const res = await fetch(`${API_BASE_URL}/candidates`);
    if (!res.ok) throw new Error('Failed to fetch candidate sites');
    return res.json();
  },

  async getHospitals() {
    const res = await fetch(`${API_BASE_URL}/hospitals`);
    if (!res.ok) throw new Error('Failed to fetch hospitals');
    return res.json();
  },

  async getStatistics() {
    const res = await fetch(`${API_BASE_URL}/statistics`);
    if (!res.ok) throw new Error('Failed to fetch statistics');
    return res.json();
  },

  async updateScenario(scenarioData) {
    const res = await fetch(`${API_BASE_URL}/scenario`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(scenarioData)
    });
    if (!res.ok) throw new Error('Failed to recalculate scenario');
    return res.json();
  },

  async queryAI(query, siteA = null, siteB = null) {
    const res = await fetch(`${API_BASE_URL}/ai/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, site_id_a: siteA, site_id_b: siteB })
    });
    if (!res.ok) throw new Error('Failed to query AI engine');
    return res.json();
  },

  async getDataSources() {
    const res = await fetch(`${API_BASE_URL}/data-sources`);
    if (!res.ok) throw new Error('Failed to fetch data sources');
    return res.json();
  }
};''',

    "src/components/ScoreBadge.jsx": '''import React from 'react';

export default function ScoreBadge({ score, isEligible = true, size = "md" }) {
  if (!isEligible) {
    return (
      
        Ineligible
      
    );
  }

  let colorClasses = "bg-emerald-900/40 text-emerald-300 border-emerald-700/50";
  if (score < 60) {
    colorClasses = "bg-amber-900/40 text-amber-300 border-amber-700/50";
  } else if (score < 40) {
    colorClasses = "bg-slate-800 text-slate-300 border-slate-700";
  }

  const sizeClass = size === "lg" ? "text-base px-3 py-1 font-bold" : "text-xs px-2.5 py-0.5 font-semibold";

  return (
    
      {score.toFixed(1)} / 100
    
  );
}''',

    "src/components/StatCard.jsx": '''import React from 'react';

export default function StatCard({ title, value, subtitle, icon: Icon, color = "blue" }) {
  const colorMap = {
    blue: "from-blue-500/10 to-transparent border-blue-500/30 text-blue-400",
    emerald: "from-emerald-500/10 to-transparent border-emerald-500/30 text-emerald-400",
    purple: "from-purple-500/10 to-transparent border-purple-500/30 text-purple-400",
    amber: "from-amber-500/10 to-transparent border-amber-500/30 text-amber-400"
  };

  return (
    
      
        {title}
        {Icon && }
      
      
        {value}
        {subtitle && {subtitle}}
      
    
  );
}''',

    "src/components/Navbar.jsx": '''import React from 'react';
import { Building2, Sparkles, Layers, ShieldCheck } from 'lucide-react';

export default function Navbar({ onOpenAI, activeRegion }) {
  return (
    
      
        
          
        
        
          
            GeoHealth PlanAI
            
              SIH 2026 MVP
            
          
          
            
            Active Region: {activeRegion}
          
        
      

      
        
          
          Spatial MCDA Engine Active
        
        
          
          AI Planning Assistant
        
      
    
  );
}''',

    "src/components/Sidebar.jsx": '''import React from 'react';
import { LayoutDashboard, MapPin, Trophy, GitCompare, Sliders, Database, BookOpen } from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab }) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'analysis', label: 'Site Analysis', icon: MapPin },
    { id: 'ranking', label: 'Rankings', icon: Trophy },
    { id: 'comparison', label: 'Site Comparison', icon: GitCompare },
    { id: 'scenario', label: 'Scenario Weights', icon: Sliders },
    { id: 'datasources', label: 'Data Sources', icon: Database },
    { id: 'methodology', label: 'Methodology', icon: BookOpen },
  ];

  return (
    
      
        
          Decision System
        
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
             setActiveTab(item.id)}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-xs font-medium transition-all ${
                isActive
                  ? 'bg-brand-600 text-white shadow-md shadow-brand-600/20'
                  : 'text-slate-300 hover:bg-slate-800/80 hover:text-white'
              }`}
            >
              
              {item.label}
            
          );
        })}
      

      
        Demo Environment
        Nagpur Metropolitan Regional Development Corridor (PMR/NMR).
      
    
  );
}''',

    "src/components/MapView.jsx": '''import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { Layers } from 'lucide-react';

const createMarkerIcon = (color, text = "") => {
  return L.divIcon({
    className: 'custom-leaflet-marker',
    html: `${text}`,
    iconSize: [28, 28],
    iconAnchor: [14, 14],
    popupAnchor: [0, -14]
  });
};

function MapFocusController({ selectedSite }) {
  const map = useMap();
  useEffect(() => {
    if (selectedSite) {
      map.flyTo([selectedSite.latitude, selectedSite.longitude], 13, { duration: 1.2 });
    }
  }, [selectedSite, map]);
  return null;
}

export default function MapView({
  sites = [],
  hospitals = [],
  selectedSite = null,
  onSelectSite
}) {
  const defaultCenter = [21.1458, 79.0882];
  const [layerVisibility, setLayerVisibility] = useState({
    candidates: true,
    hospitals: true,
    buffers: true
  });

  return (
    
      
        
          
          GIS Layer Controls
        
        
           setLayerVisibility({ ...layerVisibility, candidates: e.target.checked })}
            className="rounded bg-slate-800 border-slate-600 text-brand-600 focus:ring-0"
          />
          
          Candidate Sites
        
        
           setLayerVisibility({ ...layerVisibility, hospitals: e.target.checked })}
            className="rounded bg-slate-800 border-slate-600 text-brand-600 focus:ring-0"
          />
          
          Existing Hospitals
        
        
           setLayerVisibility({ ...layerVisibility, buffers: e.target.checked })}
            className="rounded bg-slate-800 border-slate-600 text-brand-600 focus:ring-0"
          />
          
          Service Radii (2/5/10km)
        
      

      
        
        

        {layerVisibility.buffers && selectedSite && (
          <>
            
            
            
          
        )}

        {layerVisibility.candidates && sites.map((site) => {
          const isSelected = selectedSite && selectedSite.id === site.id;
          const isEligible = site.scores?.is_eligible;
          const color = !isEligible ? '#e11d48' : isSelected ? '#0284c7' : '#059669';
          const label = !isEligible ? '!' : `${site.scores?.rank || ''}`;

          return (
             onSelectSite && onSelectSite(site)
              }}
            >
              
                
                  
                    {site.name}
                  
                  
                    Rank: #{site.scores?.rank}
                    Score: {site.scores?.overall_score}
                    Parcel: {site.parcel_size_acres} Acres
                    5km Pop: {site.population_5km?.toLocaleString()}
                  
                
              
            
          );
        })}

        {layerVisibility.hospitals && hospitals.map((hosp) => (
          
            
              
                {hosp.name}
                Type: {hosp.type}
                Capacity: {hosp.beds} Beds
              
            
          
        ))}
      
    
  );
}''',

    "src/components/RankedTable.jsx": '''import React from 'react';
import ScoreBadge from './ScoreBadge';
import { ChevronRight } from 'lucide-react';

export default function RankedTable({ sites = [], selectedSite, onSelectSite }) {
  return (
    
      
          {sites.map((site) => {
            const isSelected = selectedSite && selectedSite.id === site.id;
            return (
               onSelectSite(site)}
                className={`cursor-pointer transition-colors ${
                  isSelected ? 'bg-brand-950/40 border-l-4 border-brand-500' : 'hover:bg-slate-800/50'
                }`}
              >
                
            );
          })}
        
        
          
            Rank
            Candidate Site & Zone
            Score
            5km Catchment
            Travel Time
            Nearest Hospital
            Parcel Area
            Action
          
        
        
                  {site.scores?.is_eligible ? `#${site.scores?.rank}` : '-'}
                
                
                  {site.name}
                  {site.zone}
                
                
                  
                
                
                  {site.population_5km?.toLocaleString()}
                  Underserved: {site.estimated_underserved_pop?.toLocaleString()}
                
                
                  {site.travel_time_min} mins
                  {site.distance_to_major_road_km} km to road
                
                
                  {site.distance_to_nearest_hospital_km} km
                  {site.nearest_hospital_name}
                
                
                  {site.parcel_size_acres} Acres
                  {site.slope_percent}% Slope
                
                
                   {
                      e.stopPropagation();
                      onSelectSite(site);
                    }}
                    className="p-1.5 rounded-lg bg-slate-800 hover:bg-brand-600 text-slate-300 hover:text-white transition-colors"
                  >
                    
                  
                
              
      
    
  );
}''',

    "src/components/ScenarioSliders.jsx": '''import React from 'react';
import { Sliders, RotateCcw, AlertTriangle } from 'lucide-react';

export default function ScenarioSliders({ weights, onChangeWeights, onReset }) {
  const criteria = [
    { key: 'healthcare_need', label: 'Healthcare Need (Population Demand)', default: 30 },
    { key: 'accessibility', label: 'Accessibility & Transit Ingress', default: 25 },
    { key: 'land_suitability', label: 'Land Area & Topography Suitability', default: 20 },
    { key: 'healthcare_gap', label: 'Healthcare Coverage Gap', default: 15 },
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
    
      
        
          
            
            MCDA Weight Configuration
          
          
            Adjust planning priorities to test policy outcomes.
          
        
        
          
          Reset
        
      

      
        {criteria.map((c) => (
          
            
              {c.label}
              {weights[c.key]}%
            
             handleSliderChange(c.key, e.target.value)}
              className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-brand-500"
            />
          
        ))}
      

      
        Total Sum:
        
          {totalWeight}% {totalWeight !== 100 && '(Auto-Normalized on Calculation)'}
        
      

      
        
        Prototype weights: modify freely to evaluate sensitivity changes in candidate rankings.
      
    
  );
}''',

    "src/components/AiAssistantDrawer.jsx": '''import React, { useState } from 'react';
import { X, Sparkles, Send, Bot, CheckCircle2 } from 'lucide-react';
import { apiService } from '../services/api';

export default function AiAssistantDrawer({ isOpen, onClose, sites = [] }) {
  if (!isOpen) return null;

  const [messages, setMessages] = useState([
    {
      sender: 'ai',
      text: "Hello! I am your GIS Planning Assistant. Ask me why a site was recommended, compare two sites, or audit the highest deficit zones."
    }
  ]);
  const [inputQuery, setInputQuery] = useState('');
  const [loading, setLoading] = useState(false);

  const presetQueries = [
    "Why is Site A ranked first?",
    "Which site has the highest healthcare gap?",
    "Compare Site 1 and Site 2."
  ];

  const handleSend = async (queryText) => {
    const text = queryText || inputQuery;
    if (!text.trim()) return;

    const userMsg = { sender: 'user', text };
    setMessages((prev) => [...prev, userMsg]);
    setInputQuery('');
    setLoading(true);

    try {
      const res = await apiService.queryAI(text, sites[0]?.id, sites[1]?.id);
      const aiMsg = { sender: 'ai', text: res.answer };
      setMessages((prev) => [...prev, aiMsg]);
    } catch (err) {
      setMessages((prev) => [...prev, { sender: 'ai', text: "Error fetching explanation from decision engine." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    
      
        
          
            
          
          
            AI Planning Assistant
            
               Spatial Decision Engine
            
          
        
        
          
        
      

      
        {messages.map((m, idx) => (
          
            {m.sender === 'ai' && (
              
                
              
            )}
            
              {m.text}
            
          
        ))}
        {loading && (
          
            ●
            Synthesizing GIS spatial metrics...
          
        )}
      

      
        Suggested:
        
          {presetQueries.map((q, idx) => (
             handleSend(q)}
              className="text-[11px] px-2.5 py-1 rounded-md bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700/60 text-left"
            >
              {q}
            
          ))}
        
      

      
         {
            e.preventDefault();
            handleSend();
          }}
          className="flex gap-2"
        >
           setInputQuery(e.target.value)}
            placeholder="Ask about recommendations or site comparisons..."
            className="flex-1 px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-brand-500"
          />
          
            
          
        
      
    
  );
}''',

    "src/pages/DashboardPage.jsx": '''import React from 'react';
import StatCard from '../components/StatCard';
import MapView from '../components/MapView';
import RankedTable from '../components/RankedTable';
import ScoreBadge from '../components/ScoreBadge';
import { Building2, Users, MapPin, Activity, ShieldAlert, Sparkles, Navigation } from 'lucide-react';

export default function DashboardPage({
  sites = [],
  hospitals = [],
  stats,
  selectedSite,
  onSelectSite,
  onOpenAI
}) {
  return (
    
      
        
        
        
        
      

      
        
          
        

        
          {selectedSite ? (
            
              
                
                  Selected Candidate
                  {selectedSite.name}
                  {selectedSite.zone}
                
                
              

              {selectedSite.scores?.is_eligible ? (
                
                  
                    
                    Justification Synthesis:
                  
                  {selectedSite.scores.explanation}
                
              ) : (
                
                  
                    
                    Statutory Constraint Failure
                  
                  
                    {selectedSite.scores?.ineligibility_reasons.map((r, idx) => (
                      {r}
                    ))}
                  
                
              )}
            
          ) : (
            
              
              Click on any map marker or ranking row to inspect suitability audit.
            
          )}

          
            
            Audit with AI Assistant
          
        
      

      
        Candidate Site Evaluation Rankings
        
      
    
  );
}''',

    "src/pages/SiteAnalysisPage.jsx": '''import React from 'react';
import MapView from '../components/MapView';
import ScoreBadge from '../components/ScoreBadge';
import { Users, Car, Building, Trees, CheckCircle2, XCircle } from 'lucide-react';

export default function SiteAnalysisPage({ sites = [], hospitals = [], selectedSite, onSelectSite }) {
  const currentSite = selectedSite || sites[0];

  return (
    
      
        Comprehensive GIS Parcel Analysis
        Detailed metric breakdown across accessibility, demography, and constraints.
      

      
        
          
        

        
          
            Parcel Deep-Dive
            {currentSite?.name}
            
              
              Rank #{currentSite?.scores?.rank}
            
          

          
            
              
              A. Population Catchment
            
            
              2km Pop: {currentSite?.population_2km?.toLocaleString()}
              5km Pop: {currentSite?.population_5km?.toLocaleString()}
              Underserved: {currentSite?.estimated_underserved_pop?.toLocaleString()}
            
          

          
            
              
              B. Road Connectivity
            
            
              Arterial Dist: {currentSite?.distance_to_major_road_km} km
              Transit: {currentSite?.travel_time_min} mins
              Corridor: {currentSite?.road_type}
            
          

          
            
              
              C. Land Suitability
            
            
              Area: {currentSite?.parcel_size_acres} Acres
              Slope: {currentSite?.slope_percent}%
              Land Use: {currentSite?.land_use}
            
          

          
            
              
              D. Environmental Clearance
            
            
              Water Dist: {currentSite?.distance_to_water_body_km} km
              Protected Dist: {currentSite?.distance_to_protected_zone_km} km
            
          
        
      
    
  );
}''',

    "src/pages/SiteComparisonPage.jsx": '''import React, { useState } from 'react';
import { GitCompare } from 'lucide-react';

export default function SiteComparisonPage({ sites = [] }) {
  const [siteAId, setSiteAId] = useState(sites[0]?.id || '');
  const [siteBId, setSiteBId] = useState(sites[1]?.id || '');

  const siteA = sites.find(s => s.id === siteAId) || sites[0];
  const siteB = sites.find(s => s.id === siteBId) || sites[1];

  const compareRows = [
    { label: 'Overall Score', valA: `${siteA?.scores?.overall_score || 0}/100`, valB: `${siteB?.scores?.overall_score || 0}/100`, highlightA: (siteA?.scores?.overall_score || 0) > (siteB?.scores?.overall_score || 0) },
    { label: '5km Catchment', valA: siteA?.population_5km?.toLocaleString(), valB: siteB?.population_5km?.toLocaleString(), highlightA: (siteA?.population_5km || 0) > (siteB?.population_5km || 0) },
    { label: 'Transit Time', valA: `${siteA?.travel_time_min} mins`, valB: `${siteB?.travel_time_min} mins`, highlightA: (siteA?.travel_time_min || 0) < (siteB?.travel_time_min || 0) },
    { label: 'Nearest Hospital', valA: `${siteA?.distance_to_nearest_hospital_km} km`, valB: `${siteB?.distance_to_nearest_hospital_km} km`, highlightA: (siteA?.distance_to_nearest_hospital_km || 0) > (siteB?.distance_to_nearest_hospital_km || 0) },
    { label: 'Parcel Area', valA: `${siteA?.parcel_size_acres} Acres`, valB: `${siteB?.parcel_size_acres} Acres`, highlightA: (siteA?.parcel_size_acres || 0) > (siteB?.parcel_size_acres || 0) },
    { label: 'Eligibility', valA: siteA?.scores?.is_eligible ? 'Eligible' : 'Ineligible', valB: siteB?.scores?.is_eligible ? 'Eligible' : 'Ineligible', highlightA: siteA?.scores?.is_eligible && !siteB?.scores?.is_eligible }
  ];

  return (
    
      
        
          
          Side-by-Side Siting Alternative Comparison
        
        Compare two candidate locations across all spatial vectors.
      

      
        
          Select Site A:
           setSiteAId(e.target.value)}
            className="w-full p-2.5 rounded-lg bg-slate-800 border border-slate-700 text-xs text-white"
          >
            {sites.map(s => {s.name})}
          
        

        
          Select Site B:
           setSiteBId(e.target.value)}
            className="w-full p-2.5 rounded-lg bg-slate-800 border border-slate-700 text-xs text-white"
          >
            {sites.map(s => {s.name})}
          
        
      

      
        
            {compareRows.map((row, idx) => (
              
            ))}
          
          
            
              Evaluation Criterion
              {siteA?.name}
              {siteB?.name}
            
          
          
                {row.label}
                
                  {row.valA}
                
                
                  {row.valB}
                
              
        
      
    
  );
}''',

    "src/pages/DataSourcesPage.jsx": '''import React, { useEffect, useState } from 'react';
import { Database } from 'lucide-react';
import { apiService } from '../services/api';

export default function DataSourcesPage() {
  const [sources, setSources] = useState([]);

  useEffect(() => {
    apiService.getDataSources().then(setSources).catch(console.error);
  }, []);

  return (
    
      
        
          
          Data Sources & API Integration Readiness
        
        Distinguishing verified open data and future API connectors.
      

      
        {sources.map((src, idx) => (
          
            
              
                {src.category}
                {src.source_name}
              
              
                {src.data_tier}
              
            
            
              Target Connector:
              {src.production_connector}
            
          
        ))}
      
    
  );
}''',

    "src/pages/MethodologyPage.jsx": '''import React from 'react';
import { BookOpen } from 'lucide-react';

export default function MethodologyPage() {
  const steps = [
    { title: "1. Spatial Ingestion & Cadastral Sieve", desc: "Parcels and spatial points are indexed into memory with Haversine matrices." },
    { title: "2. Statutory Hard Constraint Gating", desc: "Exclusions (Wetlands < 150m, Eco-sensitive zones < 500m, floodplains, < 3 Acres) are audited." },
    { title: "3. Multi-Factor Metric Normalization", desc: "GIS metrics are scaled to continuous [0, 100] domain values." },
    { title: "4. Multi-Criteria Decision Analysis (Weighted Sum)", desc: "Normalized scores combine via user policy weights (Need 30%, Access 25%, Land 20%, Gap 15%, Safety 10%)." },
    { title: "5. Grounded Explainable Recommendation", desc: "Natural language engine justifies ranking results transparently." },
  ];

  return (
    
      
        
          
          Scientific Methodology & Decision Flow
        
        Mathematical formulation of the Multi-Criteria Decision Analysis (MCDA) framework.
      

      
        {steps.map((s, idx) => (
          
            {s.title}
            {s.desc}
          
        ))}
      
    
  );
}''',

    "src/App.jsx": '''import React, { useEffect, useState } from 'react';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import DashboardPage from './pages/DashboardPage';
import SiteAnalysisPage from './pages/SiteAnalysisPage';
import RankedTable from './components/RankedTable';
import SiteComparisonPage from './pages/SiteComparisonPage';
import ScenarioSliders from './components/ScenarioSliders';
import DataSourcesPage from './pages/DataSourcesPage';
import MethodologyPage from './pages/MethodologyPage';
import AiAssistantDrawer from './components/AiAssistantDrawer';
import { apiService } from './services/api';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [sites, setSites] = useState([]);
  const [hospitals, setHospitals] = useState([]);
  const [stats, setStats] = useState(null);
  const [selectedSite, setSelectedSite] = useState(null);
  const [weights, setWeights] = useState({
    healthcare_need: 30,
    accessibility: 25,
    land_suitability: 20,
    healthcare_gap: 15,
    environmental_safety: 10
  });
  const [isAiOpen, setIsAiOpen] = useState(false);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      const [candidatesData, hospitalsData, statsData] = await Promise.all([
        apiService.getCandidates(),
        apiService.getHospitals(),
        apiService.getStatistics()
      ]);
      setSites(candidatesData);
      setHospitals(hospitalsData);
      setStats(statsData);
      if (candidatesData.length > 0) {
        setSelectedSite(candidatesData[0]);
      }
      setLoading(false);
    } catch (err) {
      console.error('Failed to load initial GIS data:', err);
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleWeightsChange = async (newWeights) => {
    setWeights(newWeights);
    try {
      const updatedSites = await apiService.updateScenario({
        weights: newWeights,
        minimum_area_sqm: 12000.0,
        exclude_flood_zones: true
      });
      setSites(updatedSites);
      const updatedStats = await apiService.getStatistics();
      setStats(updatedStats);
    } catch (err) {
      console.error('Scenario recalculation failed:', err);
    }
  };

  const handleResetWeights = () => {
    const defaultWeights = {
      healthcare_need: 30,
      accessibility: 25,
      land_suitability: 20,
      healthcare_gap: 15,
      environmental_safety: 10
    };
    handleWeightsChange(defaultWeights);
  };

  return (
    
       setIsAiOpen(true)} activeRegion="Nagpur Metropolitan Region, MH" />

      
        

        
          {loading ? (
            
              Connecting to GIS spatial backend...
            
          ) : (
            <>
              {activeTab === 'dashboard' && (
                 setSelectedSite(s)}
                  onOpenAI={() => setIsAiOpen(true)}
                />
              )}
              {activeTab === 'analysis' && (
                 setSelectedSite(s)}
                />
              )}
              {activeTab === 'ranking' && (
                
                  
                    Full Siting Priority Matrix
                    Ranked listing based on MCDA composite calculation.
                  
                   setSelectedSite(s)} />
                
              )}
              {activeTab === 'comparison' && }
              {activeTab === 'scenario' && (
                
                  
                
              )}
              {activeTab === 'datasources' && }
              {activeTab === 'methodology' && }
            
          )}
        
      

       setIsAiOpen(false)}
        sites={sites}
      />
    
  );
}'''
}

for path, content in files.items():
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {path}")

print("\n Frontend files created successfully.")