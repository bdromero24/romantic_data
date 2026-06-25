    SELECT sender, COUNT(*) AS message_count
    FROM messages
    GROUP BY sender
    ORDER BY message_count desc;
    
    
SELECT DATE_TRUNC('day', timestamp) AS message_day,
COUNT(*) AS message_count
    FROM messages
    GROUP BY message_day
    ORDER BY message_day;
    
 
 
   SELECT EXTRACT(HOUR FROM timestamp) AS message_hour,
           COUNT(*) AS message_count
    FROM messages
    GROUP BY message_hour
    ORDER BY message_hour;
   
WITH conteo_diario AS (
    SELECT 
        DATE(timestamp) AS fecha, 
        COUNT(*) AS total_mensajes
    FROM messages
    GROUP BY DATE(timestamp)
)
SELECT ROUND(AVG(total_mensajes),0) AS promedio_mensajes_por_dia
FROM conteo_diario;

    SELECT COUNT(*) AS occurrence_count
    FROM messages
    WHERE message_normalized ILIKE :keyword_pattern ESCAPE '\\'
       OR message ILIKE :keyword_pattern ESCAPE '\\';
    
    
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
    
 
    SELECT
    COUNT(*) AS mensajes_con_te_amo
FROM messages
WHERE message_normalized ~* '\mte\s+amo\M';




SELECT COUNT(*) AS mensajes_con_te_extraño
FROM messages
WHERE message_normalized ~* '\yte\s+extra(ñ|a±)o\y';

SELECT
    COUNT(*) AS mensajes_con_odio_general
FROM messages
WHERE message_normalized ~* '\modio\M';

SELECT
    COUNT(*) AS mensajes_con_odio_general
FROM messages
WHERE message_normalized ~* '\mextrano\M';



DELETE FROM messages
WHERE message  IS NULL OR message = ''
and message_normalized  IS NULL OR message_normalized = '';

select * FROM messages
WHERE message  IS NULL OR message = ''
and message_normalized  IS NULL OR message_normalized = '';
   




UPDATE messages
SET sender = 'David'
WHERE sender = 'David Romero';

UPDATE messages
SET sender = '𝑴𝒂𝒓🍓'
WHERE sender = '𝑴𝒂𝒓 𝑭𝒓𝒆𝒔𝒊𝒕𝒂🍓';


UPDATE messages
SET sender = '𝑴𝒂𝒓🍓'
WHERE sender = 'Mar🍓';



-- Diagnostico no destructivo de fechas fuera del rango esperado.
SELECT id, source, sender, message, timestamp
FROM messages
WHERE timestamp < '2025-10-10 00:00:00.000 -0500'
   OR timestamp > '2026-06-21 23:59:59.000 -0500'
ORDER BY timestamp ASC, id ASC;

-- Diagnostico no destructivo de meses sospechosos por inversion dia/mes.
SELECT DATE_TRUNC('month', timestamp) AS message_month,
       COUNT(*) AS message_count
FROM messages
WHERE EXTRACT(MONTH FROM timestamp) IN (8, 12)
GROUP BY message_month
ORDER BY message_month;
