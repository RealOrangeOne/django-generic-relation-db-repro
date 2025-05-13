# Django generic relation reproduction

A repository to reproduce a bug with modifying generic relations, where the wrong database connection is used.

Confirmed on Django 4.2, 5.0, 5.1 and 5.2.

# Usage

```
uv venv
uv pip install django
.venv/bin/python ./manage.py test
```

When running the tests, they'll fail. The failure shows queries being executed against the replica connection. Since they're `UPDATE` queries, they should run against the "default" connection, instead.

# Steps to recreate

1. `django-admin startproject`
2. Create second database connection, pointing to the same database, but using MIRROR in tests.
3. Create a database router to use the secondary connection for reads and the default for writes (see `db_router.py`).
4. Create 2 models, with a generic relationship between them (see `models.py`).
