import sys
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from apscheduler.schedulers.blocking import BlockingScheduler

from app.config import DEFAULT_KEYWORDS
from app.graph import build_graph


def main() -> None:
    graph = build_graph()

    def run_job() -> None:
        since_date = (date.today() - timedelta(days=7)).isoformat()
        graph.invoke({"query_terms": DEFAULT_KEYWORDS, "since_date": since_date})
        print(f"Weekly research run completed at {datetime.now().isoformat(timespec='seconds')}.")

    scheduler = BlockingScheduler()
    scheduler.add_job(run_job, "interval", days=7, next_run_time=datetime.now())

    print("Scheduler started. Running every 7 days.")

    # Start a simple heartbeat server for Render
    import http.server
    import socketserver
    import threading
    import os

    def run_heartbeat():
        port = int(os.environ.get("PORT", 8080))
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"Heartbeat server running on port {port}")
            httpd.serve_forever()

    threading.Thread(target=run_heartbeat, daemon=True).start()

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")


if __name__ == "__main__":
    main()
