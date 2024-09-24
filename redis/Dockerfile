FROM redis:7.4

EXPOSE 6379

HEALTHCHECK --interval=5s --timeout=1s --retries=5 CMD redis-cli ping || exit 1