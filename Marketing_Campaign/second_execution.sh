#!/bin/bash
docker-compose --verbose -f postgres-docker-compose.yml up kensu_load_data_with_pandas_v2
docker-compose --verbose -f postgres-docker-compose.yml up kensu_model_predict
docker-compose --verbose -f postgres-docker-compose.yml up kensu_run_dbt_postgres