import os

files = {
    "app/__init__.py": "",
    "app/models/__init__.py": "",
    "app/db/__init__.py": "",
    "app/gis/__init__.py": "",
    "app/scoring/__init__.py": "",
    "app/ai/__init__.py": "",
    "app/adapters/__init__.py": "",
    "app/api/__init__.py": "",

    "app/config.py": '''import os
from pydantic import BaseModel

class Settings(BaseModel):
    app_name: str = "SIH 2026 GIS Hospital Site Selection Engine"
    api_prefix: str = "/api"
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", 8000))
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "*"
    ]
    demo_region: str = "Nagpur Metropolitan Growth Region, MH (Demo Dataset)"

settings = Settings()
''',

    "app/models/schemas.py": '''from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class WeightConfig(BaseModel):
    healthcare_need: float = Field(30.0, ge=0, le=100)
    accessibility: float = Field(25.0, ge=0, le=100)
    land_suitability: float = Field(20.0, ge=0, le=100)
    healthcare_gap: float = Field(15.0, ge=0, le=100)
    environmental_safety: float = Field(10.0, ge=0, le=100)

class ScenarioRequest(BaseModel):
    weights: WeightConfig
    minimum_area_sqm: float = 12000.0
    exclude_flood_zones: bool = True

class SiteScoreBreakdown(BaseModel):
    overall_score: float
    healthcare_need_score: float
    accessibility_score: float
    land_suitability_score: float
    healthcare_gap_score: float
    environmental_safety_score: float
    rank: int = 1
    is_eligible: bool
    ineligibility_reasons: List[str] = []
    explanation: str

class CandidateSite(BaseModel):
    id: str
    name: str
    zone: str
    latitude: float
    longitude: float
    area_sqm: float
    parcel_size_acres: float
    land_use: str
    slope_percent: float
    elevation_m: float
    est_acquisition_cost_inr_cr: float
    population_2km: int
    population_5km: int
    population_10km: int
    estimated_underserved_pop: int
    distance_to_major_road_km: float
    travel_time_min: float
    road_type: str
    distance_to_nearest_hospital_km: float
    hospitals_within_5km: int
    nearest_hospital_name: str
    distance_to_water_body_km: float
    distance_to_protected_zone_km: float
    is_in_flood_zone: bool
    scores: Optional[SiteScoreBreakdown] = None

class ExistingHospital(BaseModel):
    id: str
    name: str
    type: str
    beds: int
    emergency: bool
    latitude: float
    longitude: float

class EnvironmentalConstraint(BaseModel):
    id: str
    name: str
    category: str
    latitude: float
    longitude: float
    radius_meters: float
    is_hard_exclusion: bool
    description: str

class LayerGeoJSONResponse(BaseModel):
    type: str = "FeatureCollection"
    features: List[Dict[str, Any]]

class StatisticsResponse(BaseModel):
    total_candidates: int
    eligible_sites: int
    high_priority_sites: int
    total_underserved_population_covered: int
    average_accessibility_score: float
    top_recommended_site_id: str
    top_recommended_site_name: str
    highest_gap_site_id: str

class AIQueryRequest(BaseModel):
    query: str
    site_id_a: Optional[str] = None
    site_id_b: Optional[str] = None

class AIQueryResponse(BaseModel):
    query: str
    answer: str
    key_metrics_referenced: Dict[str, Any]
    confidence: float
''',

    "app/db/seed_data.py": '''CANDIDATE_SITES_DATA = [
    {
        "id": "SITE_NAG_01",
        "name": "Besa-Pipla Southern Growth Sector",
        "zone": "South Zone (Wardha Rd Fringe)",
        "latitude": 21.0782,
        "longitude": 79.0945,
        "area_sqm": 32400.0,
        "parcel_size_acres": 8.01,
        "land_use": "Public-Semi-Public Institutional",
        "slope_percent": 1.2,
        "elevation_m": 312.0,
        "est_acquisition_cost_inr_cr": 24.5,
        "population_2km": 42000,
        "population_5km": 188000,
        "population_10km": 540000,
        "estimated_underserved_pop": 125000,
        "distance_to_major_road_km": 0.35,
        "travel_time_min": 14.0,
        "road_type": "Outer Ring Road Arterial (4-lane)",
        "distance_to_nearest_hospital_km": 6.8,
        "hospitals_within_5km": 1,
        "nearest_hospital_name": "AIIMS Nagpur (Tertiary)",
        "distance_to_water_body_km": 1.85,
        "distance_to_protected_zone_km": 4.5,
        "is_in_flood_zone": False
    },
    {
        "id": "SITE_NAG_02",
        "name": "Wadi-Hingna Industrial Extension",
        "zone": "West Zone (Amravati Rd Corridor)",
        "latitude": 21.1415,
        "longitude": 78.9850,
        "area_sqm": 41200.0,
        "parcel_size_acres": 10.18,
        "land_use": "Mixed Commercial/Institutional",
        "slope_percent": 2.1,
        "elevation_m": 328.0,
        "est_acquisition_cost_inr_cr": 28.0,
        "population_2km": 56000,
        "population_5km": 210000,
        "population_10km": 620000,
        "estimated_underserved_pop": 164000,
        "distance_to_major_road_km": 0.15,
        "travel_time_min": 11.5,
        "road_type": "National Highway 53 Connector",
        "distance_to_nearest_hospital_km": 7.4,
        "hospitals_within_5km": 1,
        "nearest_hospital_name": "Lata Mangeshkar Hospital",
        "distance_to_water_body_km": 1.4,
        "distance_to_protected_zone_km": 3.8,
        "is_in_flood_zone": False
    },
    {
        "id": "SITE_NAG_03",
        "name": "Kamptee-Uppalwadi Logistics Belt",
        "zone": "North-East Corridor",
        "latitude": 21.2150,
        "longitude": 79.1620,
        "area_sqm": 28500.0,
        "parcel_size_acres": 7.04,
        "land_use": "Government Vacant Plot",
        "slope_percent": 1.8,
        "elevation_m": 305.0,
        "est_acquisition_cost_inr_cr": 16.8,
        "population_2km": 38000,
        "population_5km": 154000,
        "population_10km": 490000,
        "estimated_underserved_pop": 118000,
        "distance_to_major_road_km": 0.60,
        "travel_time_min": 19.0,
        "road_type": "State Highway 248",
        "distance_to_nearest_hospital_km": 8.2,
        "hospitals_within_5km": 0,
        "nearest_hospital_name": "Sub-District Hospital Kamptee",
        "distance_to_water_body_km": 0.95,
        "distance_to_protected_zone_km": 5.2,
        "is_in_flood_zone": False
    },
    {
        "id": "SITE_NAG_04",
        "name": "MIHAN Multi-Modal SEZ Edge",
        "zone": "South Special Economic Zone",
        "latitude": 21.0350,
        "longitude": 79.0520,
        "area_sqm": 56000.0,
        "parcel_size_acres": 13.84,
        "land_use": "Special Health/Institutional Reserve",
        "slope_percent": 0.9,
        "elevation_m": 315.0,
        "est_acquisition_cost_inr_cr": 38.0,
        "population_2km": 19000,
        "population_5km": 82000,
        "population_10km": 310000,
        "estimated_underserved_pop": 64000,
        "distance_to_major_road_km": 0.20,
        "travel_time_min": 16.0,
        "road_type": "Expressway Corridor (6-lane)",
        "distance_to_nearest_hospital_km": 3.2,
        "hospitals_within_5km": 2,
        "nearest_hospital_name": "AIIMS Nagpur",
        "distance_to_water_body_km": 2.6,
        "distance_to_protected_zone_km": 6.0,
        "is_in_flood_zone": False
    },
    {
        "id": "SITE_NAG_05",
        "name": "Gorewada Catchment Buffer Plot",
        "zone": "North-West Ecological Fringe",
        "latitude": 21.1980,
        "longitude": 79.0340,
        "area_sqm": 18000.0,
        "parcel_size_acres": 4.45,
        "land_use": "Agricultural/Restricted Green",
        "slope_percent": 4.8,
        "elevation_m": 342.0,
        "est_acquisition_cost_inr_cr": 12.0,
        "population_2km": 22000,
        "population_5km": 94000,
        "population_10km": 380000,
        "estimated_underserved_pop": 58000,
        "distance_to_major_road_km": 1.45,
        "travel_time_min": 24.5,
        "road_type": "Secondary Rural Road (2-lane)",
        "distance_to_nearest_hospital_km": 5.1,
        "hospitals_within_5km": 1,
        "nearest_hospital_name": "Alexis Multispecialty Hospital",
        "distance_to_water_body_km": 0.08,
        "distance_to_protected_zone_km": 0.25,
        "is_in_flood_zone": True
    },
    {
        "id": "SITE_NAG_06",
        "name": "Umred Road Dighori Expansion",
        "zone": "South-East Sector",
        "latitude": 21.1020,
        "longitude": 79.1480,
        "area_sqm": 35000.0,
        "parcel_size_acres": 8.65,
        "land_use": "Public Semi-Public",
        "slope_percent": 1.5,
        "elevation_m": 308.0,
        "est_acquisition_cost_inr_cr": 22.0,
        "population_2km": 49000,
        "population_5km": 195000,
        "population_10km": 580000,
        "estimated_underserved_pop": 142000,
        "distance_to_major_road_km": 0.30,
        "travel_time_min": 13.0,
        "road_type": "State Highway 9 Arterial",
        "distance_to_nearest_hospital_km": 7.1,
        "hospitals_within_5km": 0,
        "nearest_hospital_name": "Government Medical College (GMC)",
        "distance_to_water_body_km": 1.6,
        "distance_to_protected_zone_km": 4.1,
        "is_in_flood_zone": False
    },
    {
        "id": "SITE_NAG_07",
        "name": "Manewada Sub-Urban Parcel",
        "zone": "South-Central Cluster",
        "latitude": 21.1080,
        "longitude": 79.0980,
        "area_sqm": 9500.0,
        "parcel_size_acres": 2.35,
        "land_use": "Dense Residential Infill",
        "slope_percent": 0.8,
        "elevation_m": 310.0,
        "est_acquisition_cost_inr_cr": 19.5,
        "population_2km": 68000,
        "population_5km": 240000,
        "population_10km": 710000,
        "estimated_underserved_pop": 178000,
        "distance_to_major_road_km": 0.10,
        "travel_time_min": 9.0,
        "road_type": "Inner City Major Collector",
        "distance_to_nearest_hospital_km": 3.8,
        "hospitals_within_5km": 3,
        "nearest_hospital_name": "Orange City Hospital",
        "distance_to_water_body_km": 2.1,
        "distance_to_protected_zone_km": 5.5,
        "is_in_flood_zone": False
    }
]

EXISTING_HOSPITALS_DATA = [
    {"id": "HOSP_01", "name": "AIIMS Nagpur (Apex Tertiary)", "type": "Apex Tertiary Referral", "beds": 960, "emergency": True, "latitude": 21.0420, "longitude": 79.0480},
    {"id": "HOSP_02", "name": "Government Medical College (GMC)", "type": "Public Tertiary", "beds": 1400, "emergency": True, "latitude": 21.1340, "longitude": 79.0980},
    {"id": "HOSP_03", "name": "Alexis Multispecialty Hospital", "type": "Private Tertiary", "beds": 250, "emergency": True, "latitude": 21.1850, "longitude": 79.0750},
    {"id": "HOSP_04", "name": "Orange City Hospital & Research", "type": "Multispecialty Secondary", "beds": 220, "emergency": True, "latitude": 21.1180, "longitude": 79.0620},
    {"id": "HOSP_05", "name": "Lata Mangeshkar Hospital", "type": "Medical College Hospital", "beds": 750, "emergency": True, "latitude": 21.1120, "longitude": 78.9980}
]

ENVIRONMENTAL_CONSTRAINTS_DATA = [
    {"id": "ENV_01", "name": "Gorewada Bio-Park Reserve", "category": "Protected Forest", "latitude": 21.2020, "longitude": 79.0280, "radius_meters": 1200.0, "is_hard_exclusion": True, "description": "500m eco-sensitive buffer."},
    {"id": "ENV_02", "name": "Ambazari Lake Catchment", "category": "Urban Water Body", "latitude": 21.1290, "longitude": 79.0430, "radius_meters": 750.0, "is_hard_exclusion": True, "description": "Construction prohibited within 150m."}
]

POPULATION_ZONES_DATA = [
    {"id": "POP_01", "name": "Besa-Ghoghli Urban Ward", "total_population": 84000, "density_per_sqkm": 6800.0, "underserved_ratio": 0.65, "latitude": 21.0820, "longitude": 79.0920},
    {"id": "POP_02", "name": "Wadi Municipal Council", "total_population": 98000, "density_per_sqkm": 7200.0, "underserved_ratio": 0.72, "latitude": 21.1440, "longitude": 78.9910}
]

ROAD_NETWORKS_DATA = [
    {"id": "ROAD_01", "name": "Outer Ring Road Bypass", "type": "National Highway", "lanes": 6, "coordinates": [[21.0300, 79.0400], [21.0750, 79.0900], [21.1000, 79.1500]]}
]
''',

    "app/gis/spatial_engine.py": '''import math
from typing import List, Dict, Any

class SpatialEngine:
    EARTH_RADIUS_KM = 6371.0088

    @classmethod
    def generate_buffer_circle(cls, lat: float, lon: float, radius_km: float, num_points: int = 32) -> List[List[float]]:
        coords = []
        d_rad = radius_km / cls.EARTH_RADIUS_KM
        lat_rad = math.radians(lat)
        lon_rad = math.radians(lon)

        for i in range(num_points + 1):
            bearing = 2 * math.pi * (i / num_points)
            p_lat = math.asin(
                math.sin(lat_rad) * math.cos(d_rad) +
                math.cos(lat_rad) * math.sin(d_rad) * math.cos(bearing)
            )
            p_lon = lon_rad + math.atan2(
                math.sin(bearing) * math.sin(d_rad) * math.cos(lat_rad),
                math.cos(d_rad) - math.sin(lat_rad) * math.sin(p_lat)
            )
            coords.append([round(math.degrees(p_lat), 6), round(math.degrees(p_lon), 6)])
        return coords

    @classmethod
    def assemble_geojson_feature(cls, geometry_type: str, coordinates: Any, properties: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "Feature",
            "geometry": {
                "type": geometry_type,
                "coordinates": coordinates
            },
            "properties": properties
        }
''',

    "app/scoring/mcda_engine.py": '''from typing import List, Dict
from app.models.schemas import CandidateSite, SiteScoreBreakdown, ScenarioRequest

class MCDAScoringEngine:
    @staticmethod
    def evaluate_all(sites_data: List[Dict], scenario: ScenarioRequest) -> List[CandidateSite]:
        weights = scenario.weights
        total_weight = (
            weights.healthcare_need +
            weights.accessibility +
            weights.land_suitability +
            weights.healthcare_gap +
            weights.environmental_safety
        ) or 100.0

        w_need = weights.healthcare_need / total_weight
        w_acc = weights.accessibility / total_weight
        w_suit = weights.land_suitability / total_weight
        w_gap = weights.healthcare_gap / total_weight
        w_env = weights.environmental_safety / total_weight

        max_pop = max((s["population_5km"] for s in sites_data), default=1)
        max_underserved = max((s["estimated_underserved_pop"] for s in sites_data), default=1)
        max_dist_road = max((s["distance_to_major_road_km"] for s in sites_data), default=1.0)
        max_travel_time = max((s["travel_time_min"] for s in sites_data), default=1.0)
        max_area = max((s["area_sqm"] for s in sites_data), default=1.0)
        max_slope = max((s["slope_percent"] for s in sites_data), default=1.0)
        max_dist_hosp = max((s["distance_to_nearest_hospital_km"] for s in sites_data), default=1.0)
        max_hosp_nearby = max((s["hospitals_within_5km"] for s in sites_data), default=1)
        max_dist_water = max((s["distance_to_water_body_km"] for s in sites_data), default=1.0)
        max_dist_reserve = max((s["distance_to_protected_zone_km"] for s in sites_data), default=1.0)

        evaluated_sites: List[CandidateSite] = []

        for item in sites_data:
            reasons: List[str] = []
            is_eligible = True

            if item["area_sqm"] < scenario.minimum_area_sqm:
                is_eligible = False
                reasons.append(f"Insufficient parcel size ({item['area_sqm']} m² < {scenario.minimum_area_sqm} m² req).")

            if item["distance_to_water_body_km"] < 0.15:
                is_eligible = False
                reasons.append(f"Water Body Buffer Violation ({int(item['distance_to_water_body_km']*1000)}m < 150m clearance).")

            if item["distance_to_protected_zone_km"] < 0.50:
                is_eligible = False
                reasons.append(f"Eco-Sensitive Zone Infringement ({int(item['distance_to_protected_zone_km']*1000)}m buffer).")

            if scenario.exclude_flood_zones and item.get("is_in_flood_zone", False):
                is_eligible = False
                reasons.append("Identified in high-vulnerability seasonal flood basin.")

            need_score = (0.55 * (item["population_5km"] / max_pop) + 0.45 * (item["estimated_underserved_pop"] / max_underserved)) * 100.0
            acc_dist_factor = max(0.0, 1.0 - (item["distance_to_major_road_km"] / (max_dist_road * 1.1)))
            acc_time_factor = max(0.0, 1.0 - (item["travel_time_min"] / (max_travel_time * 1.1)))
            accessibility_score = (0.50 * acc_dist_factor + 0.50 * acc_time_factor) * 100.0
            area_factor = item["area_sqm"] / max_area
            slope_factor = max(0.0, 1.0 - (item["slope_percent"] / (max_slope * 1.2)))
            suitability_score = (0.60 * area_factor + 0.40 * slope_factor) * 100.0
            gap_dist_factor = item["distance_to_nearest_hospital_km"] / max_dist_hosp
            gap_density_factor = max(0.0, 1.0 - (item["hospitals_within_5km"] / (max_hosp_nearby + 1)))
            gap_score = (0.70 * gap_dist_factor + 0.30 * gap_density_factor) * 100.0
            env_water_factor = min(1.0, item["distance_to_water_body_km"] / max_dist_water)
            env_reserve_factor = min(1.0, item["distance_to_protected_zone_km"] / max_dist_reserve)
            env_score = (0.50 * env_water_factor + 0.50 * env_reserve_factor) * 100.0

            if is_eligible:
                overall_score = (
                    w_need * need_score +
                    w_acc * accessibility_score +
                    w_suit * suitability_score +
                    w_gap * gap_score +
                    w_env * env_score
                )
                explanation = (
                    f"Recommended location: High catchment ({item['population_5km']:,} in 5km), "
                    f"clear gap ({item['distance_to_nearest_hospital_km']}km to nearest tertiary), "
                    f"direct road access ({item['distance_to_major_road_km']}km via {item['road_type']}), "
                    f"and zero statutory environmental exclusions."
                )
            else:
                overall_score = 0.0
                explanation = f"INELIGIBLE FOR HOSPITAL SITING: {'; '.join(reasons)}"

            breakdown = SiteScoreBreakdown(
                overall_score=round(overall_score, 1),
                healthcare_need_score=round(need_score, 1),
                accessibility_score=round(accessibility_score, 1),
                land_suitability_score=round(suitability_score, 1),
                healthcare_gap_score=round(gap_score, 1),
                environmental_safety_score=round(env_score, 1),
                rank=1,
                is_eligible=is_eligible,
                ineligibility_reasons=reasons,
                explanation=explanation
            )

            evaluated_sites.append(CandidateSite(**item, scores=breakdown))

        evaluated_sites.sort(key=lambda s: (s.scores.is_eligible, s.scores.overall_score), reverse=True)
        for idx, site in enumerate(evaluated_sites):
            site.scores.rank = idx + 1 if site.scores.is_eligible else 999

        return evaluated_sites
''',

    "app/ai/explainability.py": '''from typing import List, Optional
from app.models.schemas import CandidateSite, AIQueryResponse

class GroundedAIExplanationEngine:
    @classmethod
    def answer_query(cls, query_str: str, sites: List[CandidateSite], site_a_id: Optional[str] = None, site_b_id: Optional[str] = None) -> AIQueryResponse:
        q = query_str.lower().strip()
        site_map = {s.id: s for s in sites}
        top_site = next((s for s in sites if s.scores.is_eligible), sites[0])

        if "gap" in q or "deficit" in q or "underserved" in q:
            highest_gap = max(sites, key=lambda s: s.scores.healthcare_gap_score if s.scores.is_eligible else -1)
            return AIQueryResponse(
                query=query_str,
                answer=f"**{highest_gap.name}** has the highest healthcare gap score ({highest_gap.scores.healthcare_gap_score}/100) and is located {highest_gap.distance_to_nearest_hospital_km} km from the nearest hospital.",
                key_metrics_referenced={"site_id": highest_gap.id, "gap_score": highest_gap.scores.healthcare_gap_score},
                confidence=0.96
            )

        return AIQueryResponse(
            query=query_str,
            answer=(
                f"**{top_site.name}** is ranked #1 with an overall score of **{top_site.scores.overall_score}/100**.\\n\\n"
                f"• Population served in 5km: {top_site.population_5km:,}\\n"
                f"• Nearest hospital distance: {top_site.distance_to_nearest_hospital_km} km\\n"
                f"• Road transit time: {top_site.travel_time_min} mins ({top_site.road_type})"
            ),
            key_metrics_referenced={"site_id": top_site.id, "overall_score": top_site.scores.overall_score},
            confidence=0.98
        )
''',

    "app/adapters/data_sources.py": '''from typing import List, Dict, Any

class DataSourceRegistry:
    @staticmethod
    def get_catalog() -> List[Dict[str, Any]]:
        return [
            {
                "category": "Roads & Transportation",
                "source_name": "OpenStreetMap (OSM)",
                "integration_status": "API Access Prepared / Mock Active",
                "production_connector": "overpass-api.de / OSRM Routing",
                "attributes": ["Highway classification", "Lane counts", "Speed profiles"],
                "data_tier": "Verified Open Source Specification"
            },
            {
                "category": "Demographics & Census",
                "source_name": "Census India Projections",
                "integration_status": "Calibrated Benchmark Data",
                "production_connector": "censusindia.gov.in",
                "attributes": ["Ward-level population", "Underserved ratio"],
                "data_tier": "Calibrated Hackathon Benchmark"
            }
        ]
''',

    "app/api/routes.py": '''from fastapi import APIRouter, HTTPException
from typing import List
from app.models.schemas import (
    CandidateSite, ExistingHospital, LayerGeoJSONResponse,
    ScenarioRequest, WeightConfig, StatisticsResponse,
    AIQueryRequest, AIQueryResponse
)
from app.db.seed_data import (
    CANDIDATE_SITES_DATA, EXISTING_HOSPITALS_DATA,
    ENVIRONMENTAL_CONSTRAINTS_DATA
)
from app.gis.spatial_engine import SpatialEngine
from app.scoring.mcda_engine import MCDAScoringEngine
from app.ai.explainability import GroundedAIExplanationEngine
from app.adapters.data_sources import DataSourceRegistry

router = APIRouter()
current_scenario = ScenarioRequest(weights=WeightConfig())

@router.get("/candidates", response_model=List[CandidateSite])
def get_candidate_sites():
    return MCDAScoringEngine.evaluate_all(CANDIDATE_SITES_DATA, current_scenario)

@router.get("/sites/{site_id}", response_model=CandidateSite)
def get_candidate_site_by_id(site_id: str):
    evaluated = MCDAScoringEngine.evaluate_all(CANDIDATE_SITES_DATA, current_scenario)
    site = next((s for s in evaluated if s.id == site_id), None)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return site

@router.get("/hospitals", response_model=List[ExistingHospital])
def get_existing_hospitals():
    return [ExistingHospital(**h) for h in EXISTING_HOSPITALS_DATA]

@router.get("/statistics", response_model=StatisticsResponse)
def get_platform_statistics():
    evaluated = MCDAScoringEngine.evaluate_all(CANDIDATE_SITES_DATA, current_scenario)
    eligible = [s for s in evaluated if s.scores.is_eligible]
    high_priority = [s for s in eligible if s.scores.overall_score >= 70.0]
    total_underserved = sum(s.estimated_underserved_pop for s in eligible)
    avg_acc = sum(s.scores.accessibility_score for s in eligible) / max(1, len(eligible))
    top_site = eligible[0] if eligible else evaluated[0]
    highest_gap_site = max(eligible, key=lambda s: s.scores.healthcare_gap_score, default=evaluated[0])

    return StatisticsResponse(
        total_candidates=len(evaluated),
        eligible_sites=len(eligible),
        high_priority_sites=len(high_priority),
        total_underserved_population_covered=total_underserved,
        average_accessibility_score=round(avg_acc, 1),
        top_recommended_site_id=top_site.id,
        top_recommended_site_name=top_site.name,
        highest_gap_site_id=highest_gap_site.id
    )

@router.post("/scenario", response_model=List[CandidateSite])
def recalculate_scenario(scenario: ScenarioRequest):
    global current_scenario
    current_scenario = scenario
    return MCDAScoringEngine.evaluate_all(CANDIDATE_SITES_DATA, current_scenario)

@router.get("/layers/geojson", response_model=LayerGeoJSONResponse)
def get_gis_layers_geojson():
    features = []
    evaluated = MCDAScoringEngine.evaluate_all(CANDIDATE_SITES_DATA, current_scenario)
    for s in evaluated:
        features.append(SpatialEngine.assemble_geojson_feature(
            geometry_type="Point",
            coordinates=[s.longitude, s.latitude],
            properties={
                "layer_type": "candidate_site",
                "id": s.id,
                "name": s.name,
                "rank": s.scores.rank,
                "score": s.scores.overall_score,
                "eligible": s.scores.is_eligible
            }
        ))
    return LayerGeoJSONResponse(features=features)

@router.post("/ai/query", response_model=AIQueryResponse)
def query_ai_planner(request: AIQueryRequest):
    evaluated = MCDAScoringEngine.evaluate_all(CANDIDATE_SITES_DATA, current_scenario)
    return GroundedAIExplanationEngine.answer_query(request.query, evaluated, request.site_id_a, request.site_id_b)

@router.get("/data-sources")
def get_data_sources():
    return DataSourceRegistry.get_catalog()
''',

    "app/main.py": '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.routes import router

app = FastAPI(
    title=settings.app_name,
    description="SIH 2026 AI/GIS-based Hospital Infrastructure Decision Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=settings.api_prefix)

@app.get("/")
def root():
    return {
        "status": "online",
        "project": settings.app_name,
        "region": settings.demo_region,
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=True)
'''
}

for path, content in files.items():
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {path}")

print("\n All backend files created successfully.")