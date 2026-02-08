

create table if not exists todos (
    id uuid primary key,
    title text not null,
    completed_date timestamp with time zone,
    created_on timestamp with time zone,
    updated_on timestamp with time zone
);


insert into migrations (seq, description) values ('0001', 'Creating Todos');
