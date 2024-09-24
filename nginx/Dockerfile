FROM nginx:1.27

EXPOSE 80

HEALTHCHECK --interval=5s --timeout=1s --retries=5 CMD curl -f http://localhost || exit 1