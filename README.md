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
This command dumps data in the sqlite3 database (db.sqlite3) to the json file.

```commandline
python -m sqlalchemy_loadump dump \
--dump-file-type=json \
--dump-file-path=dump.json \
--db-url=sqlite:///db.sqlite3
```

#### Load
This command loads data from the json file and inserts it into the sqlite3 database (db.sqlite3) database.

```commandline
python -m sqlalchemy_loadump load \
--dump-file-type=json \
--dump-file-path=dump.json \
--db-url=sqlite:///db.sqlite3
```

## Supported Dump Formats
- JSON


## Supported Databases
- SQLite3
- PostgreSQL
- Microsoft SQLServer

## Supported(Tested) DataType List
### SQLite3
<details>
    <summary>DataType List</summary>

    - BigInteger
    - Boolean
    - Date
    - DateTime
    - Double
    - Enum
    - Float
    - Integer
    - (Interval) ・・・ Treated as DateTime
    - LargeBinary
    - Numeric
    - SmallInteger
    - String
    - Text
    - Time
    - Unicode
    - UnicodeText
    - Uuid
</details>

### PostgreSQL
<details>
    <summary>DataType List</summary>

    - BigInteger
    - Boolean
    - Date
    - DateTime
    - Double
    - Enum
    - Float
    - Integer
    - Interval
    - LargeBinary
    - Numeric
    - SmallInteger
    - String
    - Text
    - Time
    - Unicode
    - UnicodeText
    - Uuid
</details>

### Microsoft SQLServer
<details>
    <summary>DataType List</summary>

    - BigInteger
    - Boolean
    - Date
    - DateTime
    - Double
    - Enum
    - Float
    - Integer
    - (Interval) ・・・ Treated as DateTime
    - LargeBinary
    - Numeric
    - SmallInteger
    - String
    - Text
    - Time
    - Unicode
    - UnicodeText
    - Uuid
</details>

## Limitation of the result of dumping. 
The python type of the result of convertion depends on the column type of table reflected by MetaData.reflect.

As a result, there is a possibility of losing type information from the dumped data.

For instance, using SQLite3, when creating a table with a UUID(SQLAlchemy) column and then dumping it, the dumped result will become a string type.

However, for the types listed in the "Supported DataType List," we ensure the proper dumping and loading of data.


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
