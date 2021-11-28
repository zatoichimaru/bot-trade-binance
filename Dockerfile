FROM python:3.10.0-slim-buster

WORKDIR /src

COPY requirements.txt requirements.txt

RUN apt-get update \
    && apt-get -y install curl \
    && pip3 install --upgrade pip \
    && pip3 install --no-cache-dir -r requirements.txt \
    && pip3 list

ENV PYTHONUNBUFFERED 1

COPY . .

COPY ./entrypoint.sh /

RUN chmod +x /entrypoint.sh

CMD ["bash","/entrypoint.sh"]
