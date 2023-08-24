# Test

**!! You need development setup before test. !!**

## Run tests
```commandline
cd tests/docker/; docker compose up --exit-code-from tester; docker compose down -v; docker image rm sqlalchemy-loadump-mssql sqlalchemy-loadump-postgres sqlalchemy-loadump-tester; cd ../../
```