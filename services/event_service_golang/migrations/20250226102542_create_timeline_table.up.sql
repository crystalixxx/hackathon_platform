CREATE TABLE timeline
(
    id                 SERIAL PRIMARY KEY,
    title              VARCHAR(255) NOT NULL,
    description        TEXT,
    deadline           TIMESTAMP,
    is_blocking        BOOLEAN      NOT NULL DEFAULT FALSE,
    track_id           INT          NOT NULL REFERENCES track (id),
    timeline_status_id INT          NOT NULL REFERENCES timeline_status (id)
);