FROM docker.io/library/nginx:1.28-alpine AS assets
COPY site-assets/ /tmp/site-assets/
RUN mkdir /site && cat /tmp/site-assets/part-* | tar -xz -C /site

FROM docker.io/library/nginx:1.28-alpine
COPY deploy/nginx.conf /etc/nginx/nginx.conf
COPY dist/ /usr/share/nginx/html/
COPY --from=assets /site/ /usr/share/nginx/html/
USER nginx
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s CMD wget -q -O /dev/null http://127.0.0.1:8080/healthz || exit 1
ENTRYPOINT ["nginx"]
CMD ["-g", "daemon off;"]
