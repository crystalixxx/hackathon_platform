CREATE TABLE track_role
(
    track_id            INT     NOT NULL REFERENCES track (id),
    user_id             INT     NOT NULL,
    can_view_results    BOOLEAN NOT NULL DEFAULT FALSE,
    can_view_statistics BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (track_id, user_id)
);