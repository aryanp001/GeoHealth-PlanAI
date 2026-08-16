from typing import List, Dict, Any

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
