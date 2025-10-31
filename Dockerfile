# syntax=docker/dockerfile:1
FROM python:3.13-alpine

ENV UV_PYTHON_DOWNLOADS=never \
    TZ="Europe/Moscow" \
    LANG="en_US.UTF-8"

SHELL ["/bin/sh", "-exc"]

COPY --link --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

RUN <<EOF
apk upgrade
rm -rf /var/cache/apk/*
EOF

RUN adduser -D appuser

USER appuser

WORKDIR /app

ADD --chown=adduser:adduser . /app/

RUN --mount=type=cache,destination=/home/appuser/.cache/uv <<EOF
uv sync --locked
EOF

CMD ["uv", "run", "./run.py"]