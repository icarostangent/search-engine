FROM postgres:16

EXPOSE 5432

HEALTHCHECK --interval=5s --timeout=1s --retries=5 CMD pg_isready || exit 1