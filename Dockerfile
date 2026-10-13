# Static site served by unprivileged nginx. Listens on 8080, so the Azure
# Container App ingress target port must be 8080.
FROM nginxinc/nginx-unprivileged:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY site/ /usr/share/nginx/html/

EXPOSE 8080
