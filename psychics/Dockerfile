FROM python:3.8.10-slim as libraries-installer

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt


FROM python:3.8.10-slim as psychics-backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/venv/bin:$PATH"

COPY --from=libraries-installer /opt/venv /opt/venv

RUN addgroup --system --gid 5858 rootless \
    && adduser --system --ingroup rootless --no-create-home --uid 5757 rootless

WORKDIR /src
COPY /src/ /src/

RUN chown -R rootless:rootless /src

USER rootless