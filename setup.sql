
CREATE TABLE IF NOT EXISTS channels (
  channel_id       BIGINT PRIMARY KEY,
  banner           VARCHAR,
  name             VARCHAR,
  username         VARCHAR,
  description      TEXT,
  awards           JSON,
  subscribers      INT,
  balance          BIGINT,
  views            BIGINT,
  location         VARCHAR,
  genre            VARCHAR,
  created_at       TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS drafts (
  draft_id         SERIAL PRIMARY KEY,
  channel_id       BIGINT REFERENCES channels (channel_id),
  status           VARCHAR,
  recorded         BOOLEAN,
  edited           BOOLEAN,
  recorded_at      TIMESTAMPTZ,
  edited_at        TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS videos (
  video_id         SERIAL PRIMARY KEY,
  channel_id       BIGINT REFERENCES channels (channel_id),
  draft_id         INT REFERENCES drafts (draft_id),
  name             VARCHAR,
  description      VARCHAR,
  status           VARCHAR,
  subscribers      INT,
  money            INT,
  views            INT,
  likes            INT,
  dislikes         INT,
  uploaded_at      TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS items (
  item_id          SERIAL PRIMARY KEY,
  channel_id       BIGINT REFERENCES channels (channel_id),
  name             VARCHAR,
  count            INT
);

CREATE TABLE IF NOT EXISTS guilds (
  guild_id         BIGINT PRIMARY KEY,
  prefix           VARCHAR
);

CREATE TABLE IF NOT EXISTS commands (
  command_id       BIGSERIAL PRIMARY KEY,
  guild            BIGINT,
  channel          BIGINT,
  author           BIGINT,
  name             VARCHAR,
  timestamp        TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS botbans (
  botban_id        BIGINT PRIMARY KEY,
  reason           TEXT,
  banned_at        TIMESTAMPTZ
);
