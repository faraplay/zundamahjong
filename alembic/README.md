## Alembic cheatsheet

```sh
python alembic/create.py   # populate a brand new database

alembic current --verbose  # check revision of connected database

alembic history            # check alembic revision history

alembic upgrade head       # run migrations on connected database
```

## Starting new migration

Whenever there is a change in database metadata, create a new Alembic revision with

```sh
alembic revision -m "<Your Message Here>" --autogenerate
```

Check the resulting new file in `alembic/versions` and edit it until it does what you want.
