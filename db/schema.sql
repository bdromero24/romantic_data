CREATE TABLE IF NOT EXISTS messages (
    id BIGSERIAL PRIMARY KEY,
    source VARCHAR(50) NOT NULL,
    sender TEXT NOT NULL,
    message TEXT,
    message_normalized TEXT,
    timestamp TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_messages_source_sender_message_timestamp
        UNIQUE (source, sender, message, timestamp)
);

CREATE INDEX IF NOT EXISTS idx_messages_timestamp
    ON messages (timestamp);

CREATE INDEX IF NOT EXISTS idx_messages_sender
    ON messages (sender);

CREATE INDEX IF NOT EXISTS idx_messages_source
    ON messages (source);

CREATE INDEX IF NOT EXISTS idx_messages_source_timestamp
    ON messages (source, timestamp);

CREATE INDEX IF NOT EXISTS idx_messages_sender_timestamp
    ON messages (sender, timestamp);

CREATE TABLE IF NOT EXISTS logs (
    id BIGSERIAL PRIMARY KEY,
    error_type VARCHAR(100) NOT NULL,
    error_message TEXT NOT NULL,
    module_name VARCHAR(100),
    function_name VARCHAR(100),
    severity VARCHAR(50) NOT NULL DEFAULT 'CRITICAL',
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_logs_timestamp
    ON logs (timestamp);

CREATE INDEX IF NOT EXISTS idx_logs_error_type
    ON logs (error_type);

CREATE INDEX IF NOT EXISTS idx_logs_severity
    ON logs (severity);
