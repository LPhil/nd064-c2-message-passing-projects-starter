FROM python:3.8-alpine as base
FROM base as builder

RUN mkdir /install
WORKDIR /install

COPY requirements.txt /requirements.txt

RUN apk add build-base postgresql-dev
RUN pip install --upgrade pip && \
    pip install --prefix=/install -r /requirements.txt


FROM base

RUN apk add --no-cache libpq
COPY --from=builder /install /usr/local

WORKDIR /
COPY . .

CMD ["python", "app.py"]