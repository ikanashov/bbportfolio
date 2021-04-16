FROM python:3.9-slim-buster as base

FROM base as builder

RUN mkdir /install
RUN apt-get update && apt-get -y install g++ unixodbc-dev
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip && pip install --prefix=/install -r /requirements.txt

FROM base

# Add pyodbc and msodbcsql17 library for work with MS SQL Database
RUN apt-get update && apt-get -y install libodbc1 curl libgssapi-krb5-2 gnupg &&\
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - &&\
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list &&\
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

COPY --from=builder /install /usr/local
COPY docker-entrypoint.sh /
COPY . /app
WORKDIR /app