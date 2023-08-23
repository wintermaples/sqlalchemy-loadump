FROM python:3.8.17-bullseye

# Install mssql odbc driver
WORKDIR /root/
ENV ACCEPT_EULA=Y
RUN curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc
RUN curl https://packages.microsoft.com/config/debian/11/prod.list | tee /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
    ACCEPT_EULA=Y apt-get install -y mssql-tools18 && \
    ACCEPT_EULA=Y apt-get install -y unixodbc-dev


# Setup tests
RUN mkdir /application/
WORKDIR /application/
RUN pip install poetry
COPY ./ ./
RUN poetry install

ENTRYPOINT ["poetry", "run", "pytest", "tests/py_tests/"]
