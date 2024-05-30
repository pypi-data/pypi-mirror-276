# Springless DB Server (sl-dbserver)

This is a simple Python server for the purpose of spinning up and destroying full copies of a
database on demand. An example use-case is running integration tests with a local postgres
instance in a docker container. Each test can create its own isolated database, run its
tests, and then destroy the created database instance when done.

# Requirements

- Python 3.10 or later
- Dependencies specified in `setup.py`

# Installing and running

If you are using this for testing a SQLAlchemy database, install via pip into the same virtual
environment your database is on:

```
pip install sl-dbserver
```

Otherwise create a new virtual environment and install there.

```
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
. .venv/bin/activate
pip install sl-dbserver
```

And then run with Uvicorn, which should be installed as part of the dependencies.

```
uvicorn sl.dbserver.app:main --port 8000
```

You can then access the documentation via the `/doc` or `/redoc` endpoints. So for the example
above, you would go to [http://localhost:8000/doc](http://localhost:8000/doc) or
[http://localhost:8000/redoc](http://localhost:8000/redoc), which will list the available
endpoints and documentation on the data to post to each.

