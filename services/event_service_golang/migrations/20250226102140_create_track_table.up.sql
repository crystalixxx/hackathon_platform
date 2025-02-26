CREATE TABLE track
(
    id             SERIAL PRIMARY KEY,
    title          VARCHAR(255) NOT NULL,
    description    TEXT,
    is_score_based BOOLEAN      NOT NULL DEFAULT FALSE,
    event_id       INT          NOT NULL REFERENCES event (id),
    date_id        INT          NOT NULL REFERENCES date (id)
);