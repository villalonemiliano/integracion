CREATE TABLE IF NOT EXISTS plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    requests_per_second INTEGER NOT NULL,
    requests_per_month INTEGER NOT NULL,
    duration_days INTEGER NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_requests_per_second CHECK (requests_per_second > 0),
    CONSTRAINT valid_requests_per_month CHECK (requests_per_month > 0),
    CONSTRAINT valid_duration CHECK (duration_days > 0),
    CONSTRAINT valid_price CHECK (price >= 0)
); 