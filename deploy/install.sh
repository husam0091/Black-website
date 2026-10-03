#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
if [[ $(id -u) == 0 ]]; then
  echo 'Run this script as your regular deployment user, without sudo.' >&2
  exit 1
fi
command -v podman >/dev/null || { echo 'Install Podman first: sudo apt install podman' >&2; exit 1; }
version=$(podman --version | awk '{print $3}')
if [[ $(printf '%s\n' 4.4 "$version" | sort -V | head -n1) != 4.4 ]]; then
  echo 'Podman 4.4 or newer is required for Quadlet. Use Ubuntu 24.04 LTS or newer.' >&2
  exit 1
fi
podman build -f Containerfile -t localhost/black-website:latest .
unit_dir="${XDG_CONFIG_HOME:-$HOME/.config}/containers/systemd"
mkdir -p "$unit_dir"
install -m 644 deploy/black-website.container "$unit_dir/black-website.container"
systemctl --user daemon-reload
systemctl --user restart black-website.service
for attempt in {1..20}; do
  if curl --fail --silent http://127.0.0.1:8080/healthz >/dev/null; then
    echo 'Black C is running on port 8080.'
    exit 0
  fi
  sleep 1
done
journalctl --user -u black-website.service -n 30 --no-pager
exit 1
