CREATE TABLE date
(
    id         SERIAL PRIMARY KEY,
    date_start timestamptz NOT NULL,
    date_end   timestamptz NOT NULL,
    created_at timestamptz DEFAULT now(),
    updated_at timestamptz DEFAULT now() ON UPDATE now()
);