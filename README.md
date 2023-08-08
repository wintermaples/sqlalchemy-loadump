# sqlalchemy-loadump
This library makes your software to dump and load data in databases with sqlalchemy.

## Dependencies
- Python 3.8+
- SQLAlchemy 2.0+

## Installation
**!!!!! Needs poetry !!!!!** 

It will install the library from github.

```commandline
poetry add git+ssh://git@github.com:wintermaples/sqlalchemy-loadump.git
```

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
