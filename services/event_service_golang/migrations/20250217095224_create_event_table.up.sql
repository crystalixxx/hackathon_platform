CREATE TABLE event
(
    id            SERIAL PRIMARY KEY,
    title         VARCHAR(255) NOT NULL,
    description   TEXT,
    redirect_link TEXT         NOT NULL,
    date_id       INT          NOT NULL REFERENCES date (id),
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trigger_event_locations_updated_at
    BEFORE UPDATE ON event
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
