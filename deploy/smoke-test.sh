#!/usr/bin/env bash
set -euo pipefail
base="${1:-http://127.0.0.1:8080}"
for route in /healthz / /company /projects /contact /ar/ /ar/company /ar/contact /assets/riyadh-frames/frame-000.webp /assets/riyadh-frames/frame-299.webp /assets/riyadh-frames/m/frame-299.webp; do
  curl --fail --silent --output /dev/null "$base$route"
done
status=$(curl --silent --output /dev/null --write-out '%{http_code}' "$base/does-not-exist")
[[ "$status" == 404 ]] || { echo "Expected 404, got $status" >&2; exit 1; }
echo 'English, Arabic, clean URLs, animation assets and 404 passed.'

# Confirm HTML is served as a document rather than plain text or a download.
for route in /company /company.html /ar/company /ar/company.html; do
  headers=$(curl --location --fail --silent --head "$base$route")
  printf '%s\n' "$headers" | tr -d '\r' | grep -Eiq '^content-type: text/html([;[:space:]]|$)'
  printf '%s\n' "$headers" | grep -Eiq '^content-security-policy:'
  printf '%s\n' "$headers" | grep -Eiq '^x-content-type-options: nosniff'
done
for route in /.git/config /.env /app.js.map /backup.sql /build-content.py; do
  status=$(curl --silent --output /dev/null --write-out '%{http_code}' "$base$route")
  [[ "$status" == 404 ]] || { echo "Sensitive path returned $status: $route" >&2; exit 1; }
done
echo 'HTML content type, security headers and sensitive-path checks passed.'
