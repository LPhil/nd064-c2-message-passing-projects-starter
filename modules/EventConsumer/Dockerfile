FROM python:3.8-alpine as base
FROM base as builder

RUN mkdir /install
WORKDIR /install

COPY requirements.txt /requirements.txt

RUN apk add build-base postgresql-dev libffi-dev
RUN pip install --prefix=/install -r /requirements.txt && \
    pip install --upgrade pip

FROM base

RUN apk add --no-cache libpq
COPY --from=builder /install /usr/local

WORKDIR /
COPY . .

CMD ["python", "app.py"]