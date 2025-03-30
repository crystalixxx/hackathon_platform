CREATE TABLE track_team
(
    id        SERIAL PRIMARY KEY,
    team_id   INT     NOT NULL,
    track_id  INT     NOT NULL REFERENCES track (id),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);