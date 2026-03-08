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

export async function getResearchCount() {
  if (!supabase) return 0;
  const { count } = await supabase
    .from("research_items")
    .select("*", { count: "exact", head: true });
  return count || 0;
}
