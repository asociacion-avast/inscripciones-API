#!/bin/bash
set -e

# Connect as the default user and set up the users and databases
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname=template1 <<-EOSQL
    -- Create databases
    CREATE DATABASE inscripciones_dev;
    CREATE DATABASE inscripciones_test;

    -- Create development user
    CREATE USER dev_user WITH PASSWORD 'dev_password';
    GRANT ALL PRIVILEGES ON DATABASE inscripciones_dev TO dev_user;

    -- Create testing user
    CREATE USER test_user WITH PASSWORD 'test_password';
    GRANT ALL PRIVILEGES ON DATABASE inscripciones_test TO test_user;

    -- Drop the default postgres database
    DROP DATABASE IF EXISTS postgres;
EOSQL

# Connect to each database and grant privileges on the public schema
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname=inscripciones_dev <<-EOSQL
    GRANT ALL ON SCHEMA public TO dev_user;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO dev_user;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname=inscripciones_test <<-EOSQL
    GRANT ALL ON SCHEMA public TO test_user;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO test_user;
EOSQL
