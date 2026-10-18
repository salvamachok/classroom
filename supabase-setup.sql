
create table if not exists public.class_monitor_state (
    id integer primary key check (id = 1),
    data jsonb not null default
    '{"students":[],"attendance":{},"work":[],"marks":[]}'::jsonb,
    updated_at timestamptz not null default now()
);

insert into public.class_monitor_state (id)
values (1)
on conflict (id) do nothing;

alter table public.class_monitor_state
enable row level security;

revoke all on public.class_monitor_state
from anon, authenticated;
