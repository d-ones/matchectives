#!/bin/sh

curl -X POST "https://api.cloudflare.com/client/v4/zones/$cf_zone/purge_cache" \
     -H "Authorization: Bearer $cf_api" \
     -H "Content-Type: application/json" \
     --data "{  \"purge_everything\": true }"
