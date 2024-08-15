#!/bin/bash

TEXT="Einstein gilt als einer der bedeutendsten Physiker der Wissenschaftsgeschichte und weltweit als einer der bekanntesten Wissenschaftler der Neuzeit."

QUERY="Erstelle einen Titelvorschlag für folgenden Artikel:\n$TEXT" 

MODEL_NAME=$(basename $1)

MODEL_CONTAINER_PATH="/models/$MODEL_NAME"

curl http://localhost:10300/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d "{
         \"model\": \"${MODEL_CONTAINER_PATH}\",
         \"messages\": [
             {\"role\": \"user\", \"content\": \"${QUERY}\"}
         ]
     }"