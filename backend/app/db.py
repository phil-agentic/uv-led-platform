from functools import lru_cache
from typing import Any, Dict, List

from supabase import Client, create_client

from .config import load_settings


@lru_cache(maxsize=1)
def get_supabase() -> Client:
    settings = load_settings()
    return create_client(settings.supabase_url, settings.supabase_service_role_key)


def upsert_research_items(items: List[Dict[str, Any]]) -> None:
    if not items:
        return
    supabase = get_supabase()
    supabase.table("research_items").upsert(items, on_conflict="url").execute()


def insert_hot_topic(week_start: str, markdown: str, sources: List[Dict[str, Any]]) -> None:
    supabase = get_supabase()
    supabase.table("hot_topics").insert(
        {
            "week_start": week_start,
            "markdown": markdown,
            "sources_json": sources,
        }
    ).execute()


def fetch_pending_forum_messages() -> List[Dict[str, Any]]:
    supabase = get_supabase()
    response = (
        supabase.table("forum_messages")
        .select("*")
        .eq("status", "pending")
        .order("created_at", desc=False)
        .execute()
    )
    return response.data or []


def insert_forum_reply(message_id: str, draft_markdown: str) -> None:
    supabase = get_supabase()
    supabase.table("forum_replies").insert(
        {
            "forum_message_id": message_id,
            "draft_markdown": draft_markdown,
            "status": "draft",
        }
    ).execute()


def mark_forum_message_drafted(message_id: str) -> None:
    supabase = get_supabase()
    supabase.table("forum_messages").update({"status": "drafted"}).eq("id", message_id).execute()


def fetch_recent_research(limit: int = 10) -> List[Dict[str, Any]]:
    supabase = get_supabase()
    response = (
        supabase.table("research_items")
        .select("title,summary,url,published_at,source")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return response.data or []


def fetch_recent_benchmarks(limit: int = 10) -> List[Dict[str, Any]]:
    supabase = get_supabase()
    response = (
        supabase.table("benchmarks")
        .select("product_name,wavelength_nm,wpe,thermal_notes,source_url,created_at")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return response.data or []


def fetch_discovery_stats() -> List[Dict[str, Any]]:
    """
    Fetch counts of new research items per day for the last 10 days.
    """
    supabase = get_supabase()
    response = (
        supabase.table("research_items")
        .select("created_at")
        .order("created_at", desc=True)
        .execute()
    )
    return response.data or []


def fetch_patent_count() -> int:
    """
    Fetch the count of research items that are patents.
    """
    supabase = get_supabase()
    response = (
        supabase.table("research_items")
        .select("id", count="exact")
        .or_("title.ilike.%patent%,title.ilike.%intellectual property%,source.ilike.%google.com%,source.ilike.%wipo%")
        .execute()
    )
    return response.count or 0
