FROM python:3.8-alpine as base
FROM base as builder

RUN mkdir /install
WORKDIR /install

COPY requirements.txt /requirements.txt

RUN apk add build-base linux-headers libffi-dev
RUN pip install --upgrade pip && \
    pip install --prefix=/install -r /requirements.txt


FROM base

RUN apk add --no-cache libstdc++
COPY --from=builder /install /usr/local

WORKDIR /app
COPY . .

EXPOSE 5000 5005

CMD ["python", "wsgi.py"]