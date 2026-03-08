import os
from dataclasses import dataclass
from typing import List

from dotenv import load_dotenv

DEFAULT_KEYWORDS: List[str] = [
    "sterilization",
    "disinfection",
    "germicidal",
    "UVC",
    "medical devices",
    "water treatment",
    "air purification",
    "semiconductor",
    "packaging",
    "thermal management",
    "wall-plug efficiency",
    "reliability",
]


@dataclass(frozen=True)
class Settings:
    supabase_url: str
    supabase_service_role_key: str
    tavily_api_key: str
    groq_api_key: str
    groq_model: str = "llama-3.1-70b-versatile"


def load_settings() -> Settings:
    load_dotenv(override=False)

    supabase_url = os.getenv("SUPABASE_URL", "").strip()
    supabase_service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip()
    tavily_api_key = os.getenv("TAVILY_API_KEY", "").strip()
    groq_api_key = os.getenv("GROQ_API_KEY", "").strip()
    groq_model = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile").strip()

    missing = []
    if not supabase_url:
        missing.append("SUPABASE_URL")
    if not supabase_service_role_key:
        missing.append("SUPABASE_SERVICE_ROLE_KEY")
    if not tavily_api_key:
        missing.append("TAVILY_API_KEY")
    if not groq_api_key:
        missing.append("GROQ_API_KEY")

    if missing:
        missing_list = ", ".join(missing)
        raise ValueError(f"Missing required environment variables: {missing_list}")

    return Settings(
        supabase_url=supabase_url,
        supabase_service_role_key=supabase_service_role_key,
        tavily_api_key=tavily_api_key,
        groq_api_key=groq_api_key,
        groq_model=groq_model,
    )
