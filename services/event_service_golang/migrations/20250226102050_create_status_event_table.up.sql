CREATE TABLE status_event
(
    event_id  INT NOT NULL REFERENCES event (id),
    status_id INT NOT NULL REFERENCES status (id),
    PRIMARY KEY (status_id, event_id)
);