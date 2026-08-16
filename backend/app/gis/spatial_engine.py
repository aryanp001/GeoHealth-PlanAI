import math
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
