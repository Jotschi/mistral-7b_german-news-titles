#!/bin/bash

TEXT="Einstein gilt als einer der bedeutendsten Physiker der Wissenschaftsgeschichte und weltweit als einer der bekanntesten Wissenschaftler der Neuzeit."

MODEL_NAME=$(basename $1)

MODEL_CONTAINER_PATH="/models/$MODEL_NAME"

for count in 7 14 18 20 24 ; do
    echo
    echo "Titel für $count Wörter:"
    QUERY="Erstelle einen $count Wörter langen Titelvorschlag für folgenden Artikel:\n$TEXT" 
    curl -s http://localhost:10300/v1/chat/completions \
         -H "Content-Type: application/json" \
         -d "{
             \"model\": \"${MODEL_CONTAINER_PATH}\",
             \"messages\": [
                 {\"role\": \"user\", \"content\": \"${QUERY}\"}
             ]
         }" | jq -r .choices[0].message.content
done