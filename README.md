# Black C website

Complete bilingual Black C construction website, with the current design, project pages, company profile and 300-frame scroll animation. Page code is included in `dist/`; binary assets are included as split archives in `site-assets/` and extracted automatically during the container build. No Node.js build or external CDN is required to deploy.

## Ubuntu + Podman service

Use Ubuntu 24.04 LTS or newer with Podman 4.4+, systemd and cgroup v2. Run the following as a regular user with sudo access:

```bash
sudo apt update
sudo apt install -y podman git curl uidmap
sudo loginctl enable-linger "$USER"
git clone https://github.com/husam0091/Black-website.git
cd Black-website
bash deploy/install.sh
bash deploy/smoke-test.sh
```

Visit `http://SERVER_IP:8080`. If UFW is already enabled and you want direct access, allow the port with `sudo ufw allow 8080/tcp`. The installer builds the image locally, installs a rootless Quadlet service and starts it. Linger keeps the user service running after logout and at boot; the Quadlet's `[Install]` section starts it automatically. Do not run `systemctl enable` on the generated service.

Port 8080 must be available. To change it, edit `PublishPort=8080:8080` in `deploy/black-website.container`, rerun the installer, and adjust the health check URL in the installer and smoke test command. The second port remains 8080.

```bash
systemctl --user status black-website.service
journalctl --user -u black-website.service -f
systemctl --user restart black-website.service
systemctl --user stop black-website.service
```

To update:

```bash
git pull --ff-only
bash deploy/install.sh
bash deploy/smoke-test.sh
```

## Domain and HTTPS

The container serves HTTP on 8080. Put your existing HTTPS reverse proxy in front of it and forward to `http://127.0.0.1:8080`. For proxy-only access, set `PublishPort=127.0.0.1:8080:8080` before installation. Configure your domain, DNS and certificate in the proxy. Website metadata still uses the current Sites domain; update the canonical, hreflang, Open Graph and schema URLs before using your own domain.

## Run without systemd

```bash
podman build -f Containerfile -t localhost/black-website:latest .
podman run -d --name black-website -p 8080:8080 --read-only --tmpfs /tmp:rw,size=64m --cap-drop=all --security-opt=no-new-privileges localhost/black-website:latest
bash deploy/smoke-test.sh
```

## Editing

The container serves `dist/` directly. HTML pages, `dist/style.css`, `dist/app.js`, images and both desktop/mobile frame sequences are included. To extract the binary assets locally before editing or running the page generators:

```bash
cat site-assets/part-* | tar -xz -C dist
```

After changing binary assets, run `python3 deploy/pack-assets.py` before building (the container uses archived binary assets). Source generators are retained for larger content changes:

```bash
python3 build-ar.py
python3 enhance-home.py
```

These regenerate page content; direct HTML edits can be overwritten. CSS and JS remain in `dist/`. Editable content is in `dist/content/`. Rebuild/restart the container after changes. The original motion-generation video is not required to serve the included frames.

The quote form prepares a WhatsApp message for the visitor to send; it is not an email/backend submission. Analytics hooks require a configured GA4 or Plausible integration. The Nginx container runs as an unprivileged user with a read-only filesystem and writable temporary storage.

## Validation

Shell syntax and site assets were checked during preparation. A container runtime was not available in the preparation environment; run the included smoke test on Ubuntu after installation to verify the service. Podman Quadlet documentation: https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html
