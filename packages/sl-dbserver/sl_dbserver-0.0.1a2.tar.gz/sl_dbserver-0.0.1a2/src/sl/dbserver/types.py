import typing as _t
import pydantic as _pyd
import fastapi as _fapi


class ApiError(_pyd.BaseModel):
    result: _t.Literal["Err"] = "Err"
    message: str

    def to_httperr(self):
        return _fapi.HTTPException(status_code=404, detail=self.message)


class Credentials(_pyd.BaseModel):
    username: str = _pyd.Field(
        title="Username",
        description="Database username",
    )
    password: str = _pyd.Field(
        title="Password",
        description="Database password",
    )


class CreatedDb(_pyd.BaseModel):
    url: str = _pyd.Field(
        title="URL",
        description="URL string to use to connect to the newly-created database",
    )
    drop_id: str = _pyd.Field(
        title="Drop ID", description="Use this value to drop the database later."
    )


_schemadef_type_desc = """\
Specifies the type of `value`:
- `sqlalchemy` - A path to a sqlalchemy metadata object; eg: `sl.module.db:metadata`.
- `file` - The path to a SQL file that should be run to build the models. It is recommended that
this be an absolute path, and the file must be resident on the same filesystem on which the server
is running. eg: `/path/to/file.sql`.
- `raw_sql` - Raw SQL passed in through the value which will create the schema.
"""


class SchemaDef(_pyd.BaseModel):
    """Define how to load the schema"""

    type: _t.Literal["sqlalchemy", "file", "raw_sql"] = _pyd.Field(
        title="Type", description=_schemadef_type_desc
    )
    value: str = _pyd.Field(
        title="Value",
        description=(
            "Value that corresponds to the type. See the type field for more information."
        ),
    )


_seeddata_type_desc = """\
Specifies the type of `value`:
- `json` - Raw JSON-formatted data, structured as:
```
{
    "metadata": "abs.path.to.module:metadata",
    "data": {
        "table_1_name": [
            {
                "int_col": 1,
                "str_col": "value",
                ...
            },
            ...entries
        ],
        "table_2_name": [ ...entries ],
        ...tables
    }
}
```
- `sql` - Raw SQL containing `INSERT`/`UPDATE`/etc. statements.
- `file` - Path to file local to the dbserver containing `json`/`sql` data structured as described
above
- `module` - Module path to a file local to the dbserver containing `json`/`sql` data structured
as described above. A module path consists of a python module, followed by a colon, then the rest
of the path to the file. eg. `sl.dbserver.__test__:seeds/test.json`. The module path portion can
only include directories recognizable as Python modules (ie. containing an `__init__.py` file).
Any subdirectories after that point which are not python modules must be included after the colon.
"""


class SeedData(_pyd.BaseModel):
    """Define a source for seed data for the newly created database"""

    type: _t.Literal["json", "sql", "file", "module"] = _pyd.Field(
        title="Type",
        description=_seeddata_type_desc,
    )
    value: str = _pyd.Field(
        title="Value",
        description=(
            "Value that corresponds to the type. See the type field for more information."
        ),
    )


class CreateDbArgs(_pyd.BaseModel):
    url: str = _pyd.Field(
        title="Connection string",
        description=(
            "A database connection string, eg: `postgres://user:password@localhost:5432/db_name`. "
            "The user/password combination must have database CREATE privileges."
        ),
    )
    append_name: str = _pyd.Field(
        default="",
        title="Append name",
        description=(
            "String to append to the database name when creating. Used for differentiating tests"
        ),
    )
    with_timestamp: bool = _pyd.Field(
        default=False,
        title="With timestamp",
        description=(
            'Set to "true" to include a timestamp in a created database name. This can help '
            "differentiate different runs of the same test"
        ),
    )
    schema_def: SchemaDef = _pyd.Field(
        alias="schema",
        title="Schema Definition",
        description=(
            "Used to create the database schema after the database has been created."
        ),
    )
    seeds: _t.List[SeedData] = _pyd.Field(
        default=[],
        title="Seed data",
        description=(
            "Seed data files to load into the database after creation. Will be loaded in the same "
            "order they are provided."
        ),
    )
    keep_db_on_error: bool = _pyd.Field(
        default=False,
        title="Keep Database on Error",
        description=(
            "By default an error while creating the database will cause the server to return the "
            "error raised and clean up the broken build. Setting this value to `true` will keep "
            "the broken database intact."
        ),
    )
    reset_seq: bool = _pyd.Field(
        default=False,
        title="Reset sequences",
        description=(
            "When using a SQLAlchemy module as the schema, any autoincrement sequences in the "
            "database will **not** be automatically set correctly to the maximum value of the "
            "inserted items. This can lead to insert problems later, where a newly inserted "
            "value will attempt to take an ID already taken by another item in the database. "
            "This option **only** works when using a sqlalchemy metadata object to load the "
            "schema, and will find all of the known autoincrementing sequences and set them equal "
            "to the highest value in the column that the sequence is attached to. It will do "
            "this only if seed values are loaded, and only if the schema was loaded via a "
            "sqlalchemy MetaData object. If loading via SQL just make sure to set the sequences "
            "properly as part of loading the seed."
        ),
    )


class DropDbArgs(_pyd.BaseModel):
    drop_id: str = _pyd.Field(
        title="Drop ID",
        description=(
            "The `drop_id` passed back to you from the initial database creation."
        ),
    )
