from typing import List, Optional
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
                f"**{top_site.name}** is ranked #1 with an overall score of **{top_site.scores.overall_score}/100**.\n\n"
                f"• Population served in 5km: {top_site.population_5km:,}\n"
                f"• Nearest hospital distance: {top_site.distance_to_nearest_hospital_km} km\n"
                f"• Road transit time: {top_site.travel_time_min} mins ({top_site.road_type})"
            ),
            key_metrics_referenced={"site_id": top_site.id, "overall_score": top_site.scores.overall_score},
            confidence=0.98
        )
