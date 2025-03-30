CREATE TABLE team_action_status
(
    track_team_id   INT NOT NULL REFERENCES track_team (id),
    timeline_id     INT NOT NULL REFERENCES timeline (id),
    result_value    INT,
    resolution_link TEXT,
    notes           TEXT,
    competed_at     TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (track_team_id, timeline_id)
);