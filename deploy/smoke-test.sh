#!/usr/bin/env bash
set -euo pipefail
base="${1:-http://127.0.0.1:8080}"
for route in /healthz / /company /projects /contact /ar/ /ar/company /ar/contact /assets/riyadh-frames/frame-000.webp /assets/riyadh-frames/frame-299.webp /assets/riyadh-frames/m/frame-299.webp; do
  curl --fail --silent --output /dev/null "$base$route"
done
status=$(curl --silent --output /dev/null --write-out '%{http_code}' "$base/does-not-exist")
[[ "$status" == 404 ]] || { echo "Expected 404, got $status" >&2; exit 1; }
echo 'English, Arabic, clean URLs, animation assets and 404 passed.'
