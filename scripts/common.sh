#!/bin/bash

# =========================
# LOGGING PADRÃO
# =========================

log() {
    local level=${2:-INFO}
    local msg=$1
    local ts=$(date +'%Y-%m-%d %H:%M:%S')
    # Gera um log formatado em JSON para o Loki processar facilmente
    printf '{"ts": "%s", "level": "%s", "msg": "%s", "trace_id": "%s"}\n' \
        "$ts" "$level" "$msg" "$TRACE_ID"
}

info() {
  log "$1" "INFO"
}

warn() {
  log "$1" "WARN"
}

error() {
  log "$1" "ERROR"
}

# =========================
# TRACE ID (simples)
# =========================

generate_trace_id() {
  if command -v uuidgen >/dev/null 2>&1; then
    uuidgen
  else
    date +%s%N
  fi
}

TRACE_ID=${TRACE_ID:-$(generate_trace_id)}

# =========================
# CALL HTTP PADRONIZADO
# =========================

call_api() {
  local url=$1
  local method=${2:-GET}
  local data=${3:-}
  local trace_id=${TRACE_ID}

  local response_file
  response_file=$(mktemp)

  local http_code

  info "HTTP CALL -> $method $url (trace_id=$trace_id)"

  if [ -z "$data" ]; then
    http_code=$(curl -s -o "$response_file" -w "%{http_code}" \
      -X "$method" \
      -H "X-Trace-Id: $trace_id" \
      "$url")
  else
    http_code=$(curl -s -o "$response_file" -w "%{http_code}" \
      -X "$method" \
      -H "Content-Type: application/json" \
      -H "X-Trace-Id: $trace_id" \
      -d "$data" \
      "$url")
  fi

  local body
  body=$(cat "$response_file")
  rm -f "$response_file"

  # saída estruturada para consumo em script
  echo "HTTP_CODE=$http_code"
  echo "BODY=$body"

  if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
    return 0
  else
    return 1
  fi
}
