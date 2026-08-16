import React, { useEffect, useState } from 'react';
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

const FALLBACK_SITES = [
  {
    id: "SITE_NAG_01",
    name: "Besa-Pipla Southern Growth Sector",
    zone: "South Zone (Wardha Rd Fringe)",
    latitude: 21.0782,
    longitude: 79.0945,
    area_sqm: 32400.0,
    parcel_size_acres: 8.01,
    land_use: "Public-Semi-Public Institutional",
    slope_percent: 1.2,
    elevation_m: 312.0,
    population_2km: 42000,
    population_5km: 188000,
    population_10km: 540000,
    estimated_underserved_pop: 125000,
    distance_to_major_road_km: 0.35,
    travel_time_min: 14.0,
    road_type: "Outer Ring Road Arterial (4-lane)",
    distance_to_nearest_hospital_km: 6.8,
    hospitals_within_5km: 1,
    nearest_hospital_name: "AIIMS Nagpur (Tertiary)",
    distance_to_water_body_km: 1.85,
    distance_to_protected_zone_km: 4.5,
    is_in_flood_zone: false,
    scores: {
      overall_score: 84.5,
      healthcare_need_score: 88.0,
      accessibility_score: 82.5,
      land_suitability_score: 85.0,
      healthcare_gap_score: 79.0,
      environmental_safety_score: 92.0,
      rank: 1,
      is_eligible: true,
      ineligibility_reasons: [],
      explanation: "Recommended: High population catchment (188,000 in 5km), significant healthcare deficit, and excellent arterial transit connectivity."
    }
  },
  {
    id: "SITE_NAG_02",
    name: "Wadi-Hingna Industrial Extension",
    zone: "West Zone (Amravati Rd Corridor)",
    latitude: 21.1415,
    longitude: 78.9850,
    area_sqm: 41200.0,
    parcel_size_acres: 10.18,
    land_use: "Mixed Commercial/Institutional",
    slope_percent: 2.1,
    elevation_m: 328.0,
    population_2km: 56000,
    population_5km: 210000,
    population_10km: 620000,
    estimated_underserved_pop: 164000,
    distance_to_major_road_km: 0.15,
    travel_time_min: 11.5,
    road_type: "National Highway 53 Connector",
    distance_to_nearest_hospital_km: 7.4,
    hospitals_within_5km: 1,
    nearest_hospital_name: "Lata Mangeshkar Hospital",
    distance_to_water_body_km: 1.4,
    distance_to_protected_zone_km: 3.8,
    is_in_flood_zone: false,
    scores: {
      overall_score: 81.2,
      healthcare_need_score: 91.0,
      accessibility_score: 89.0,
      land_suitability_score: 78.0,
      healthcare_gap_score: 74.0,
      environmental_safety_score: 80.0,
      rank: 2,
      is_eligible: true,
      ineligibility_reasons: [],
      explanation: "Optimal highway connection via NH-53 connector with 11.5 min emergency response time."
    }
  }
];

const FALLBACK_HOSPITALS = [
  { id: "HOSP_01", name: "AIIMS Nagpur", type: "Apex Tertiary", beds: 960, emergency: true, latitude: 21.0420, longitude: 79.0480 },
  { id: "HOSP_02", name: "Government Medical College", type: "Public Tertiary", beds: 1400, emergency: true, latitude: 21.1340, longitude: 79.0980 }
];

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [sites, setSites] = useState(FALLBACK_SITES);
  const [hospitals, setHospitals] = useState(FALLBACK_HOSPITALS);
  const [stats, setStats] = useState({
    total_candidates: 2,
    eligible_sites: 2,
    high_priority_sites: 2,
    total_underserved_population_covered: 289000,
    average_accessibility_score: 85.7,
    top_recommended_site_name: "Besa-Pipla Southern Growth Sector"
  });
  const [selectedSite, setSelectedSite] = useState(FALLBACK_SITES[0]);
  const [weights, setWeights] = useState({
    healthcare_need: 30,
    accessibility: 25,
    land_suitability: 20,
    healthcare_gap: 15,
    environmental_safety: 10
  });
  const [isAiOpen, setIsAiOpen] = useState(false);

  useEffect(() => {
    Promise.all([
      apiService.getCandidates(),
      apiService.getHospitals(),
      apiService.getStatistics()
    ])
      .then(([candidatesData, hospitalsData, statsData]) => {
        if (candidatesData && candidatesData.length > 0) {
          setSites(candidatesData);
          setSelectedSite(candidatesData[0]);
        }
        if (hospitalsData && hospitalsData.length > 0) {
          setHospitals(hospitalsData);
        }
        if (statsData) {
          setStats(statsData);
        }
      })
      .catch((err) => {
        console.warn('Backend connection pending - using built-in standalone dataset:', err.message);
      });
  }, []);

  const handleWeightsChange = async (newWeights) => {
    setWeights(newWeights);
    try {
      const updatedSites = await apiService.updateScenario({
        weights: newWeights,
        minimum_area_sqm: 12000.0,
        exclude_flood_zones: true
      });
      if (updatedSites) setSites(updatedSites);
      const updatedStats = await apiService.getStatistics();
      if (updatedStats) setStats(updatedStats);
    } catch (err) {
      console.warn('Scenario recalculation falling back to local state update.');
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
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Navbar onOpenAI={() => setIsAiOpen(true)} activeRegion="Nagpur Metropolitan Region, MH" />

      <div className="flex-1 flex overflow-hidden">
        <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

        <main className="flex-1 overflow-y-auto p-6 bg-slate-950">
          {activeTab === 'dashboard' && (
            <DashboardPage
              sites={sites}
              hospitals={hospitals}
              stats={stats}
              selectedSite={selectedSite}
              onSelectSite={(s) => setSelectedSite(s)}
              onOpenAI={() => setIsAiOpen(true)}
            />
          )}
          {activeTab === 'analysis' && (
            <SiteAnalysisPage
              sites={sites}
              hospitals={hospitals}
              selectedSite={selectedSite}
              onSelectSite={(s) => setSelectedSite(s)}
            />
          )}
          {activeTab === 'ranking' && (
            <div className="space-y-4">
              <div>
                <h2 className="text-base font-bold text-white">Full Siting Priority Matrix</h2>
                <p className="text-xs text-slate-400">Ranked listing based on MCDA composite calculation.</p>
              </div>
              <RankedTable sites={sites} selectedSite={selectedSite} onSelectSite={(s) => setSelectedSite(s)} />
            </div>
          )}
          {activeTab === 'comparison' && <SiteComparisonPage sites={sites} />}
          {activeTab === 'scenario' && (
            <div className="max-w-2xl">
              <ScenarioSliders
                weights={weights}
                onChangeWeights={handleWeightsChange}
                onReset={handleResetWeights}
              />
            </div>
          )}
          {activeTab === 'datasources' && <DataSourcesPage />}
          {activeTab === 'methodology' && <MethodologyPage />}
        </main>
      </div>

      <AiAssistantDrawer
        isOpen={isAiOpen}
        onClose={() => setIsAiOpen(false)}
        sites={sites}
      />
    </div>
  );
}