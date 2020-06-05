#!/usr/bin/env bash

export PYTHONPATH=$(pwd)

export API_PORT=8000
export API_EXPOSED_PORT=5000
export API_CACHE_TIME=31536000
export DJANGO_SETTINGS_MODULE=core.settings.dev
export APP_SECRET_KEY=2q8dw7aio-4bh4mv_zq2#6x$atf5mkwx$^abn0t4twvb8p8%-#
export APP_ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0

# Database
export DB_PG_DB=route_api
export DB_PG_USER=dev
export DB_PG_PASS=dev
export DB_PG_PORT=25432

# Cache
export REDIS_PORT=26379
