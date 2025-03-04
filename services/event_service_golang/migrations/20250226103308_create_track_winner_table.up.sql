CREATE TABLE track_winner
(
    track_id      INT     NOT NULL REFERENCES track (id),
    track_team_id INT     NOT NULL REFERENCES track_team (id),
    place         INT,
    is_awardee    BOOLEAN NOT NULL DEFAULT FALSE
);