#!/bin/sh

TZ="GMT"
DS=$(date)
TM=$(date +"%a, %d %b %Y" -d "$DATE + 1 day")
ES="${TM} 04:00:00 GMT"

curl -X POST "https://api.cloudflare.com/client/v4/zones/$cf_zone/purge_cache" \
     -H "Authorization: Bearer $cf_api" \
     -H "Content-Type: application/json" \
     --data "{  \"purge_everything\": true }"

CM='{
  "rules": [
    {
      "expression": "true",
      "description": "cache-expire",
      "action": "rewrite",
      "action_parameters": {
        "headers": {
          "expires": {
            "operation": "set",
            "value": "'$ES'"
          }
        }
      }
    },
    {
      "expression": "true",
      "description": "cache-control",
      "action": "rewrite",
      "action_parameters": {
        "headers": {
          "cache-control": {
            "operation": "set",
            "value": "no-cache, must-revalidate, max-age=0"
          }
        }
      }
    }
  ]
}'

curl -X PUT "https://api.cloudflare.com/client/v4/zones/$cf_zone/rulesets/$http_response_header_id" \
     -H "Authorization: Bearer $header_api" \
     -H "Content-Type: application/json" \
     --data "$CM"
