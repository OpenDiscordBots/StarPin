CREATE TABLE IF NOT EXISTS Starboards (
    channel_id      BIGINT PRIMARY KEY,
    emoji           VARCHAR(255) NOT NULL DEFAULT '⭐',
    required_stars  INT NOT NULL DEFAULT 5
);

CREATE TABLE IF NOT EXISTS StarboardMessages (
    id              BIGINT PRIMARY KEY,
    channel_id      BIGINT NOT NULL
);
