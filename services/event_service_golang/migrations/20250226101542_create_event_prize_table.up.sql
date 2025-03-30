CREATE TABLE event_prize
(
    id            SERIAL PRIMARY KEY,
    place         INT          NOT NULL,
    primary_prize VARCHAR(255) NOT NULL,
    description   TEXT,
    icon_url      TEXT         NOT NULL,
    event_id      INT          NOT NULL REFERENCES event (id),
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
);