#!/usr/bin/env bash

RESPONSE=$(curl -X POST \
  'http://0.0.0.0:8080/api/evaluations/' \
  -H 'accept: application/json' \
  -H "Content-Type: application/json" \
  -d @./input.json)

echo ${RESPONSE} | jq .

echo ${RESPONSE} | jq -r .id | echo "Evaluation ID: $(cat)"
