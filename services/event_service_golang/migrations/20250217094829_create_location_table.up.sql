CREATE TABLE location
(
    id         SERIAL PRIMARY KEY,
    title      VARCHAR(255) NOT NULL,
    created_at timestamptz  NOT NULL DEFAULT now(),
    updated_at timestamptz  NOT NULL DEFAULT now()
);

CREATE TRIGGER trigger_update_locations_updated_at
    BEFORE UPDATE
    ON location
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
