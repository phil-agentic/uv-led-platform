create extension if not exists "uuid-ossp";

create table if not exists research_items (
  id uuid primary key default uuid_generate_v4(),
  title text not null,
  url text not null,
  source text,
  published_at timestamptz,
  summary text,
  raw_json jsonb,
  created_at timestamptz not null default now()
);

create unique index if not exists research_items_url_key on research_items (url);

create table if not exists hot_topics (
  id uuid primary key default uuid_generate_v4(),
  week_start date not null,
  markdown text not null,
  sources_json jsonb,
  created_at timestamptz not null default now()
);

create table if not exists benchmarks (
  id uuid primary key default uuid_generate_v4(),
  product_name text not null,
  wavelength_nm numeric,
  wpe numeric,
  thermal_notes text,
  source_url text,
  created_at timestamptz not null default now()
);

create table if not exists forum_messages (
  id uuid primary key default uuid_generate_v4(),
  user_id text,
  message text not null,
  status text not null default 'pending',
  created_at timestamptz not null default now()
);

create table if not exists forum_replies (
  id uuid primary key default uuid_generate_v4(),
  forum_message_id uuid not null references forum_messages(id) on delete cascade,
  draft_markdown text not null,
  status text not null default 'draft',
  created_at timestamptz not null default now()
);

create unique index if not exists forum_replies_message_key on forum_replies (forum_message_id);
