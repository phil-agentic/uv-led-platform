import json
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional, TypedDict
from urllib.parse import urlparse

from langchain_groq import ChatGroq
from langgraph.graph import END, StateGraph
from tavily import TavilyClient

from .config import DEFAULT_KEYWORDS, load_settings
from .db import (
    fetch_pending_forum_messages,
    fetch_recent_benchmarks,
    fetch_recent_research,
    insert_forum_reply,
    insert_hot_topic,
    mark_forum_message_drafted,
    upsert_research_items,
)


class GraphState(TypedDict, total=False):
    query_terms: List[str]
    since_date: str
    research_items: List[Dict[str, Any]]
    hot_topics_markdown: str
    moderation_drafts: List[Dict[str, Any]]


def build_graph():
    graph = StateGraph(GraphState)
    graph.add_node("researcher", researcher_node)
    graph.add_node("content_manager", content_manager_node)
    graph.add_node("moderator", moderator_node)
    graph.set_entry_point("researcher")
    graph.add_edge("researcher", "content_manager")
    graph.add_edge("content_manager", "moderator")
    graph.add_edge("moderator", END)
    return graph.compile()


def researcher_node(state: GraphState) -> Dict[str, Any]:
    settings = load_settings()
    client = TavilyClient(api_key=settings.tavily_api_key)

    query_terms = state.get("query_terms") or DEFAULT_KEYWORDS
    since_date = state.get("since_date")

    collected: List[Dict[str, Any]] = []
    for term in query_terms:
        query = f"UV LED {term}"
        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=3,
            include_answer=False,
            include_raw_content=False,
        )
        for result in response.get("results", []):
            item = _normalize_result(result)
            if not item:
                continue
            if since_date and not _is_newer_or_unknown(item.get("published_at"), since_date):
                continue
            collected.append(item)

    deduped: Dict[str, Dict[str, Any]] = {}
    for item in collected:
        deduped[item["url"]] = item

    items = list(deduped.values())
    upsert_research_items(items)

    return {"research_items": items}


def content_manager_node(state: GraphState) -> Dict[str, Any]:
    settings = load_settings()
    items = state.get("research_items") or []
    if not items:
        return {"hot_topics_markdown": ""}

    sources = [
        {
            "title": item.get("title"),
            "url": item.get("url"),
            "source": item.get("source"),
            "published_at": item.get("published_at"),
        }
        for item in items
    ]

    llm = ChatGroq(
        groq_api_key=settings.groq_api_key,
        model=settings.groq_model,
        temperature=0.2,
        max_tokens=1200,
    )

    prompt = _build_hot_topics_prompt(items[:20])
    response = llm.invoke(prompt)
    markdown = response.content.strip()

    week_start = _week_start(date.today()).isoformat()
    insert_hot_topic(week_start, markdown, sources)

    return {"hot_topics_markdown": markdown}


def moderator_node(state: GraphState) -> Dict[str, Any]:
    settings = load_settings()
    pending = fetch_pending_forum_messages()
    if not pending:
        return {"moderation_drafts": []}

    research_context = fetch_recent_research(limit=12)
    benchmark_context = fetch_recent_benchmarks(limit=6)

    llm = ChatGroq(
        groq_api_key=settings.groq_api_key,
        model=settings.groq_model,
        temperature=0.3,
        max_tokens=1200,
    )

    drafts: List[Dict[str, Any]] = []
    for message in pending:
        prompt = _build_moderation_prompt(
            question=message.get("message", ""),
            research_context=research_context,
            benchmark_context=benchmark_context,
        )
        response = llm.invoke(prompt)
        draft = response.content.strip()

        insert_forum_reply(message["id"], draft)
        mark_forum_message_drafted(message["id"])
        drafts.append({"forum_message_id": message["id"], "draft_markdown": draft})

    return {"moderation_drafts": drafts}


def _normalize_result(result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    url = result.get("url")
    if not url:
        return None

    title = result.get("title") or "Untitled"
    content = result.get("content") or result.get("snippet") or ""
    published_at = result.get("published_date") or result.get("published_at")
    source = result.get("source") or _domain_from_url(url)

    return {
        "title": title,
        "url": url,
        "source": source,
        "published_at": published_at,
        "summary": content[:400],
        "raw_json": result,
    }


def _domain_from_url(url: str) -> str:
    parsed = urlparse(url)
    return parsed.netloc or "unknown"


def _is_newer_or_unknown(published_at: Optional[str], since_date: str) -> bool:
    if not published_at:
        return True
    try:
        published = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
        since = datetime.fromisoformat(since_date)
        return published >= since
    except ValueError:
        return True


def _week_start(day: date) -> date:
    return day - timedelta(days=day.weekday())


def _build_hot_topics_prompt(items: List[Dict[str, Any]]) -> str:
    payload = [
        {
            "title": item.get("title"),
            "url": item.get("url"),
            "summary": item.get("summary"),
            "published_at": item.get("published_at"),
            "source": item.get("source"),
        }
        for item in items
    ]

    return (
        "You are an expert UV LED analyst. Summarize the latest findings into a Markdown "
        "weekly digest for the Hot-Topics section. Avoid hype and focus on wall-plug "
        "efficiency, wavelength stability, and thermal management when relevant.\n\n"
        "Output format:\n"
        "## Hot Topics\n"
        "- Bullet list of key findings\n"
        "\n"
        "## Sources\n"
        "- Title - URL\n\n"
        "Only use the provided sources. Do not invent data.\n\n"
        f"Sources JSON:\n{json.dumps(payload, indent=2)}"
    )


def _build_moderation_prompt(
    question: str,
    research_context: List[Dict[str, Any]],
    benchmark_context: List[Dict[str, Any]],
) -> str:
    return (
        "You are a friendly-but-expert UV LED forum moderator. Draft a helpful response "
        "that cites sources for technical claims. If data is insufficient, say so and ask "
        "for clarification.\n\n"
        f"Question:\n{question}\n\n"
        "Recent research items:\n"
        f"{json.dumps(research_context, indent=2)}\n\n"
        "Recent benchmarks:\n"
        f"{json.dumps(benchmark_context, indent=2)}\n\n"
        "Respond in Markdown with citations in the form (URL)."
    )
