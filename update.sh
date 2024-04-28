#!/bin/sh

curl -X POST "https://api.cloudflare.com/client/v4/zones/$cf_api/purge_cache" \
     -H "Authorization: Bearer $cf_zone" \
     --data "{  \"purge_everything\": true }"
