#!/bin/sh

TZ="GMT"
DS=$(date)
TM=$(date +"%a, %d %b %Y" -d "$DATE + 1 day")
ES="${TM} 00:00:00 GMT"

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
          "execute": {
            "operation": "set",
            "value": "'$ES'"
          }
        }
      }
    }
  ]
}'

curl --request PUT https://api.cloudflare.com/client/v4/zones/$cf_zone/rulesets/$http_response_header_id \
     --header "Authorization: Bearer $header_api" \
     --header "Content-Type: application/json" --data "$CM"
