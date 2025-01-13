#!/bin/sh

export PGUSER="postgres"

psql -c "CREATE DATABASE chipin"

psql chipin -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"

