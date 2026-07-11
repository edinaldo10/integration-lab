#!/bin/bash
source ./common.sh

URL="http://localhost:8001/start"

MAX_RETRIES=3
SLEEP_BETWEEN=2

attempt=1

info "INICIANDO FLUXO RESILIENTE"

while [ $attempt -le $MAX_RETRIES ]; do
  info "Tentativa $attempt de $MAX_RETRIES"

  if output=$(call_api "$URL"); then
    info "SUCESSO NA TENTATIVA $attempt"
    echo "$output"
    exit 0
  else
    warn "FALHA NA TENTATIVA $attempt"
  fi

  attempt=$((attempt + 1))
  sleep $SLEEP_BETWEEN
done

error "FLUXO FALHOU APÓS $MAX_RETRIES TENTATIVAS"
exit 1
