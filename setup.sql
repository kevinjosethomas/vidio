
CREATE TABLE IF NOT EXISTS genres (
  genre            VARCHAR PRIMARY KEY,
  emoji            VARCHAR UNIQUE
);

CREATE TABLE IF NOT EXISTS channels (
  id               BIGINT PRIMARY KEY,
  banner           VARCHAR,
  name             VARCHAR,
  username         VARCHAR,
  description      TEXT,
  awards           JSON,
  subscribers      INT,
  balance          BIGINT,
  views            BIGINT,
  location         VARCHAR,
  genre            VARCHAR REFERENCES genres (genre),
  created_at       TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS drafts (
  id               SERIAL PRIMARY KEY,
  channel_id       BIGINT REFERENCES channels (id),
  status           VARCHAR,
  recorded         BOOLEAN,
  edited           BOOLEAN,
  recorded_at      TIMESTAMPTZ,
  edited_at        TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS videos (
  id               SERIAL PRIMARY KEY,
  channel_id       BIGINT REFERENCES channels (id),
  draft_id         INT REFERENCES drafts (id),
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
  id               SERIAL PRIMARY KEY,
  channel_id       BIGINT REFERENCES channels (id),
  name             VARCHAR,
  count            INT
);

CREATE TABLE IF NOT EXISTS guilds (
  id               BIGINT PRIMARY KEY,
  prefix           VARCHAR
);

CREATE TABLE IF NOT EXISTS commands (
  id               BIGSERIAL PRIMARY KEY,
  guild            BIGINT,
  channel          BIGINT,
  author           BIGINT,
  name             VARCHAR,
  timestamp        TIMESTAMPTZ
);

INSERT INTO genres (genre, emoji) VALUES ('Film & Animation', '📸');
INSERT INTO genres (genre, emoji) VALUES ('Autos & Vehicles', '🏎️');
INSERT INTO genres (genre, emoji) VALUES ('Music', '🎵');
INSERT INTO genres (genre, emoji) VALUES ('Pets & Animals', '🐶');
INSERT INTO genres (genre, emoji) VALUES ('Sports', '🏀');
INSERT INTO genres (genre, emoji) VALUES ('Travel & Events', '✈️');
INSERT INTO genres (genre, emoji) VALUES ('Gaming', '🎮');
INSERT INTO genres (genre, emoji) VALUES ('People & Blogs', '👥');
INSERT INTO genres (genre, emoji) VALUES ('Comedy', '🎭');
INSERT INTO genres (genre, emoji) VALUES ('Entertainment', '📺');
INSERT INTO genres (genre, emoji) VALUES ('News & Politics', '📰');
INSERT INTO genres (genre, emoji) VALUES ('Howto & Style', '👚');
INSERT INTO genres (genre, emoji) VALUES ('Education', '📖');
INSERT INTO genres (genre, emoji) VALUES ('Science & Technology', '🧪');
INSERT INTO genres (genre, emoji) VALUES ('Nonprofits & Activism', '💸');
