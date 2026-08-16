import os
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
