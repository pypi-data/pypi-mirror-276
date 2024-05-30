from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md")) as f:
    README = f.read()

requires = [
    # For DB management
    "sqlalchemy[asyncio]          >= 1, < 2",
    "python-dateutil              >= 2",
    "sqlalchemy-utils",
    "psycopg2-binary              >= 2",
    "python-slugify               >= 4",
    # For server
    "fastapi[all]",
    "uvicorn[standard]",
]

dev_requires = [
    "pytest                >= 7",
    "pytest-cov            >= 4",
    "pytest-asyncio        >= 0.17",
    "mypy                  >= 0.812",
    "requests              >= 2, < 3",
    "types-python-dateutil >= 2, < 3",
    "black                 >= 23",
    "alembic               >= 1",
    "build",
    "twine",
]

setup(
    name="sl-dbserver",
    version="0.0.1a2",
    license="MIT",
    description="Springless Database Server",
    long_description=README,
    author="cogs",
    author_email="cogs@springless.com",
    url="https://github.com/Springless/sl-dbserver",
    packages=find_packages("src"),
    package_dir={"": "src"},
    namespace_packages=["sl"],
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    extras_require={
        "dev": dev_requires,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Testing",
    ],
    entry_points={
        "console_scripts": [
            "sl-dbserver=sl.dbserver.cli:start_server",
        ],
    },
    keywords="sl springless database server testing postgresql",
)
