begin;

create table if not exists branch (
    id integer primary key,
    path text unique
);

create table if not exists album (
    id integer primary key,
    branch_id integer,
    path text,
    foreign key (branch_id) references branch(id)
);

create table if not exists album_entry (
    id integer primary key,
    album_id integer,
    path text,
    foreign key (album_id) references album(id)
);
                
create table if not exists tag (
    id integer primary key,
    name text unique
);

create table if not exists tag_hierarchy (
    parent_id integer,
    child_id integer
);
                
create table if not exists album_entry_tag_link (
    album_entry_id integer,
    tag_id integer,
    link_type text,
    foreign key (album_entry_id) references album_entry(id),
    foreign key (tag_id) references tag(id),
    check (link_type in ('include', 'exclude'))
);

commit;