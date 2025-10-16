-- Creates database, user, and grants for local development
-- Adjust names/passwords as needed

CREATE DATABASE flask_blog;

DO $$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles WHERE rolname = 'flaskuser'
   ) THEN
      CREATE ROLE flaskuser LOGIN PASSWORD 'flaskpass';
   END IF;
END
$$;

GRANT ALL PRIVILEGES ON DATABASE flask_blog TO flaskuser;

