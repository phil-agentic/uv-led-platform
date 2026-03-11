import { createClient, SupabaseClient } from "@supabase/supabase-js";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || "";
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || "";

let supabase: SupabaseClient | null = null;
if (supabaseUrl && supabaseAnonKey) {
  supabase = createClient(supabaseUrl, supabaseAnonKey);
}

export { supabase };

export function hasSupabaseConfig() {
  return Boolean(supabaseUrl && supabaseAnonKey);
}

export async function getLatestResearch(limit = 10) {
  if (!supabase) return [];
  const { data } = await supabase
    .from("research_items")
    .select("*")
    .order("created_at", { ascending: false })
    .limit(limit);
  return data || [];
}

export async function getLatestHotTopic() {
  if (!supabase) return null;
  const { data } = await supabase
    .from("hot_topics")
    .select("*")
    .order("created_at", { ascending: false })
    .limit(1)
    .single();
  return data;
}

export async function getResearchCount(): Promise<number> {
  if (!supabase) return 0;
  const { count, error } = await supabase
    .from("research_items")
    .select("*", { count: "exact", head: true });
  return count || 0;
}

export async function getPatentCount(): Promise<number> {
  if (!supabase) return 0;
  const { count, error } = await supabase
    .from("research_items")
    .select("*", { count: "exact", head: true })
    .or("title.ilike.%patent%,title.ilike.%intellectual property%,source.ilike.%google.com%,source.ilike.%wipo%");
  return count || 0;
}

export async function getDiscoveryStats(): Promise<number[]> {
  if (!supabase) return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
  const { data, error } = await supabase
    .from("research_items")
    .select("created_at")
    .order("created_at", { ascending: false });

  if (!data) return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

  // Group by day (last 10 days)
  const stats = new Array(10).fill(0);
  const now = new Date();

  data.forEach((item: any) => {
    const d = new Date(item.created_at);
    const diffTime = Math.abs(now.getTime() - d.getTime());
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
    if (diffDays < 10) {
      stats[9 - diffDays]++;
    }
  });

  return stats;
}
