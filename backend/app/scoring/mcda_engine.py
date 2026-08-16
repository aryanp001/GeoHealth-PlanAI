from typing import List, Dict
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
