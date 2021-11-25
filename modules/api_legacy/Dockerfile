FROM python:3.8-alpine as base
FROM base as builder

RUN mkdir /install
WORKDIR /install

COPY requirements.txt /requirements.txt

#RUN apk add --no-cache build-base gcc geos libc-dev musl-dev linux-headers libffi-dev postgresql-dev
#RUN apk add --no-cache build-base musl-dev linux-headers libffi-dev postgresql-dev geos-dev
RUN apk add build-base musl-dev linux-headers postgresql-dev geos-dev

#RUN pip install --no-cache-dir --upgrade pip && \
#    pip install --no-cache-dir --prefix=/install -r /requirements.txt

RUN pip install --upgrade pip && \
    pip install --prefix=/install -r /requirements.txt

FROM base

RUN apk add --no-cache geos musl libpq
COPY --from=builder /install /usr/local

EXPOSE 5000

COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]