#!/usr/bin/env bash

ID=$1

RESPONSE=$(curl -X GET \
             "http://0.0.0.0:8080/api/evaluations/{$ID}" \
             -H 'accept: application/json' \
             -H "Content-Type: application/json")

echo ${RESPONSE} | jq .
echo ${RESPONSE} | jq -r .id | echo "Evaluation ID: $(cat)"
echo ${RESPONSE} | jq -r .ilab_evaluation.status | echo "Ilab Eval Status: $(cat)"
echo ${RESPONSE} | jq -r .openai_evaluation.status | echo "OpenAI Eval Status: $(cat)"
