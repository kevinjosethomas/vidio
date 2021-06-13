
CREATE TABLE IF NOT EXISTS channels (
  channel_id       BIGINT PRIMARY KEY,
  banner           VARCHAR,
  name             VARCHAR NOT NULL,
  vanity           VARCHAR,
  description      TEXT NOT NULL,
  awards           SMALLINT[],
  subscribers      INT NOT NULL DEFAULT 0,
  balance          BIGINT NOT NULL DEFAULT 0,
  views            BIGINT NOT NULL DEFAULT 0,
  genre            VARCHAR NOT NULL,
  created_at       TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS drafts (
  draft_id         SERIAL PRIMARY KEY,
  channel_id       BIGINT REFERENCES channels (channel_id),
  status           SMALLINT,
  recorded         BOOLEAN,
  edited           BOOLEAN,
  recorded_at      TIMESTAMPTZ,
  edited_at        TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS videos (
  video_id         SERIAL PRIMARY KEY,
  channel_id       BIGINT REFERENCES channels (channel_id),
  draft_id         INT REFERENCES drafts (draft_id),
  name             VARCHAR NOT NULL,
  description      VARCHAR NOT NULL,
  status           SMALLINT NOT NULL,
  subscribers      INT NOT NULL DEFAULT 0,
  money            INT NOT NULL DEFAULT 0,
  views            INT NOT NULL DEFAULT 0,
  likes            INT NOT NULL DEFAULT 0,
  dislikes         INT NOT NULL DEFAULT 0,
  uploaded_at      TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS items (
  item_id          SERIAL PRIMARY KEY,
  channel_id       BIGINT REFERENCES channels (channel_id),
  name             VARCHAR NOT NULL,
  count            INT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS guilds (
  guild_id         BIGINT PRIMARY KEY,
  prefix           VARCHAR
);

CREATE TABLE IF NOT EXISTS commands (
  command_id       BIGSERIAL PRIMARY KEY,
  guild            BIGINT,
  channel          BIGINT,
  author           BIGINT NOT NULL,
  name             VARCHAR NOT NULL,
  timestamp        TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS botbans (
  botban_id        BIGINT PRIMARY KEY,
  reason           TEXT,
  banned_at        TIMESTAMPTZ NOT NULL
);
