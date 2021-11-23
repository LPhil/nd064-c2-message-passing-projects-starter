FROM python:3.8-alpine as base
FROM base as builder

RUN mkdir /install
WORKDIR /install

COPY requirements.txt /requirements.txt
COPY dist/UdaDB* /

RUN apk add build-base geos-dev libffi-dev postgresql-dev
RUN pip install --prefix=/install -r /requirements.txt && \
    pip install --prefix=/install /UdaDB* && \
    pip install --upgrade pip

FROM base

RUN apk add --no-cache geos libpq
COPY --from=builder /install /usr/local

EXPOSE 5000

COPY . .
CMD ["python", "wsgi.py"]