CREATE TABLE status_track
(
    track_id  INT NOT NULL REFERENCES track (id),
    status_id INT NOT NULL REFERENCES status (id),
    PRIMARY KEY (status_id, track_id)
);