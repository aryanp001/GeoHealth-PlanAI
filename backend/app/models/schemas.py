from pydantic import BaseModel, Field
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
