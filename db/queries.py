"""Parameterized SQL queries for database access."""

from sqlalchemy import bindparam, text
from sqlalchemy.sql.elements import TextClause


INSERT_LOG_QUERY: TextClause = text(
    """
    INSERT INTO logs (
        error_type,
        error_message,
        module_name,
        function_name,
        severity
    )
    VALUES (
        :error_type,
        :error_message,
        :module_name,
        :function_name,
        :severity
    )
    """
)

COUNT_ALL_MESSAGES_QUERY: TextClause = text(
    """
    SELECT COUNT(*) AS message_count
    FROM messages
    """
)

COUNT_MESSAGES_BY_SOURCE_QUERY: TextClause = text(
    """
    SELECT source, COUNT(*) AS message_count
    FROM messages
    GROUP BY source
    ORDER BY message_count DESC
    """
)

COUNT_MESSAGES_BY_SENDER_QUERY: TextClause = text(
    """
    SELECT sender, COUNT(*) AS message_count
    FROM messages
    GROUP BY sender
    ORDER BY message_count DESC
    """
)

COUNT_MESSAGES_BY_DAY_QUERY: TextClause = text(
    """
    SELECT DATE_TRUNC('day', timestamp) AS message_day,
           COUNT(*) AS message_count
    FROM messages
    GROUP BY message_day
    ORDER BY message_day
    """
)

COUNT_MESSAGES_BY_HOUR_QUERY: TextClause = text(
    """
    SELECT EXTRACT(HOUR FROM timestamp) AS message_hour,
           COUNT(*) AS message_count
    FROM messages
    GROUP BY message_hour
    ORDER BY message_hour
    """
)

COUNT_KEYWORD_OCCURRENCES_QUERY: TextClause = text(
    """
    SELECT COUNT(*) AS occurrence_count
    FROM messages
    WHERE message_normalized ILIKE :keyword_pattern ESCAPE '\\'
       OR message ILIKE :keyword_pattern ESCAPE '\\'
    """
)

FETCH_MESSAGES_QUERY: TextClause = text(
    """
    SELECT
        id,
        source,
        sender,
        message,
        message_normalized,
        timestamp,
        created_at
    FROM messages
    WHERE (:source IS NULL OR source = :source)
      AND (:sender IS NULL OR sender = :sender)
      AND (:start_timestamp IS NULL OR timestamp >= :start_timestamp)
      AND (:end_timestamp IS NULL OR timestamp <= :end_timestamp)
    ORDER BY timestamp ASC, id ASC
    LIMIT :limit
    OFFSET :offset
    """
)

CHECK_DUPLICATE_MESSAGE_QUERY: TextClause = text(
    """
    SELECT EXISTS (
        SELECT 1
        FROM messages
        WHERE source = :source
          AND sender = :sender
          AND message IS NOT DISTINCT FROM :message
          AND timestamp = :timestamp
    ) AS is_duplicate
    """
)

INSERT_MESSAGE_QUERY: TextClause = text(
    """
    INSERT INTO messages (
        sender,
        message,
        message_normalized,
        timestamp,
        source
    )
    VALUES (
        :sender,
        :message,
        :message_normalized,
        :timestamp,
        :source
    )
    ON CONFLICT (source, sender, message, timestamp)
    DO NOTHING
    """
)

VALID_MESSAGE_FILTER = """
    message IS NOT NULL
    AND message_normalized IS NOT NULL
    AND BTRIM(message) <> ''
    AND BTRIM(message_normalized) <> ''
    AND LOWER(BTRIM(message_normalized)) NOT IN (
        'null',
        'none',
        'nan',
        'na',
        'n/a'
    )
"""

ROMANTIC_SUMMARY_QUERY: TextClause = text(
    f"""
    SELECT
        COUNT(*) AS total_messages,
        COUNT(DISTINCT DATE(timestamp)) AS total_conversation_days,
        MIN(timestamp) AS first_message_timestamp,
        MAX(timestamp) AS last_message_timestamp
    FROM messages
    WHERE {VALID_MESSAGE_FILTER}
    """
)

ROMANTIC_FIRST_MESSAGE_QUERY: TextClause = text(
    f"""
    SELECT id, sender, message, timestamp
    FROM messages
    WHERE {VALID_MESSAGE_FILTER}
    ORDER BY timestamp ASC, id ASC
    LIMIT 1
    """
)

ROMANTIC_MESSAGE_BY_ID_QUERY: TextClause = text(
    f"""
    SELECT id, sender, message, timestamp
    FROM messages
    WHERE {VALID_MESSAGE_FILTER}
      AND id = :message_id
    LIMIT 1
    """
)

ROMANTIC_MESSAGES_BY_IDS_QUERY: TextClause = text(
    f"""
    SELECT id, sender, message, timestamp, source
    FROM messages
    WHERE {VALID_MESSAGE_FILTER}
      AND id IN :message_ids
    """
).bindparams(bindparam("message_ids", expanding=True))

ROMANTIC_PATTERN_COUNT_QUERY: TextClause = text(
    f"""
    SELECT COUNT(*) AS occurrence_count
    FROM messages
    WHERE {VALID_MESSAGE_FILTER}
      AND message_normalized ~* :pattern
    """
)

ROMANTIC_HATER_WORD_COUNT_QUERY: TextClause = text(
    f"""
    SELECT COALESCE(SUM(regexp_count(message_normalized, :pattern, 1, 'i')), 0)
           AS total_odio
    FROM messages
    WHERE sender = :sender_name
      AND {VALID_MESSAGE_FILTER}
    """
)

ROMANTIC_FIRST_PATTERN_MESSAGE_QUERY: TextClause = text(
    f"""
    SELECT id, sender, message, timestamp
    FROM messages
    WHERE {VALID_MESSAGE_FILTER}
      AND message_normalized ~* :pattern
    ORDER BY timestamp ASC, id ASC
    LIMIT 1
    """
)

ROMANTIC_PATTERN_MESSAGES_QUERY: TextClause = text(
    f"""
    SELECT id, sender, message, timestamp
    FROM messages
    WHERE {VALID_MESSAGE_FILTER}
      AND message_normalized ~* :pattern
    ORDER BY timestamp ASC, id ASC
    LIMIT :limit
    """
)

ROMANTIC_PEAK_DAY_QUERY: TextClause = text(
    f"""
    SELECT DATE(timestamp) AS message_day,
           COUNT(*) AS message_count
    FROM messages
    WHERE {VALID_MESSAGE_FILTER}
    GROUP BY message_day
    ORDER BY message_count DESC, message_day ASC
    LIMIT 1
    """
)

ROMANTIC_PEAK_MONTH_QUERY: TextClause = text(
    f"""
    SELECT DATE_TRUNC('month', timestamp) AS message_month,
           COUNT(*) AS message_count
    FROM messages
    WHERE {VALID_MESSAGE_FILTER}
    GROUP BY message_month
    ORDER BY message_count DESC, message_month ASC
    LIMIT 1
    """
)

ROMANTIC_FAVORITE_HOUR_QUERY: TextClause = text(
    f"""
    SELECT EXTRACT(HOUR FROM timestamp)::INTEGER AS message_hour,
           COUNT(*) AS message_count
    FROM messages
    WHERE {VALID_MESSAGE_FILTER}
    GROUP BY message_hour
    ORDER BY message_count DESC, message_hour ASC
    LIMIT 1
    """
)

ROMANTIC_CONVERSATION_STARTER_QUERY: TextClause = text(
    f"""
    WITH first_messages_by_day AS (
        SELECT DISTINCT ON (DATE(timestamp))
            DATE(timestamp) AS message_day,
            sender
        FROM messages
        WHERE {VALID_MESSAGE_FILTER}
        ORDER BY DATE(timestamp), timestamp ASC, id ASC
    )
    SELECT sender,
           COUNT(*) AS conversation_start_count
    FROM first_messages_by_day
    GROUP BY sender
    ORDER BY conversation_start_count DESC, sender ASC
    LIMIT 1
    """
)

ROMANTIC_AVERAGE_DAILY_MESSAGES_QUERY: TextClause = text(
    f"""
    WITH daily_messages AS (
        SELECT DATE(timestamp) AS conversation_day,
               COUNT(*) AS total_messages
        FROM messages
        WHERE {VALID_MESSAGE_FILTER}
          AND timestamp IS NOT NULL
        GROUP BY conversation_day
    )
    SELECT COALESCE(AVG(total_messages)::numeric, 0) AS avg_daily_messages
    FROM daily_messages
    """
)

ROMANTIC_HOURLY_RHYTHM_QUERY: TextClause = text(
    f"""
    SELECT EXTRACT(HOUR FROM timestamp)::INTEGER AS label,
           COUNT(*) AS message_count
    FROM messages
    WHERE {VALID_MESSAGE_FILTER}
    GROUP BY label
    ORDER BY label ASC
    """
)

ROMANTIC_WEEKDAY_RHYTHM_QUERY: TextClause = text(
    f"""
    SELECT EXTRACT(ISODOW FROM timestamp)::INTEGER AS label,
           COUNT(*) AS message_count
    FROM messages
    WHERE {VALID_MESSAGE_FILTER}
    GROUP BY label
    ORDER BY label ASC
    """
)

ROMANTIC_MONTHLY_RHYTHM_QUERY: TextClause = text(
    f"""
    SELECT DATE_TRUNC('month', timestamp) AS label,
           COUNT(*) AS message_count
    FROM messages
    WHERE {VALID_MESSAGE_FILTER}
    GROUP BY label
    ORDER BY label ASC
    """
)

ROMANTIC_SENDER_RHYTHM_QUERY: TextClause = text(
    f"""
    SELECT sender AS label,
           COUNT(*) AS value
    FROM messages
    WHERE {VALID_MESSAGE_FILTER}
      AND sender IS NOT NULL
      AND BTRIM(sender) <> ''
      AND (:max_date IS NULL OR timestamp <= :max_date)
    GROUP BY sender
    ORDER BY value DESC
    """
)

ROMANTIC_WORD_COUNTS_QUERY: TextClause = text(
    f"""
    WITH tokens AS (
        SELECT regexp_split_to_table(message_normalized, '\\s+') AS token
        FROM messages
        WHERE {VALID_MESSAGE_FILTER}
    )
    SELECT token AS word,
           COUNT(*) AS word_count
    FROM tokens
    WHERE token IN (
        'amor',
        'te amo',
        'te adoro',
        'mi vida',
        'preciosa',
        'hermosa',
        'bonita',
        'linda',
        'divina',
        'feliz',
        'besitos',
        'abrazos',
        'tranquila'
    )
    GROUP BY token
    ORDER BY word_count DESC, token ASC
    LIMIT :limit
    """
)
