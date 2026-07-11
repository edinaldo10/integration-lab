#!/bin/bash

# Define cores para facilitar a leitura no terminal
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo "=== INICIANDO FLUXO DE INTEGRAÇÃO ==="

# Faz a chamada e armazena o status code
RESPONSE=$(curl -s -w "%{http_code}" -o response.json http://localhost:8001/start)

if [ "$RESPONSE" == "200" ]; then
    echo -e "${GREEN}Sucesso!${NC} Resposta do Serviço A:"
    cat response.json | jq
else
    echo -e "${RED}Erro na integração!${NC} Status: $RESPONSE"
    cat response.json | jq
fi

echo "=== FIM ==="