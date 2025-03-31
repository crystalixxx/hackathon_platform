CREATE TABLE location_track
(
    location_id INT NOT NULL REFERENCES location (id),
    track_id    INT NOT NULL REFERENCES track (id),
    PRIMARY KEY (location_id, track_id)
);