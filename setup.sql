
CREATE TABLE IF NOT EXISTS channels (
  user_id BIGINT PRIMARY KEY,
  banner VARCHAR(205),
  name VARCHAR(37),
  slug VARCHAR(37),
  description VARCHAR(205),
  awards JSON,
  subscribers INT,
  balance BIGINT,
  views BIGINT,
  location VARCHAR(37),
  genre VARCHAR(47),
  created_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS videos (
  video_id SERIAL PRIMARY KEY,
  user_id BIGINT,
  name VARCHAR(55),
  description VARCHAR(205),
  status VARCHAR(15),
  subscribers INT,
  money INT,
  views INT,
  likes INT,
  dislikes INT,
  uploaded_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS drafts (
  draft_id SERIAL PRIMARY KEY,
  user_id BIGINT REFERENCES channels (user_id),
  status VARCHAR(15),
  recorded BOOLEAN,
  edited BOOLEAN,
  recorded_at TIMESTAMPTZ,
  edited_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS items (
  user_id BIGINT PRIMARY KEY REFERENCES channels (user_id),
  name VARCHAR(55)
);

CREATE TABLE IF NOT EXISTS guilds (
  guild_id BIGINT PRIMARY KEY,
  prefix VARCHAR(15),
  commands INT
);

CREATE TABLE IF NOT EXISTS users (
  user_id BIGINT PRIMARY KEY,
  commands INT
);

CREATE TABLE IF NOT EXISTS genres (
  emoji VARCHAR(37),
  genre VARCHAR(37)
);
