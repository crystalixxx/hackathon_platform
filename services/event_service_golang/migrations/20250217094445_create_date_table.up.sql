CREATE TABLE date
(
    id         SERIAL PRIMARY KEY,
    date_start timestamptz NOT NULL,
    date_end   timestamptz NOT NULL,
    created_at timestamptz DEFAULT now(),
    updated_at timestamptz DEFAULT now(),
    CONSTRAINT chk_date_range CHECK (date_end > date_start)
);

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_dates_updated_at
    BEFORE UPDATE ON date
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
