import { getLatestResearch, getLatestHotTopic, getResearchCount, hasSupabaseConfig } from "../lib/supabaseClient";
import ResearchList from "./components/ResearchList";
import ReactMarkdown from "react-markdown";
import { Activity, Database, Flame, Search } from "lucide-react";

const sections = [
  {
    title: "History",
    description:
      "Trace major milestones in UV LED development, with verified sources and performance shifts.",
  },
  {
    title: "Technical",
    description:
      "WPE, wavelength stability, and thermal management benchmarks curated from papers and datasheets.",
  },
  {
    title: "Products",
    description:
      "Manufacturer specs cross-referenced with independent validation for objective comparisons.",
  },
  {
    title: "Hot-Topics",
    description:
      "Weekly digest of UV LED research, patents, and product announcements.",
  },
];

export default async function Page() {
  const supabaseReady = hasSupabaseConfig();
  const latestResearch = await getLatestResearch(5);
  const hotTopic = await getLatestHotTopic();
  const totalCount = await getResearchCount();

  return (
    <main className="page">
      <section className="hero">
        <span className="tag">UV LED Intelligence</span>
        <h1>Autonomous UV LED Knowledge Platform</h1>
        <p>
          Centralize UV LED research, benchmarks, and expert community responses in
          one continuously updated workspace.
        </p>
      </section>

      <div className="stats-grid">
        <div className="stat-card">
          <Database className="stat-icon" size={20} />
          <div className="stat-value">{totalCount}</div>
          <div className="stat-label">Total Items</div>
        </div>
        <div className="stat-card">
          <Activity className="stat-icon" size={20} />
          <div className="stat-value">+12%</div>
          <div className="stat-label">Weekly Growth</div>
        </div>
        <div className="stat-card">
          <Search className="stat-icon" size={20} />
          <div className="stat-value">Real-time</div>
          <div className="stat-label">Monitoring</div>
        </div>
        <div className="stat-card">
          <Flame className="stat-icon" size={20} />
          <div className="stat-value">Hot</div>
          <div className="stat-label">Insights</div>
        </div>
      </div>

      <section className="live-data">
        <div className="card full-width">
          <div className="card-header">
            <h3>Latest Weekly Digest</h3>
            <span className="live-badge">Live Analysis</span>
          </div>
          {hotTopic ? (
            <div className="markdown-content">
              <ReactMarkdown>{hotTopic.markdown}</ReactMarkdown>
            </div>
          ) : (
            <p>No monthly digest generated yet. Run the research loop to see updates!</p>
          )}
        </div>
      </section>

      <section className="grid">
        <div className="card">
          <h3>Recent Research</h3>
          <ResearchList items={latestResearch} />
        </div>
        <div className="card">
          <h3>Research Velocity</h3>
          <div className="graph-container">
            {[40, 70, 45, 90, 65, 80, 55, 95, 75, 100].map((h, i) => (
              <div
                key={i}
                className="graph-bar"
                style={{ height: `${h}%` }}
              />
            ))}
          </div>
          <p style={{ marginTop: '1rem', fontSize: '0.8rem' }}>Discovery rate per day (last 10 days)</p>
        </div>
      </section>

      <section className="footer">
        <p>Currently monitoring <strong>{totalCount}</strong> research items in the pipeline.</p>
        <p>
          Supabase status: {supabaseReady ? "Configured" : "Not configured"}
        </p>
      </section>
    </main>
  );
}
