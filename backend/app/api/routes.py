from fastapi import APIRouter, HTTPException
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
