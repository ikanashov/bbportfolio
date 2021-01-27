#!/bin/bash

# Забираем переменные настройки postgreSQL для поключения 
source ../.env
POSTGRES_URI="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

#Запускаем скрипт генерирующий схему базы данных
#psql $POSTGRES_URI -A -q -t -f create_blackboard_db_schema.sql
echo psql $POSTGRES_URI -A -q -t -f create_blackboard_db_schema.sql

