CREATE TABLE event_location
(
    location_id INT NOT NULL REFERENCES location (id),
    event_id    INT NOT NULL REFERENCES event (id),
    PRIMARY KEY (location_id, event_id)
);