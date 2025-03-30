CREATE TABLE track_judge
(
    track_id INT NOT NULL REFERENCES track (id),
    judge_id INT NOT NULL,
    PRIMARY KEY (track_id, judge_id)
);