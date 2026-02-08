

create table if not exists migrations (
    seq varchar(255) primary key,
    description text,
    applied_at timestamp with time zone default now()
);