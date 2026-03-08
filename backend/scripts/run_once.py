import argparse
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.config import DEFAULT_KEYWORDS
from app.graph import build_graph


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the UV LED research graph once.")
    parser.add_argument(
        "--since",
        dest="since_date",
        default=None,
        help="ISO date (YYYY-MM-DD). Defaults to 7 days ago.",
    )
    parser.add_argument(
        "--keywords",
        dest="keywords",
        default=None,
        help="Comma-separated keywords. Defaults to built-in list.",
    )
    args = parser.parse_args()

    since_date = args.since_date or (date.today() - timedelta(days=7)).isoformat()
    keywords = (
        [k.strip() for k in args.keywords.split(",") if k.strip()]
        if args.keywords
        else DEFAULT_KEYWORDS
    )

    graph = build_graph()
    result = graph.invoke(
        {
            "query_terms": keywords,
            "since_date": since_date,
        }
    )

    print("Run complete.")
    print(f"Research items: {len(result.get('research_items', []))}")
    print("Hot topics generated." if result.get("hot_topics_markdown") else "No hot topics.")
    print(f"Moderation drafts: {len(result.get('moderation_drafts', []))}")


if __name__ == "__main__":
    main()
