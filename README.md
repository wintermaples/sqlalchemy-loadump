# sqlalchemy-loadump
This library makes your software to dump and load data in databases with sqlalchemy.


## Dependencies
- Python 3.8+
- SQLAlchemy 2.0+


## Development dependencies
- Poetry
- Docker
- Docker Compose


## Installation
### Latest version
```pip install sqlalchemy-loadump```

### Specific version(e.g. 0.1.1)
```pip install sqlalchemy-loadump==0.1.1```


## Usage
### Commandline
#### Dump
This command dumps data in the postgresql database to the json file.

**You need installing the database adapter before using this command. In below example, you need installing psycopg2.**

```commandline
python -m sqlalchemy_loadump dump \
--dump-file-type=json \
--dump-file-path=dump.json \
--db-url=postgresql+psycopg2://user:password@host:port/database
```

#### Load
This command loads data from the json file and inserts it into the postgresql database.

**You need installing the database adapter before using this command. In below example, you need installing psycopg2.**

```commandline
python -m sqlalchemy_loadump load \
--dump-file-type=json \
--dump-file-path=dump.json \
--db-url=postgresql+psycopg2://user:password@host:port/database
```

## Supported Dump Formats
- JSON


## Supported Databases
- PostgreSQL
- Microsoft SQLServer


## Development Setup
### Install docker & docker-compose
This library uses docker & docker-compose to test.

You can install docker & docker-compose by following [this link](https://docs.docker.com/engine/install/).

### Install poetry
This library uses poetry to manage dependencies and build.

You can install poetry by following [this link](https://python-poetry.org/docs/).

### Install dependencies
Installing dependencies for this library.

```commandline
poetry install
```
