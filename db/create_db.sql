-- 1. Verificar dónde estás conectado
SELECT current_database(), current_user;

-- 2. Crear usuario solo si no existe
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_catalog.pg_roles WHERE rolname = 'landing'
    ) THEN
        CREATE ROLE landing LOGIN PASSWORD 'page';
    END IF;
END
$$;

-- 3. Permitir conexión a la base
GRANT CONNECT ON DATABASE chat TO landing;

-- 4. Permitir uso y creación en schema public
GRANT USAGE, CREATE ON SCHEMA public TO landing;

-- 5. Permisos sobre tablas y secuencias existentes
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO landing;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO landing;

-- 6. Permisos sobre objetos futuros
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL PRIVILEGES ON TABLES TO landing;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL PRIVILEGES ON SEQUENCES TO landing;

-- 7. Validar permisos
SELECT 
    has_schema_privilege('landing', 'public', 'USAGE') AS has_usage,
    has_schema_privilege('landing', 'public', 'CREATE') AS has_create;