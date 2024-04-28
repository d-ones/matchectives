#!/bin/sh

echo $cf_api
echo $cf_zone

curl -X POST "https://api.cloudflare.com/client/v4/zones/$cf_zone/purge_cache" \
     -H "Authorization: Bearer $cf_api" \
     --data "{  \"purge_everything\": true }"
