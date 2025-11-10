# syntax=docker/dockerfile:1
FROM python:3.13-alpine

ENV UV_PYTHON_DOWNLOADS=never \
    TZ="Europe/Moscow" \
    LANG="en_US.UTF-8"
ARG app_user_name=appuser \
    app_user_id=1000

SHELL ["/bin/sh", "-exc"]

COPY --link --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

RUN <<EOF
apk upgrade
rm -rf /var/cache/apk/*
EOF

RUN adduser -D $app_user_name -u $app_user_id

USER $app_user_name

WORKDIR /app

ADD --chown=$app_user_name:$app_user_name . /app/

RUN --mount=type=cache,destination=/home/$app_user_name/.cache/uv,uid=$app_user_id <<EOF
uv sync --locked
EOF

CMD ["uv", "run", "./run.py"]