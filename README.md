<h1 align="center">sqlalchemy-loadump</h1>

<p align="center"><img src="https://i.imgur.com/vUMAgWM.png" alt="Library image"></p>

<div align="center">

[![.github/workflows/main.yml](https://github.com/wintermaples/sqlalchemy-loadump/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/wintermaples/sqlalchemy-loadump/actions/workflows/main.yml)
![PyPI - Version](https://img.shields.io/pypi/v/sqlalchemy-loadump)
[![Apache-2.0](https://custom-icon-badges.herokuapp.com/badge/license-Apache%202.0-8BB80A.svg?logo=law&logoColor=white)]()
![PyPI - Downloads](https://img.shields.io/pypi/dm/sqlalchemy-loadump)



This library makes your software to dump and load data in databases with sqlalchemy.
</div>


## ✨Features
- Dump data in databases to file
- Load data from file into databases
- Dump/Load without defining SQLAlchemy table


## 📥Installation
### Latest version
```pip install sqlalchemy-loadump```

### Specific version(e.g. 0.1.1)
```pip install sqlalchemy-loadump==0.1.1```


## 📖Usage
### ⌨️Commandline
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


## 📦Dependencies
- Python 3.8+
- SQLAlchemy 2.0+


## 📦Development dependencies
- Poetry
- Docker
- Docker Compose


## 🛠️Supported Dump Formats
- JSON


## 🛠️Supported Databases
- SQLite3
- PostgreSQL
- Microsoft SQLServer

## 🛠️Supported(Tested) DataType List
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

## ⚠️Limitation of the result of dumping. 
The python type of the result of convertion depends on the column type of table reflected by MetaData.reflect.

As a result, there is a possibility of losing type information from the dumped data.

For instance, using SQLite3, when creating a table with a UUID(SQLAlchemy) column and then dumping it, the dumped result will become a string type.

However, for the types listed in the "Supported DataType List," we ensure the proper dumping and loading of data.


## 👨‍💻Development Setup
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
