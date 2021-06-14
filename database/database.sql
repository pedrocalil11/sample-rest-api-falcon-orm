CREATE TABLE player (
    id                          SERIAL PRIMARY KEY,
    player_key                  CHAR(36) NOT NULL,
    name                        VARCHAR(255) NOT NULL,
    created_at                  TIMESTAMP NOT NULL DEFAULT(NOW()),
    UNIQUE (player_key)
);

CREATE TABLE sample_round (
    id                          SERIAL PRIMARY KEY,
    sample_round_key            CHAR(36) NOT NULL,
    name                        VARCHAR(255) NOT NULL,
    start_date                  TIMESTAMP NOT NULL,
    end_date                    TIMESTAMP,
    created_at                  TIMESTAMP NOT NULL DEFAULT(NOW()),
    UNIQUE (name)
);

CREATE TABLE participant (
    id                          SERIAL PRIMARY KEY,
    sample_round_id             INTEGER NOT NULL REFERENCES sample_round(id),
    player_id                   INTEGER NOT NULL REFERENCES player(id),
    subscription_date           TIMESTAMP NOT NULL,
    created_at                  TIMESTAMP NOT NULL DEFAULT(NOW()),
    UNIQUE (sample_round_id, player_id)
);