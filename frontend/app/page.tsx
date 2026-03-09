import { getLatestResearch, getLatestHotTopic, getResearchCount, hasSupabaseConfig } from "../lib/supabaseClient";
import ResearchList from "./components/ResearchList";

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

      <section className="live-data">
        <div className="card full-width">
          <h3>Latest Weekly Digest</h3>
          {hotTopic ? (
            <div className="markdown-content">
              {hotTopic.markdown}
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
          <h3>Benchmarks</h3>
          <p>Integration pending. Wall-plug efficiency, wavelength stability, and thermal management metrics.</p>
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
