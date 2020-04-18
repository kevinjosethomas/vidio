-- Database Setup File


-- creates user table, which holes -
--      - user_id, the discord id of the user.
--      - money, the amount of money the user has.
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    money BIGINT
);


-- creates channels table which holds -
--      - user_id, the owner of the channel. References users.user_id
--      - channel_id, the auto incremented unique id (serial) of the channel.
--      - name, the name of the channel. (Max 50 characters)
--      - description, the description of the channel. (Max 250 characters)
--      - subscribers, the total number of subscribers of the channel.
--      - total_views, the total number of views the channel has received on all videos.
--      - category, the channel's topic/category.
--      - created_at, the date and time the channel was created.
CREATE TABLE IF NOT EXISTS channels (
    user_id BIGINT REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    channel_id SERIAL PRIMARY KEY,
    name VARCHAR(55),
    description TEXT,
    subscribers BIGINT,
    total_views BIGINT,
    category VARCHAR(30),
    created_at TIMESTAMP
);


-- creates videos table which holds -
--      - video_id, the auto incremented id (serial) of the video.
--      - channel_id, the channel that posted the video. References channels.channel_id
--      - name, the name of the video. (Maximum 50 characters)
--      - description, the description of the video. (Max 250 characters)
--      - status, the state of the video. Whether it was successful or not.
--      - new_subs, the total number of subscribers the video produced.
--      - views, the total number of views the video produced.
--      - likes, the total number of likes the video produced.
--      - dislikes, the total number of dislikes the video produced.
--      - last_percentage, the last added/subtracted percentage in the vloger algorithm.
--      - last_updated, the last time the statistics of the video were updated.
--      - uploaded_at, the date the video was uploaded.
CREATE TABLE IF NOT EXISTS videos (
    video_id SERIAL PRIMARY KEY,
    channel_id INT REFERENCES channels (channel_id) ON DELETE CASCADE ON UPDATE CASCADE,
    name VARCHAR(55),
    description TEXT,
    status VARCHAR(30),
    new_subs BIGINT,
    views BIGINT,
    likes BIGINT,
    dislikes BIGINT,
    iteration INT,
    last_percentage INT,
    last_updated TIMESTAMP,
    uploaded_at TIMESTAMP
);


-- creates subscribers table which holds -
--      - subscriber, the user that subscribed.
--      - channel, the channel that was subscribed to.
CREATE TABLE IF NOT EXISTS subscribers (
    subscriber BIGINT,
    channel INT REFERENCES channels (channel_id) ON DELETE CASCADE ON UPDATE CASCADE
);


-- creates guilds table which holds -
--      - guild_id, guild ids
--      - prefix, custom prefixes
CREATE TABLE IF NOT EXISTS guilds (
    guild_id BIGINT UNIQUE,
    prefix VARCHAR(15)
);


-- creates bans table which holds -
--      - user_id, banned user's id
CREATE TABLE IF NOT EXISTS bans (
    user_id BIGINT
);
