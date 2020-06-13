create table if not exists users (
    user_id bigint primary key,
    money bigint,
    commands int default 0
);

create table if not exists channels (
    channel_id serial primary key,
    user_id bigint references users (user_id),
    name varchar(55),
    description text,
    subscribers bigint,
    total_views bigint,
    category varchar(30),
    created_at bigint
);

create table if not exists videos (
    video_id serial primary key,
    channel_id int references channels (channel_id),
    name varchar(55),
    description text,
    status varchar(30),
    new_subscribers bigint,
    new_money bigint default 0,
    views bigint,
    likes bigint,
    dislikes bigint,
    subscriber_cap bigint,
    iteration int,
    last_updated bigint,
    uploaded_at bigint
);

create table if not exists guilds (
    guild_id bigint primary key,
    prefix varchar(15),
    commands bigint default 0
);

create table if not exists subscriptions (
    user_id bigint references users (user_id),
    channel_id int references channels (channel_id)
);

create table if not exists votes (
    user_id bigint references users (user_id),
    timestamp bigint
);

create table if not exists botbans (
    user_id bigint primary key
);

create table if not exists awards (
    channel_id int references channels (channel_id),
    award text
);

create table if not exists warns (
    warn_id serial primary key,
    user_id bigint,
    moderator bigint,
    timestamp bigint,
    warning text
);

create table if not exists vote_reminders (
    user_id bigint primary key,
    toggle boolean,
    last_reminded bigint default 0,
    last_voted bigint
);

create table if not exists upload_reminders (
    channel_id bigint primary key,
    toggle boolean,
    last_reminded bigint default 0,
    last_uploaded bigint
);
