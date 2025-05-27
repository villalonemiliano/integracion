CREATE TABLE IF NOT EXISTS api_keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    requests_per_month INTEGER NOT NULL DEFAULT 10000,
    requests_this_month INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL,
    last_used_at TIMESTAMP,
    expires_at TIMESTAMP,
    CONSTRAINT unique_api_key UNIQUE (key),
    CONSTRAINT unique_email UNIQUE (email)
); 