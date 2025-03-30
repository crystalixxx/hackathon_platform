CREATE TABLE status
(
    id          SERIAL PRIMARY KEY,
    title       VARCHAR(255) NOT NULL,
    description TEXT,
    created_at  timestamptz  NOT NULL DEFAULT now(),
    updated_at  timestamptz  NOT NULL DEFAULT now()
);

CREATE TRIGGER trigger_update_status_updated_at
    BEFORE UPDATE ON status
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();